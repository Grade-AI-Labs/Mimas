#!/usr/bin/env python3
"""Tests for check_inheritance_suffix.py. Run: python3 test_check_inheritance_suffix.py"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_inheritance_suffix.py")

RULE = """\
### {id}
```yaml
id: {id}
title: test rule
scope: {scope}
severity: high
intent: test
check_logic: test
evidence_expectation: file and line
allowed_exceptions: none
source: user-specified
status: {status}
{automation}
```
"""

ANY_BASE = """\
automation:
  check_type: inheritance_suffix
  apply_scope: changed-files
  selector:
    class_name_suffix: Repository
    exclude: [BaseRepository]
  expectation:
    base_class_suffix: Repository
    match_strategy: any-base-with-suffix"""

SAME_STEM = """\
automation:
  check_type: inheritance_suffix
  selector:
    class_name_suffix: Controller
  expectation:
    base_class_suffix: MainController"""

INDEX = """\
# Review Policy Index

## Routing Map
| File subtree | Module policy |
| --- | --- |
| `src/billing/**` | `module-billing.md` |
"""


def rule(rule_id: str, automation: str, scope: str = "global", status: str = "active") -> str:
    return RULE.format(id=rule_id, scope=scope, status=status, automation=automation)


class CheckerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.policies = self.repo / "policies"
        self.policies.mkdir()
        (self.policies / "POLICY_INDEX.md").write_text(INDEX)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, rel: str, text: str) -> None:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text))

    def check(self, changed: list[str]) -> dict:
        listing = self.repo / "changed.txt"
        listing.write_text("\n".join(changed) + "\n")
        out = subprocess.run(
            [sys.executable, str(SCRIPT), "--policies-dir", str(self.policies), "--repo", str(self.repo),
             "--changed-files", str(listing)],
            capture_output=True, text=True, check=True,
        ).stdout
        return {r["rule_id"]: r for r in json.loads(out)["rules"]}

    def test_any_base_with_suffix_fails_bare_class_and_honours_exclude(self) -> None:
        (self.policies / "global-policy.md").write_text(rule("RP-GLOBAL-001", ANY_BASE))
        self.write("src/shared/base_repository.py", "class BaseRepository:\n    pass\n")
        self.write("src/orders/repo.py", """\
            from shared.base_repository import BaseRepository
            class OrderRepository(BaseRepository):
                pass
            class ArchivedOrderRepository(OrderRepository):
                pass
            """)
        self.write("src/billing/repo.py", "\n\nclass CreditNoteRepository:\n    pass\n")
        result = self.check(["src/shared/base_repository.py", "src/orders/repo.py", "src/billing/repo.py", "README.md"])
        r = result["RP-GLOBAL-001"]
        self.assertEqual(r["status"], "fail")
        self.assertEqual([(v["file"], v["line"], v["class"]) for v in r["violations"]],
                         [("src/billing/repo.py", 3, "CreditNoteRepository")])
        self.assertEqual(r["skipped_excluded"], ["src/shared/base_repository.py:1 BaseRepository()"])
        self.assertIn("src/orders/repo.py:4 ArchivedOrderRepository(OrderRepository)", r["evaluated"])

    def test_same_stem_suffix_across_languages(self) -> None:
        (self.policies / "global-policy.md").write_text(rule("RP-GLOBAL-001", SAME_STEM))
        self.write("web/order.ts", "// class FakeController extends Nothing\nexport class OrderController extends OrderMainController<T> {}\n")
        self.write("api/Invoice.cs", "public sealed class InvoiceController : InvoiceMainController, IDisposable\n{\n}\n")
        self.write("api/Cart.java", "/* header */\npublic class CartController extends BaseController {\n}\n")
        r = self.check(["web/order.ts", "api/Invoice.cs", "api/Cart.java"])["RP-GLOBAL-001"]
        self.assertEqual(r["status"], "fail")
        self.assertEqual([(v["file"], v["line"], v["expected"]) for v in r["violations"]],
                         [("api/Cart.java", 2, "CartMainController")])
        self.assertEqual(len(r["evaluated"]), 3)

    def test_passes_when_all_classes_comply(self) -> None:
        (self.policies / "global-policy.md").write_text(rule("RP-GLOBAL-001", ANY_BASE))
        self.write("src/orders/repo.py", "class OrderRepository(base.BaseRepository):\n    pass\n")
        self.assertEqual(self.check(["src/orders/repo.py"])["RP-GLOBAL-001"]["status"], "pass")

    def test_malformed_metadata_is_unknown_not_an_error(self) -> None:
        broken = ANY_BASE.replace("    base_class_suffix: Repository\n", "")
        bad_strategy = SAME_STEM + "\n    match_strategy: nonsense-strategy"
        (self.policies / "global-policy.md").write_text(
            rule("RP-GLOBAL-001", broken) + rule("RP-GLOBAL-002", bad_strategy) + rule("RP-GLOBAL-003", ""))
        self.write("src/orders/repo.py", "class OrderRepository:\n    pass\n")
        result = self.check(["src/orders/repo.py"])
        self.assertEqual(result["RP-GLOBAL-001"]["status"], "unknown")
        self.assertIn("base_class_suffix", result["RP-GLOBAL-001"]["reason"])
        self.assertEqual(result["RP-GLOBAL-002"]["status"], "unknown")
        self.assertIn("nonsense-strategy", result["RP-GLOBAL-002"]["reason"])
        self.assertNotIn("RP-GLOBAL-003", result)  # no automation: not a deterministic rule

    def test_module_rule_only_checks_its_routed_subtree(self) -> None:
        (self.policies / "module-billing.md").write_text(rule("RP-BILLING-001", ANY_BASE, scope="module:billing"))
        (self.policies / "module-orders.md").write_text(rule("RP-ORDERS-001", ANY_BASE, scope="module:orders"))
        self.write("src/billing/repo.py", "class InvoiceRepository(BaseRepository):\n    pass\n")
        self.write("src/orders/repo.py", "class OrderRepository:\n    pass\n")
        result = self.check(["src/billing/repo.py", "src/orders/repo.py"])
        self.assertEqual(result["RP-BILLING-001"]["status"], "pass")
        self.assertEqual(result["RP-BILLING-001"]["targets"], ["src/billing/repo.py"])
        self.assertEqual(result["RP-ORDERS-001"]["status"], "unknown")  # no route in POLICY_INDEX.md

    def test_unparseable_and_unsupported_files_are_unknown(self) -> None:
        (self.policies / "global-policy.md").write_text(rule("RP-GLOBAL-001", ANY_BASE))
        self.write("src/broken.py", "class OrderRepository(:\n")
        self.write("src/Order.kt", "class OrderRepository(val x: Int) : BaseRepository()\n")
        r = self.check(["src/broken.py", "src/Order.kt"])["RP-GLOBAL-001"]
        self.assertEqual(r["status"], "unknown")
        self.assertEqual({u["file"] for u in r["unknown_targets"]}, {"src/broken.py", "src/Order.kt"})

    def test_inactive_rules_and_deleted_files_are_skipped(self) -> None:
        (self.policies / "global-policy.md").write_text(rule("RP-GLOBAL-001", ANY_BASE, status="deprecated"))
        self.assertEqual(self.check(["src/deleted.py"]), {})


if __name__ == "__main__":
    unittest.main()
