"""Observe ten additional CVE models through files, SQLite and dependency calls."""
from contextlib import closing
from html import escape
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import unittest
from unittest.mock import patch
from urllib.parse import quote

from test_named_cves import load, workspace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lab import read_catalog
from runner import run_cases

IDS = {
    "python/spring4shell-binding": "CVE-2022-22965",
    "python/jenkins-cli-atfile": "CVE-2024-23897",
    "python/fortios-forwarded-auth": "CVE-2022-40684",
    "python/confluence-setup-reopen": "CVE-2023-22515",
    "python/gitlab-reset-recipients": "CVE-2023-7028",
    "python/minio-bootstrap-disclosure": "CVE-2023-28432",
    "python/activemq-openwire-type": "CVE-2023-46604",
    "python/zabbix-role-projection": "CVE-2024-42327",
    "python/imagetragick-delegate": "CVE-2016-3714",
    "python/apache-proxy-request-splitting": "CVE-2023-25690",
}


class ExtensionCatalogTests(unittest.TestCase):
    def test_all_new_contracts_execute_both_variants(self):
        cases = [case for case in read_catalog() if case["id"] in IDS]
        self.assertEqual({case["id"] for case in cases}, set(IDS))
        for case in cases:
            self.assertEqual(case["cve"], [IDS[case["id"]]])
            self.assertTrue(case["references"])
        records, failed = run_cases(cases, strict=True)
        self.assertFalse(failed, json.dumps(records, indent=2))
        self.assertEqual(sum(len(r["checks"]) for r in records), 2 * sum(len(c["tests"]) for c in cases))

    def test_malformed_json_shapes_do_not_crash_fixed_handlers(self):
        for cid in IDS:
            module = load(cid.split("/", 1)[1], "fixed")
            with self.subTest(case=cid), workspace():
                for value in (None, [], {}, True, 42):
                    result = module.run(value)
                    self.assertIn(result["status"], {400, 401, 404})


class IndependentEffectsTests(unittest.TestCase):
    def test_spring_internal_binding_changes_actual_log_destination_only_when_vulnerable(self):
        property_name = "class.module.classLoader.pipeline.prefix"
        for variant in ("vulnerable", "fixed"):
            module = load("spring4shell-binding", variant)
            with self.subTest(variant=variant), workspace() as work:
                module.run({"fields": {"name": "changed", property_name: "private"}})
                target = work / "logs/private.log"
                self.assertEqual(target.exists(), variant == "vulnerable")
                if target.exists(): self.assertEqual(target.read_text(), "user=changed\n")
                else: self.assertFalse((work / "logs").exists())
                module.run({"fields": {"profile.display_name": "Approved"}})
                self.assertEqual((work / "logs/access.log").read_text(), "user=alice\n")

    def test_jenkins_discloses_first_line_before_help_authorization(self):
        for variant in ("vulnerable", "fixed"):
            module = load("jenkins-cli-atfile", variant)
            with self.subTest(variant=variant), workspace() as work:
                (work / "credentials.txt").write_text("UNIQUE_PRIVATE_LINE\nSECOND_LINE\n")
                with patch.object(module, "expand", wraps=module.expand) as expand:
                    result = module.run({"args": ["@credentials.txt"], "token": "wrong"})
                self.assertEqual(result["status"], 403)
                self.assertEqual(result["argument"], "UNIQUE_PRIVATE_LINE" if variant == "vulnerable" else "@credentials.txt")
                self.assertEqual(expand.call_count, 1 if variant == "vulnerable" else 0)

    def test_fortios_spoof_cannot_modify_existing_key_file_after_fix(self):
        headers = {"User-Agent": "Report Runner", "Forwarded": 'for="[127.0.0.1]:12345"',
                   "Authorization": "Bearer invalid"}
        for variant in ("vulnerable", "fixed"):
            module = load("fortios-forwarded-auth", variant)
            with self.subTest(variant=variant), workspace() as work:
                target = work / "appliance-admin.keys"
                target.write_text("LAB_KEY_EXISTING\n")
                module.run({"headers": headers, "key": "LAB_KEY_FORGED"})
                self.assertEqual(target.read_text(), "LAB_KEY_FORGED\n" if variant == "vulnerable" else "LAB_KEY_EXISTING\n")

    def test_confluence_setup_state_survives_separate_calls_and_uses_real_rows(self):
        prop = "bootstrapStatusProvider.applicationConfig.setupComplete"
        for variant in ("vulnerable", "fixed"):
            module = load("confluence-setup-reopen", variant)
            with self.subTest(variant=variant), workspace(), patch.dict(os.environ, {"BADASS_SETUP_MODE": "installed"}):
                module.run({"steps": [{"path": "/server-info.action", "params": {prop: "false"}}]})
                module.run({"steps": [{"path": "/setup/setupadministrator.action", "user": "forged"}]})
                with closing(sqlite3.connect("setup.sqlite")) as db:
                    self.assertEqual(db.execute("SELECT name, role FROM users").fetchall(),
                                     [("forged", "admin")] if variant == "vulnerable" else [])
                    self.assertEqual(db.execute("SELECT complete FROM state").fetchone(), (1,))

    def test_gitlab_token_is_only_delivered_to_server_verified_recipients_after_fix(self):
        for variant in ("vulnerable", "fixed"):
            module = load("gitlab-reset-recipients", variant)
            with self.subTest(variant=variant), workspace() as work, \
                    patch.dict(module.VERIFIED, {"alice": {"verified@example.test"}}, clear=True):
                module.run({"email": ["unverified@example.test", "verified@example.test"], "verified": True})
                deliveries = json.loads((work / "outbox.json").read_text())
                self.assertEqual([item["to"] for item in deliveries],
                                 ["unverified@example.test", "verified@example.test"] if variant == "vulnerable" else ["verified@example.test"])
                self.assertTrue(all(item["token"] == "LAB_RESET_TOKEN" for item in deliveries))

    def test_minio_configuration_is_not_loaded_before_peer_authentication(self):
        for variant in ("vulnerable", "fixed"):
            module = load("minio-bootstrap-disclosure", variant)
            with self.subTest(variant=variant), patch.object(module, "load_server_config", return_value={"secret": "UNIQUE_CLUSTER_SECRET"}) as config:
                result = module.run({"path": "/bootstrap/verify", "token": "wrong"})
                if variant == "vulnerable":
                    self.assertEqual(result["environment"], {"secret": "UNIQUE_CLUSTER_SECRET"})
                    config.assert_called_once()
                else:
                    self.assertEqual(result["status"], 401)
                    config.assert_not_called()
                config.reset_mock()
                result = module.run({"path": "/bootstrap/verify", "token": "LAB_CLUSTER_PEER_TOKEN"})
                self.assertEqual(result["status"], 200)
                config.assert_called_once()

    def test_activemq_error_return_does_not_hide_constructor_side_effect(self):
        for variant in ("vulnerable", "fixed"):
            module = load("activemq-openwire-type", variant)
            with self.subTest(variant=variant), workspace() as work, \
                    patch.dict(module.CONTEXTS, {"lab://unique": "<beans><marker>UNIQUE_CONTEXT_EFFECT</marker></beans>"}):
                result = module.run({"class": "ContextLoader", "message": "lab://unique"})
                self.assertEqual(result["status"], 400)
                target = work / "loaded-context.txt"
                self.assertEqual(target.exists(), variant == "vulnerable")
                if target.exists(): self.assertEqual(target.read_text(), "UNIQUE_CONTEXT_EFFECT")

    def test_zabbix_projection_is_rejected_before_database_execution(self):
        module = load("zabbix-role-projection", "fixed")
        with patch.object(module.sqlite3, "connect") as connect:
            result = module.run({"token": "LAB_API_READER", "selectRole": ["name", "(SELECT token FROM roles) AS injected"]})
            self.assertEqual(result["status"], 400)
            connect.assert_not_called()

    def test_imagetragick_fix_keeps_the_resource_in_one_literal_argv_element(self):
        url = 'https://images.test/x$(printf UNIQUE_DELEGATE_EFFECT > delegate-marker)'
        document = '<svg xmlns="http://www.w3.org/2000/svg"><image href="' + escape(url, quote=True) + '"/></svg>'
        for variant in ("vulnerable", "fixed"):
            module = load("imagetragick-delegate", variant)
            with self.subTest(variant=variant), workspace() as work, \
                    patch.object(module.subprocess, "run", wraps=module.subprocess.run) as execute:
                result = module.run(document)
                marker = work / "delegate-marker"
                self.assertEqual(marker.exists(), variant == "vulnerable")
                if variant == "vulnerable": self.assertEqual(marker.read_text(), "UNIQUE_DELEGATE_EFFECT")
                else:
                    self.assertEqual(result["echo"], url)
                    self.assertEqual(execute.call_args.args[0], ["/usr/bin/printf", "%s", url])
                    self.assertIs(execute.call_args.kwargs["shell"], False)

    def test_proxy_bytes_contain_two_request_lines_only_when_vulnerable(self):
        value = 'public HTTP/1.1\r\nHost: backend.test\r\n\r\nGET /private?x='
        for variant in ("vulnerable", "fixed"):
            module = load("apache-proxy-request-splitting", variant)
            with self.subTest(variant=variant), workspace() as work, patch.object(module, "backend", wraps=module.backend) as backend:
                result = module.run(quote(value, safe=""))
                target = work / "upstream.http"
                if variant == "vulnerable":
                    self.assertEqual(result["status"], 200)
                    request_lines = re.findall(rb"(?:^|\r\n)GET ([^ ]+) HTTP/1\.1\r\n", target.read_bytes())
                    self.assertEqual(request_lines, [b"/backend?q=public", b"/private?x="])
                    backend.assert_called_once()
                else:
                    self.assertEqual(result["status"], 400)
                    self.assertFalse(target.exists())
                    backend.assert_not_called()


if __name__ == "__main__":
    unittest.main()
