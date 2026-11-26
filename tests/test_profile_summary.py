"""Testes do utilitário de perfil."""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import profile_summary  # noqa: E402


def valid_config() -> dict:
    """Retorna uma configuração mínima e válida."""
    return {
        "username": "JNeves07",
        "name": "João Marcelo",
        "role": "Desenvolvedor Back-End",
        "theme": "tokyonight",
        "technologies": ["Python", "Docker", "APIs REST"],
        "stats": {"public_repos": 9, "contributions_last_year": 31},
        "cards": ["3-stats.svg"],
    }


class ProfileSummaryTests(unittest.TestCase):
    """Cobre validação, resumo e erros amigáveis."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.config_path = self.root / "profile-config.json"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_config(self, config: dict) -> None:
        """Grava a configuração no diretório temporário."""
        self.config_path.write_text(
            json.dumps(config, ensure_ascii=False), encoding="utf-8"
        )

    def write_card(self, theme: str, name: str) -> None:
        """Cria um SVG falso para o teste."""
        card_dir = self.root / "profile-summary-card-output" / theme
        card_dir.mkdir(parents=True, exist_ok=True)
        (card_dir / name).write_text("<svg />", encoding="utf-8")

    def test_validate_valid_config_with_cards(self) -> None:
        self.write_config(valid_config())
        self.write_card("tokyonight", "3-stats.svg")

        config = profile_summary.load_config(self.config_path)
        cards_dir = self.root / "profile-summary-card-output"
        self.assertEqual(profile_summary.validate_config(config, cards_dir=cards_dir), [])

    def test_validate_reports_missing_and_invalid_fields(self) -> None:
        config = {
            "username": "",
            "name": "João",
            "role": "Back-End",
            "technologies": ["Python", "Python", ""],
            "stats": {"public_repos": -1},
            "cards": "3-stats.svg",
        }

        errors = profile_summary.validate_config(config)

        self.assertTrue(any("username" in error for error in errors))
        self.assertTrue(any("duplicado" in error for error in errors))
        self.assertTrue(any("stats.contributions_last_year" in error for error in errors))
        self.assertTrue(any("stats.public_repos" in error for error in errors))
        self.assertTrue(any("cards" in error for error in errors))

    def test_validate_rejects_missing_card_file(self) -> None:
        config = valid_config()
        cards_dir = self.root / "profile-summary-card-output"

        errors = profile_summary.validate_config(config, cards_dir=cards_dir)

        self.assertTrue(any("card não encontrado" in error for error in errors))

    def test_summary_includes_technologies_and_stats(self) -> None:
        summary = profile_summary.build_summary(valid_config())
        rendered = profile_summary.format_summary(summary)

        self.assertEqual(summary["technologies"]["total"], 3)
        self.assertEqual(summary["stats"]["public_repos"], 9)
        self.assertIn("APIs REST", rendered)
        self.assertIn("31 contribuições no último ano", rendered)
        self.assertIn("Cards (1, tema tokyonight)", rendered)

    def test_invalid_json_returns_friendly_error(self) -> None:
        self.config_path.write_text('{"username":', encoding="utf-8")

        with self.assertRaises(profile_summary.ProfileConfigError) as context:
            profile_summary.load_config(self.config_path)

        self.assertIn("JSON inválido", str(context.exception))

    def test_cli_validate_and_summary_succeed(self) -> None:
        self.write_config(valid_config())
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            code = profile_summary.main(
                ["--config", str(self.config_path), "--no-card-check"]
            )

        self.assertEqual(code, 0)
        self.assertIn("Configuração válida.", stdout.getvalue())
        self.assertIn("JNeves07", stdout.getvalue())

    def test_cli_json_output_is_parseable(self) -> None:
        self.write_config(valid_config())
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            code = profile_summary.main(
                ["--config", str(self.config_path), "--summary", "--json", "--no-card-check"]
            )

        self.assertEqual(code, 0)
        data = json.loads(stdout.getvalue())
        self.assertEqual(data["stats"]["contributions_last_year"], 31)

    def test_cli_invalid_json_returns_exit_code_one(self) -> None:
        self.config_path.write_text("{invalid", encoding="utf-8")
        stderr = io.StringIO()

        with contextlib.redirect_stderr(stderr):
            code = profile_summary.main(
                ["--config", str(self.config_path), "--validate", "--no-card-check"]
            )

        self.assertEqual(code, 1)
        self.assertIn("Erro: JSON inválido", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
