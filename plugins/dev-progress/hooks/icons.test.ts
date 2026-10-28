import type { On } from 'claude-code'
import { expect, mock, test } from 'claude-code/testing'
import type { Engine } from 'claude-code/testing'

const PLUGIN = 'dev-progress'
const PROGRESS = 'mcp__dev-progress__progress'
const pane = { title: '', isFocused: false, bodyColumns: 80, placement: 'dock', scroll: { offset: 0, bodyRows: 40 }, view: {} } as const
const band = { hasSurvey: false, isWorking: false, maxRows: 4, bodyColumns: 100, scroll: { offset: 0, bodyRows: 4 }, view: {} }

// Starts one running subagent of `type` and returns the desktop panel's drawings.
const panelWith = async ($: Engine, on: On, type: string): Promise<string> => {
  mock.clock(on)
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('agent.spawn', () => ({ model: 'claude-opus-5-5', agentId: 'a1' }))
  await $.agent.spawn({ tool_use_id: 't1', prompt: 'Build ticket 3.', description: 'Ticket three', subagentType: type, provider: 'engine', parentModel: 'claude-opus-5-5', background: true, fork: false } as never)
  const ui = await $.ui.mount({ plugin: PLUGIN, surface: 'desktop', component: 'Pane', requestId: 'dev-agents', props: pane })
  return (await ui.findAll({ type: 'Svg' })).map(el => String(el.props.source)).join('')
}

test('icons: the crabs by default', async ($, on) => {
  const drawn = await panelWith($, on, 'dev-workflow:tier-medium')
  expect(drawn).toContain('class="c-medium run"')
  expect(drawn).not.toContain('j-medium')
})

test('icons: jdm draws a car for the tier, wheels turning while it runs', { options: { icons: 'jdm' } }, async ($, on) => {
  const drawn = await panelWith($, on, 'dev-workflow:tier-medium')
  expect(drawn).toContain('class="j-medium run"')
  expect(drawn).toContain('class="jwa"')
  expect(drawn).not.toContain('c-medium')
  expect(drawn).not.toContain('class="la"')
})

test('icons: jdm draws the explorer as the sand Pajero', { options: { icons: 'jdm' } }, async ($, on) => {
  const drawn = await panelWith($, on, 'dev-workflow:explorer')
  expect(drawn).toContain('class="j-explore run"')
  expect(drawn).toContain('#C9A66B')
})

test('icons: jdm puts the kei truck on the progress bar', { options: { icons: 'jdm' } }, async $ => {
  await $.tool.call({ tool: PROGRESS, title: 'Ship it', phase: 'delegate', total: 2 } as never)
  const ui = await $.ui.mount({ plugin: PLUGIN, surface: 'desktop', component: 'AbovePrompt', props: band })
  const row = String((await ui.find({ type: 'Svg' }))?.props.source)
  expect(row).toContain('j-other')
  expect(row).not.toContain('c-other')
})

test('icons: an unknown value keeps the crabs', { options: { icons: 'tanks' } }, async ($, on) => {
  const drawn = await panelWith($, on, 'dev-workflow:tier-medium')
  expect(drawn).toContain('class="c-medium run"')
})
