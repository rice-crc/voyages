"""Validate the resolved Compose service contract without starting containers."""
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ComposeContractTests(unittest.TestCase):
    def test_adminer_is_absent_and_dependencies_resolve(self):
        for compose in sorted(ROOT.glob("docker-compose*.yml")):
            if compose.name not in ("docker-compose.yml", "docker-compose-as.yml"):
                continue
            with self.subTest(compose=compose.name):
                result = subprocess.run(
                    ["docker", "compose", "-f", str(compose), "--profile", "*",
                     "config", "--format", "json"],
                    cwd=ROOT, capture_output=True, text=True, check=True,
                )
                services = json.loads(result.stdout)["services"]
                self.assertTrue(services)
                self.assertIn("voyages-mysql", services)
                self.assertIn("voyages-solr", services)
                self.assertIn("voyages-redis", services)
                for name, service in services.items():
                    self.assertNotIn("adminer", name.lower())
                    self.assertNotIn("adminer", service.get("image", "").lower())
                    for dependency in service.get("depends_on", {}):
                        self.assertIn(dependency, services)
                    for port in service.get("ports", []):
                        self.assertNotEqual(str(port.get("published")), "8080")
                if "voyages-api" in services:
                    for name in ("voyages-api", "voyages-stats", "voyages-people-networks", "voyages-geo-networks"):
                        self.assertIn(name, services)
                else:
                    for name in ("voyages-django", "voyages-nginx", "voyages-mailhog"):
                        self.assertIn(name, services)

if __name__ == "__main__":
    unittest.main()
