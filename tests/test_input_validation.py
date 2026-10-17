"""Exercise real fixed entry points with synthetic Unicode and JSON boundaries."""
from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.parse import urlencode
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]


def load_fixed(case):
    path = ROOT / "labs" / case / "fixed/main.py"
    spec = importlib.util.spec_from_file_location("fixture_" + uuid4().hex, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AuthenticationInputTests(unittest.TestCase):
    def test_csrf_accepts_valid_token_and_rejects_unicode_and_json_types(self):
        run = load_fixed("python/csrf").run
        self.assertEqual(run({"csrf": "lab-session-csrf-token"}), "TRANSFERRED")
        for token in ("é", "\ud800", "\udcff", "", None, True, 1, [], {}, "wrong"):
            with self.subTest(token=repr(token)):
                self.assertEqual(run({"csrf": token}), "DENIED")
        for request in (None, [], "text", True, 12, {}):
            with self.subTest(request=repr(request)):
                self.assertEqual(run(request), "DENIED")

    def test_bearer_authentication_rejects_invalid_request_and_token_shapes(self):
        run = load_fixed("rest-api/broken-authentication").run
        self.assertEqual(run({"token": "LAB_VALID_TOKEN"}), {"status": 200})
        for token in ("é", "\ud800", "\udcff", None, True, 1, [], {}, "forged"):
            with self.subTest(token=repr(token)):
                self.assertEqual(run({"token": token}), {"status": 401})
        for request in (None, [], "text", True, 12, {}):
            with self.subTest(request=repr(request)):
                self.assertEqual(run(request), {"status": 401})

    def credential_call(self, language, module, value):
        if language == "python":
            return module.run(value)
        if language == "rest-api":
            return module.run({"value": value})
        result = module.run(urlencode({"value": value}))
        return json.loads(result.split("\r\n\r\n", 1)[1])

    def test_configured_passwords_work_in_ascii_and_unicode(self):
        for language in ("python", "rest-api", "cgi"):
            module = load_fixed(language + "/hardcoded-credentials")
            for password in ("LAB_CONFIGURED_PASSWORD", "mot-de-passe-é", "密碼🔐"):
                with self.subTest(language=language, password=password), \
                     patch.dict(os.environ, {"BADASS_ADMIN_PASSWORD": password}):
                    self.assertEqual(self.credential_call(language, module, password), "ADMIN")
                    self.assertEqual(self.credential_call(language, module, password + "-wrong"), "DENIED")

    def test_missing_configuration_fails_closed(self):
        for language in ("python", "rest-api", "cgi"):
            module = load_fixed(language + "/hardcoded-credentials")
            with self.subTest(language=language), patch.dict(os.environ):
                os.environ.pop("BADASS_ADMIN_PASSWORD", None)
                self.assertEqual(self.credential_call(language, module, "BADASS_LAB_DEFAULT"), "DENIED")

    def test_credential_json_types_and_unencodable_strings_fail_closed(self):
        for language in ("python", "rest-api"):
            module = load_fixed(language + "/hardcoded-credentials")
            with patch.dict(os.environ, {"BADASS_ADMIN_PASSWORD": "LAB_CONFIGURED_PASSWORD"}):
                for password in (None, True, 1, [], {}, "é", "\ud800", "\udcff", "x" * 1025):
                    with self.subTest(language=language, password=repr(password)):
                        self.assertEqual(self.credential_call(language, module, password), "DENIED")
        module = load_fixed("rest-api/hardcoded-credentials")
        for request in (None, [], "text", True, {}):
            with self.subTest(request=repr(request)):
                self.assertEqual(module.run(request), "DENIED")

    def test_cgi_rejects_invalid_utf8_surrogates_and_ambiguous_values(self):
        module = load_fixed("cgi/hardcoded-credentials")
        with patch.dict(os.environ, {"BADASS_ADMIN_PASSWORD": "LAB_CONFIGURED_PASSWORD"}):
            queries = (
                "value=%FF", "value=%ED%A0%80", "value=\ud800", "value=\udcff",
                "value=LAB_CONFIGURED_PASSWORD&value=wrong", "a=1&" * 17,
                None, [], {},
            )
            for query in queries:
                with self.subTest(query=repr(query)):
                    result = module.run(query)
                    self.assertEqual(json.loads(result.split("\r\n\r\n", 1)[1]), "DENIED")


class UpstreamValidationTests(unittest.TestCase):
    def test_integer_price_boundaries_remain_functional(self):
        run = load_fixed("rest-api/unsafe-upstream-data").run
        for price in (0, 1, 20, 100):
            with self.subTest(price=price):
                self.assertEqual(run({"upstream": {"price": price}}), 100 - price)

    def test_full_json_shape_is_checked_before_use(self):
        run = load_fixed("rest-api/unsafe-upstream-data").run
        invalid = (
            None, [], "text", {}, {"upstream": None}, {"upstream": []},
            {"upstream": "text"}, {"upstream": {}}, {"upstream": {"price": None}},
            {"upstream": {"price": True}}, {"upstream": {"price": 20.5}},
            {"upstream": {"price": -1}}, {"upstream": {"price": 101}},
            {"upstream": {"price": "20"}}, {"upstream": {"price": []}},
        )
        for request in invalid:
            with self.subTest(request=repr(request)):
                self.assertEqual(run(request), "DENIED")


class StatefulFixtureInputTests(unittest.TestCase):
    def test_invalid_accounts_do_not_mutate_token_store(self):
        module = load_fixed("python/predictable-token")
        for account in (None, [], {}, True, "", "\ud800", "a" * 257):
            store = {"existing": "UNCHANGED"}
            with self.subTest(account=repr(account)):
                self.assertIsNone(module.issue_reset_token(account, store))
                self.assertEqual(store, {"existing": "UNCHANGED"})
                self.assertFalse(module.validate_reset_token(account, "anything", store))
                self.assertFalse(module.consume_reset_token(account, "anything", store))

    def test_password_records_reject_malformed_values_and_unbounded_work_factors(self):
        module = load_fixed("python/weak-password-hash")
        for password in (None, [], {}, True, "", "\ud800", "\udcff", "a" * 1025):
            with self.subTest(password=repr(password)):
                self.assertIsNone(module.hash_password(password))
                self.assertFalse(module.verify_password(password, {}))
        record = module.hash_password("mot-de-passe-é")
        self.assertTrue(module.verify_password("mot-de-passe-é", deepcopy(record)))
        self.assertFalse(module.verify_password("wrong", record))
        for key, value in (("n", 2**60), ("n", True), ("r", -1), ("salt", "\ud800"),
                           ("digest", None), ("digest", "0" * 64), ("algorithm", "md5")):
            changed = deepcopy(record)
            changed[key] = value
            with self.subTest(key=key, value=repr(value)):
                self.assertFalse(module.verify_password("mot-de-passe-é", changed))

    def test_invalid_session_ids_preserve_existing_sessions(self):
        module = load_fixed("python/session-fixation")
        for session_id in (None, [], {}, True, "", "é", "\ud800", "a" * 129):
            sessions = {"existing": "bob"}
            with self.subTest(session_id=repr(session_id)):
                self.assertIsNone(module.login(session_id, "alice", sessions))
                self.assertEqual(sessions, {"existing": "bob"})
                self.assertIsNone(module.resolve_session(session_id, sessions))
                self.assertFalse(module.logout(session_id, sessions))


if __name__ == "__main__":
    unittest.main()
