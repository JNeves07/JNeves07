"""Valida e resume os dados locais do perfil GitHub."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "profile-config.json"
DEFAULT_CARDS = (
    "0-profile-details.svg",
    "1-repos-per-language.svg",
    "2-most-commit-language.svg",
    "3-stats.svg",
    "4-productive-time.svg",
)
REQUIRED_STATS = ("public_repos", "contributions_last_year")
OPTIONAL_STATS = ("followers", "following")
STAT_LABELS = {
    "public_repos": "repositórios públicos",
    "contributions_last_year": "contribuições no último ano",
    "followers": "seguidores",
    "following": "seguindo",
}
THEME_PATTERN = re.compile(r"[A-Za-z0-9_-]+")
URL_PREFIXES = ("https://", "http://")


class ProfileConfigError(Exception):
    """Erro amigável ao ler a configuração do perfil."""


def _is_text(value: Any) -> bool:
    """Verifica se o valor é um texto não vazio."""
    return isinstance(value, str) and bool(value.strip())


def _is_count(value: Any) -> bool:
    """Verifica se o valor é um inteiro não negativo."""
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _is_url(value: Any) -> bool:
    """Verifica se o valor é uma URL http(s) simples."""
    return (
        _is_text(value)
        and value.strip().startswith(URL_PREFIXES)
        and not any(char.isspace() for char in value)
    )


def load_config(path: Path) -> dict[str, Any]:
    """Lê o JSON de configuração com mensagens claras de erro."""
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ProfileConfigError(f"Arquivo não encontrado: {path}") from exc
    except OSError as exc:
        raise ProfileConfigError(f"Não foi possível ler {path}: {exc}") from exc

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ProfileConfigError(
            f"JSON inválido em {path} (linha {exc.lineno}, coluna {exc.colno})."
        ) from exc

    if not isinstance(data, dict):
        raise ProfileConfigError(
            f"Configuração inválida em {path}: a raiz deve ser um objeto JSON."
        )
    return data


def _check_text(config: dict[str, Any], key: str, errors: list[str]) -> None:
    """Valida um campo de texto obrigatório."""
    if key not in config:
        errors.append(f"campo obrigatório ausente: {key}")
    elif not _is_text(config[key]):
        errors.append(f"{key} deve ser um texto não vazio")


def _check_url(config: dict[str, Any], key: str, errors: list[str]) -> None:
    """Valida um campo de URL opcional."""
    if key in config and not _is_url(config[key]):
        errors.append(f"{key} deve ser uma URL http(s) válida")


def validate_config(
    config: dict[str, Any], *, cards_dir: Path | None = None
) -> list[str]:
    """Retorna uma lista de problemas encontrados na configuração."""
    errors: list[str] = []

    for key in ("username", "name", "role"):
        _check_text(config, key, errors)
    for key in ("profile_url", "portfolio_url"):
        _check_url(config, key, errors)

    theme = config.get("theme", "tokyonight")
    if not isinstance(theme, str) or not THEME_PATTERN.fullmatch(theme):
        errors.append("theme deve conter apenas letras, números, '-' ou '_'")

    technologies = config.get("technologies")
    if "technologies" not in config:
        errors.append("campo obrigatório ausente: technologies")
    elif not isinstance(technologies, list) or not technologies:
        errors.append("technologies deve ser uma lista não vazia de textos")
    else:
        seen: set[str] = set()
        for index, item in enumerate(technologies):
            if not _is_text(item):
                errors.append(f"technologies[{index}] deve ser um texto não vazio")
            elif item.strip() in seen:
                errors.append(f"technologies[{index}] está duplicado: {item.strip()}")
            else:
                seen.add(item.strip())

    stats = config.get("stats")
    if "stats" not in config:
        errors.append("campo obrigatório ausente: stats")
    elif not isinstance(stats, dict):
        errors.append("stats deve ser um objeto")
    else:
        for key in REQUIRED_STATS:
            if key not in stats:
                errors.append(f"stats.{key} é obrigatório")
            elif not _is_count(stats[key]):
                errors.append(f"stats.{key} deve ser um inteiro maior ou igual a zero")
        for key in OPTIONAL_STATS:
            if key in stats and not _is_count(stats[key]):
                errors.append(f"stats.{key} deve ser um inteiro maior ou igual a zero")
        unknown = set(stats) - set(REQUIRED_STATS) - set(OPTIONAL_STATS)
        if unknown:
            errors.append(f"stats contém chaves desconhecidas: {', '.join(sorted(unknown))}")

    projects = config.get("featured_projects", [])
    if not isinstance(projects, list):
        errors.append("featured_projects deve ser uma lista")
    else:
        for index, project in enumerate(projects):
            prefix = f"featured_projects[{index}]"
            if not isinstance(project, dict):
                errors.append(f"{prefix} deve ser um objeto")
                continue
            for key in ("name", "url"):
                if not _is_text(project.get(key)):
                    errors.append(f"{prefix}.{key} deve ser um texto não vazio")
            if _is_text(project.get("url")) and not _is_url(project["url"]):
                errors.append(f"{prefix}.url deve ser uma URL http(s) válida")
            if not _is_text(project.get("description")):
                errors.append(f"{prefix}.description deve ser um texto não vazio")
            project_techs = project.get("technologies", [])
            if not isinstance(project_techs, list) or not all(
                _is_text(item) for item in project_techs
            ):
                errors.append(f"{prefix}.technologies deve ser uma lista de textos")

    cards = config.get("cards", list(DEFAULT_CARDS))
    if not isinstance(cards, list) or not cards:
        errors.append("cards deve ser uma lista não vazia de nomes de SVG")
    else:
        for index, card in enumerate(cards):
            if not isinstance(card, str) or not card.endswith(".svg") or "/" in card:
                errors.append(f"cards[{index}] deve ser um nome de arquivo .svg")

        if cards_dir is not None and isinstance(theme, str) and THEME_PATTERN.fullmatch(theme):
            for card in cards:
                if isinstance(card, str) and card.endswith(".svg") and "/" not in card:
                    card_path = cards_dir / theme / card
                    if not card_path.is_file():
                        errors.append(f"card não encontrado: {card_path}")

    return errors


def normalize_config(config: dict[str, Any]) -> dict[str, Any]:
    """Aplica valores padrão e remove variações de espaçamento."""
    stats = {
        key: config["stats"][key]
        for key in (*REQUIRED_STATS, *OPTIONAL_STATS)
        if key in config["stats"]
    }
    return {
        "username": config["username"].strip(),
        "name": config["name"].strip(),
        "role": config["role"].strip(),
        "theme": config.get("theme", "tokyonight").strip(),
        "technologies": sorted({item.strip() for item in config["technologies"]}),
        "stats": stats,
        "projects": [project["name"].strip() for project in config.get("featured_projects", [])],
        "cards": list(config.get("cards", DEFAULT_CARDS)),
    }


def build_summary(config: dict[str, Any]) -> dict[str, Any]:
    """Monta um resumo estruturado com tecnologias e estatísticas."""
    data = normalize_config(config)
    return {
        "username": data["username"],
        "name": data["name"],
        "role": data["role"],
        "theme": data["theme"],
        "technologies": {
            "total": len(data["technologies"]),
            "items": data["technologies"],
        },
        "stats": data["stats"],
        "featured_projects": {
            "total": len(data["projects"]),
            "items": data["projects"],
        },
        "cards": {
            "total": len(data["cards"]),
            "theme": data["theme"],
            "items": data["cards"],
        },
    }


def format_summary(summary: dict[str, Any]) -> str:
    """Formata o resumo para leitura no terminal."""
    tech = summary["technologies"]
    stats = summary["stats"]
    projects = summary["featured_projects"]
    cards = summary["cards"]

    stats_text = " · ".join(
        f"{value} {STAT_LABELS[key]}" for key, value in stats.items() if key in STAT_LABELS
    )
    return "\n".join(
        (
            f"Perfil: {summary['username']} — {summary['name']}",
            f"Cargo: {summary['role']}",
            f"Tecnologias ({tech['total']}): {', '.join(tech['items'])}",
            f"Estatísticas: {stats_text or 'não informadas'}",
            f"Projetos em destaque ({projects['total']}): "
            f"{', '.join(projects['items']) or 'nenhum'}",
            f"Cards ({cards['total']}, tema {cards['theme']}): {', '.join(cards['items'])}",
        )
    )


def _show_errors(errors: list[str]) -> None:
    """Imprime a lista de problemas no stderr."""
    print("Validação falhou:", file=sys.stderr)
    for error in errors:
        print(f"  - {error}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    """Executa a interface de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Valida e resume o perfil GitHub a partir de profile-config.json."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="caminho do profile-config.json (padrão: raiz do repositório)",
    )
    parser.add_argument("--validate", action="store_true", help="valida a configuração")
    parser.add_argument("--summary", action="store_true", help="mostra o resumo local")
    parser.add_argument("--json", action="store_true", help="saída do resumo em JSON")
    parser.add_argument(
        "--no-card-check",
        action="store_true",
        help="não verifica se os SVGs do tema existem",
    )
    args = parser.parse_args(argv)

    if not args.validate and not args.summary:
        args.validate = True
        args.summary = True

    try:
        config = load_config(args.config)
        cards_dir = (
            None if args.no_card_check else args.config.resolve().parent / "profile-summary-card-output"
        )
        errors = validate_config(config, cards_dir=cards_dir)

        if errors:
            _show_errors(errors)
            return 1

        if args.validate:
            print("Configuração válida.")

        if args.summary:
            summary = build_summary(config)
            if args.json:
                print(json.dumps(summary, ensure_ascii=False, indent=2))
            else:
                print(format_summary(summary))
    except ProfileConfigError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
