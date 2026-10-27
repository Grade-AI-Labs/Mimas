import type { On } from 'claude-code'
import { expect, mock, test } from 'claude-code/testing'
import type { Engine } from 'claude-code/testing'

const PLUGIN = 'dev-progress'
const PROGRESS = 'mcp__dev-progress__progress'
const STEP = 'mcp__dev-progress__step'
const pane = { title: '', isFocused: false, bodyColumns: 80, placement: 'dock', scroll: { offset: 0, bodyRows: 40 }, view: {} } as const

// Spawns one subagent of `type` and records the brief it was started with and
// every pane the mod opened.
const spawn = async ($: Engine, on: On, type: string, opened: string[] = []) => {
  const prompts: string[] = []
  mock.clock(on)
  on('ui.open', (_$, e) => {
    opened.push(e.id)
    return { value: { isPlaced: true } }
  })
  on('agent.spawn', (_$, e) => {
    prompts.push(e.prompt)
    return { model: 'claude-opus-5-5', agentId: 'a1' }
  })
  await $.agent.spawn({ tool_use_id: 't1', prompt: 'Build ticket 3.', description: 'Ticket three', subagentType: type, provider: 'engine', parentModel: 'claude-opus-5-5', background: true, fork: false } as never)
  return { prompt: prompts[0] ?? '', opened }
}

const terminalPane = ($: Engine) => $.ui.mount({ plugin: PLUGIN, surface: 'terminal', component: 'Pane', requestId: 'dev-agents', props: pane })

// The dev-workflow tiers, as the Agent tool names them when installed as a plugin and when copied by hand.
for (const [type, tier] of [
  ['dev-workflow:tier-careful', 'careful'],
  ['tier-light', 'light'],
  ['dev-workflow:tier-fable', 'fable'],
] as const) {
  test(`workflow: ${type} is a ${tier} worker`, async ($, on) => {
    const { prompt, opened } = await spawn($, on, type)
    expect(prompt).toContain(STEP)
    expect(opened).toEqual(['dev-agents'])
    const ui = await terminalPane($)
    expect(await ui.find({ type: 'Text', text: new RegExp(`^\\s+${tier} · Opus 5\\.5`) })).toBeDefined()
  })
}

// The pipeline's other agents are workers too, shown by their role.
for (const role of ['explorer', 'merger', 'reviewer'] as const) {
  test(`workflow: dev-workflow:${role} is briefed and shown as ${role}`, async ($, on) => {
    const { prompt, opened } = await spawn($, on, `dev-workflow:${role}`)
    expect(prompt).toContain(STEP)
    expect(opened).toEqual(['dev-agents'])
    const ui = await terminalPane($)
    expect(await ui.find({ type: 'Text', text: new RegExp(`^\\s+${role} · Opus 5\\.5`) })).toBeDefined()
  })
}

test('workflow: an unrelated subagent is listed but not briefed and does not open the panel', async ($, on) => {
  const { prompt, opened } = await spawn($, on, 'general-purpose')
  expect(prompt).toBe('Build ticket 3.')
  expect(opened).toEqual([])
  const ui = await terminalPane($)
  expect(await ui.find({ type: 'Text', text: /^\s+general-purpose · Opus 5\.5/ })).toBeDefined()
})

test('workflow: a brief that already names the step tool is left alone', async ($, on) => {
  const prompts: string[] = []
  mock.clock(on)
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('agent.spawn', (_$, e) => {
    prompts.push(e.prompt)
    return { model: 'claude-opus-5-5', agentId: 'a1' }
  })
  const brief = `Build ticket 3. Report with ${STEP}.`
  await $.agent.spawn({ tool_use_id: 't1', prompt: brief, description: 'Ticket three', subagentType: 'dev-workflow:tier-medium', provider: 'engine', parentModel: 'claude-opus-5-5', background: true, fork: false } as never)
  expect(prompts).toEqual([brief])
})

test('workflow: planned tasks accept the tier-* agent names', async ($, on) => {
  on('ui.open', () => ({ value: { isPlaced: true } }))
  const reported = await $.tool.call({
    tool: PROGRESS,
    title: 'Candidate summary',
    phase: 'delegate',
    tasks: [
      { title: 'Schema and migration', tier: 'tier-heavy' },
      { title: 'Route', tier: 'dev-workflow:tier-light', after: [1] },
    ],
  } as never)
  expect(reported).toMatchObject({ result: 'ok: Tasks 0/2' })
  const ui = await terminalPane($)
  expect(await ui.find({ type: 'Text', text: /^\s+heavy · Opus · xhigh/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /^\s+light · Opus · low · after 1/ })).toBeDefined()
})

test('workflow: the step tool is described for dev-workflow agents', async ($, on) => {
  const tools: { name: string; description: string }[] = []
  on('tool.register', (_$, e) => {
    tools.push({ name: e.name, description: e.description })
    return { value: undefined } as never
  })
  mock.clock(on)
  mock.env(on, { LANG: 'en_US.UTF-8' })
  on('settings.read', async () => ({ value: {} }) as never)
  on('session.start', async () => ({ cwd: '/repo' }) as never)
  await $.session.start({ source: 'startup', cwd: '/repo', surface: 'terminal', isInteractive: true } as never)
  const text = tools.map(t => t.description).join('\n')
  expect(text).toContain('/orchestrate-spec')
  expect(text).toContain('dev-workflow')
  expect(text).not.toContain('savvy')
})
