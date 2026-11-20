import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("audit", ROOT / "mcp_listchange_audit.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class AuditTests(unittest.TestCase):
    def test_flags_call_between_notification_and_refresh(self):
        trace = ['{"jsonrpc":"2.0","method":"notifications/tools/list_changed"}',
                 '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"x"}}',
                 '{"jsonrpc":"2.0","id":2,"method":"tools/list"}']
        result = module.audit(trace)
        self.assertEqual([f["code"] for f in result["findings"]], ["call_before_refresh"])

    def test_flags_unclosed_refresh_window(self):
        result = module.audit(['{"jsonrpc":"2.0","method":"notifications/tools/list_changed"}'])
        self.assertEqual(result["findings"][0]["code"], "missing_refresh")

    def test_fresh_list_closes_window(self):
        trace = ['{"jsonrpc":"2.0","method":"notifications/tools/list_changed"}',
                 '{"jsonrpc":"2.0","id":2,"method":"tools/list"}',
                 '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"x"}}']
        self.assertTrue(module.audit(trace)["ok"])

    def test_invalid_line_report_does_not_echo_content(self):
        result = module.audit(['secret token is not json'])
        self.assertEqual(result["findings"][0]["code"], "invalid_jsonl")
        self.assertNotIn("secret", str(result))

    def test_empty_trace_is_clean(self):
        self.assertTrue(module.audit([])["ok"])


if __name__ == "__main__":
    unittest.main()
