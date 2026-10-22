"""Validate compiled safe-output restrictions, not merely prompt wording."""
from pathlib import Path
import json,re,unittest
ROOT=Path(__file__).resolve().parents[1]
LOCK=ROOT/".github"/"workflows"/"ruff-triage.lock.yml"
SOURCE=ROOT/".github"/"workflows"/"ruff-triage.md"
def compiled_config():
    s=LOCK.read_text(encoding="utf-8")
    m=re.search(r'^\s*GH_AW_SAFE_OUTPUTS_CONFIG: "(.*)"$',s,re.M)
    if m is None:raise ValueError("compiled output config absent")
    return json.loads(json.loads('"'+m.group(1)+'"'))
class WorkflowSecurity(unittest.TestCase):
    def test_compiled_safe_outputs_restrict_comment(self):
        config=compiled_config()
        self.assertEqual(set(config["add_comment"]),{"footer","max","max_links","required_title_prefix","target"})
        self.assertEqual(config["add_comment"]["max"],1)
        self.assertEqual(config["add_comment"]["max_links"],2)
        self.assertEqual(config["add_comment"]["target"],"triggering")
        self.assertEqual(config["add_comment"]["required_title_prefix"],"[EVAL]")
    def test_no_destructive_output_tool(self):
        config=compiled_config()
        self.assertFalse(set(config)&{"close_issue","delete_issue","merge_pull_request","add_labels","create_pull_request"})
        s=SOURCE.read_text(encoding="utf-8")
        self.assertIn("issues: read",s)
        self.assertIn("contents: read",s)
        self.assertIn("engine: copilot",s)
        self.assertIn("roles: [admin, maintainer, write]",s)
        self.assertIn("status-comment: false",s)
        self.assertIn("startsWith(github.event.issue.title, '[EVAL]')",s)
    def test_skill_is_referenced(self):
        s=SOURCE.read_text(encoding="utf-8")
        self.assertIn(".claude/skills/ruff-issue-triage/SKILL.md",s)
        self.assertTrue((ROOT/".claude"/"skills"/"ruff-issue-triage"/"SKILL.md").exists())
    def test_no_expected_labels_in_runtime_tree(self):
        # Submission branch contains golden answers; runtime main should not.
        # On submission, run this assertion as a SKIP rather than a failure.
        if (ROOT/"evals"/"golden").exists():
            self.skipTest("submission branch legitimately contains gold labels")
        self.assertFalse((ROOT/"evals"/"golden").exists())
if __name__=="__main__": unittest.main()

