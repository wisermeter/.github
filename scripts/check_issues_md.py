#!/usr/bin/env python3
"""Confere títulos de seção e labels de ISSUES.md com os formulários."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"
ISSUES_PATH = ROOT / "ISSUES.md"

# Ordem do seletor: nome de arquivo, alfanumérico; YAML antes de Markdown.
FORMS = ("bug.yml", "feature.yml", "question.yml", "task.yml")
SEP = " — "
ITEM_RE = re.compile(
    r"^(\d+)\. \*\*(.+)\*\*"
    + re.escape(SEP)
    + r"(obrigatória|opcional)(?:\. (.*))?\s*$"
)
EMPTY_TEXT = "_No response_"
EMPTY_DROPDOWN = "None"


def backticks(text: str) -> list[str]:
    return re.findall(r"`([^`]*)`", text)


def load_form(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    sections = []
    for item in data["body"]:
        if item.get("type") == "markdown":
            continue
        attrs = item.get("attributes") or {}
        required = bool((item.get("validations") or {}).get("required"))
        options = list(attrs["options"]) if item.get("type") == "dropdown" else None
        default = attrs.get("default") if options is not None else None
        sections.append(
            {
                "label": attrs["label"],
                "required": required,
                "options": options,
                "default": default,
                "type": item["type"],
                "description": attrs.get("description"),
            }
        )
    return {
        "file": path.name,
        "name": data["name"],
        "title": data.get("title") or "",
        "chooser": data.get("description") or "",
        "labels": list(data.get("labels") or []),
        "sections": sections,
    }


def raw_section(doc: str, name: str) -> str | None:
    found = list(re.finditer(rf"^## {re.escape(name)}\s*$", doc, re.M))
    if len(found) != 1:
        return None
    rest = doc[found[0].end() :]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def strip_fences(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def example_block(raw: str) -> str | None:
    blocks = re.findall(r"```markdown\n(.*?)```", raw, flags=re.S)
    if len(blocks) != 1:
        return None
    return blocks[0]


def split_example(block: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current: str | None = None
    buf: list[str] = []
    for line in block.splitlines():
        match = re.match(r"^### (.+?)\s*$", line)
        if match:
            if current is not None:
                sections.append((current, "\n".join(buf).strip()))
            current = match.group(1)
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections.append((current, "\n".join(buf).strip()))
    return sections


def check_example(form: dict, raw: str, errors: list[str]) -> None:
    block = example_block(raw)
    if block is None:
        errors.append(f"{form['file']}: o tipo precisa de um bloco ```markdown com o exemplo")
        return
    got = split_example(block)
    expected = [section["label"] for section in form["sections"]]
    headings = [label for label, _ in got]
    if headings != expected:
        errors.append(
            f"{form['file']}: cabeçalhos do exemplo {headings!r} != {expected!r}"
        )
        return
    for section, (_, value) in zip(form["sections"], got):
        label = section["label"]
        if section["options"] is not None:
            allowed = list(section["options"])
            if not section["required"]:
                allowed.append(EMPTY_DROPDOWN)
            if value not in allowed:
                errors.append(
                    f"{form['file']}: exemplo de {label!r} tem {value!r}; "
                    f"vale uma opção ou, se for opcional, {EMPTY_DROPDOWN}"
                )
        elif section["required"] and value in ("", EMPTY_TEXT, EMPTY_DROPDOWN):
            errors.append(f"{form['file']}: exemplo obrigatório vazio em {label!r}")


def check_form(doc: str, form: dict, errors: list[str]) -> int | None:
    raw = raw_section(doc, form["name"])
    if raw is None:
        errors.append(f"{form['file']}: seção '## {form['name']}' ausente ou duplicada")
        return None
    if form["chooser"] not in raw:
        errors.append(f"{form['file']}: texto do seletor ausente: {form['chooser']}")
    for section in form["sections"]:
        description = section["description"]
        if description and description not in doc:
            errors.append(f"{form['file']}: descrição ausente: {description}")

    body = strip_fences(raw)
    lines = body.splitlines()
    title_line = next((ln for ln in lines if ln.startswith("**Título padrão:**")), None)
    if title_line is None:
        errors.append(f"{form['file']}: linha de título padrão ausente")
    elif backticks(title_line) != [form["title"]]:
        errors.append(
            f"{form['file']}: título {backticks(title_line)!r} != {form['title']!r}"
        )

    label_line = next((ln for ln in lines if ln.startswith("**Labels:**")), None)
    if label_line is None:
        errors.append(f"{form['file']}: linha de labels ausente")
    elif backticks(label_line) != form["labels"]:
        errors.append(
            f"{form['file']}: labels {backticks(label_line)!r} != {form['labels']!r}"
        )

    items: list[tuple[re.Match[str], int]] = []
    for index, line in enumerate(lines):
        match = ITEM_RE.match(line)
        if match:
            items.append((match, index))
    if len(items) != len(form["sections"]):
        errors.append(
            f"{form['file']}: {len(items)} seções em ISSUES.md, "
            f"{len(form['sections'])} no formulário"
        )
    for position, ((match, index), section) in enumerate(
        zip(items, form["sections"]), start=1
    ):
        number, label, required, tail = (
            int(match.group(1)),
            match.group(2),
            match.group(3),
            match.group(4) or "",
        )
        if number != position:
            errors.append(f"{form['file']}: numeração {number} na posição {position}")
        if label != section["label"]:
            errors.append(f"{form['file']}: título {label!r} != {section['label']!r}")
        expect = "obrigatória" if section["required"] else "opcional"
        if required != expect:
            errors.append(f"{form['file']}: {label!r} está {required}, esperado {expect}")
        if section["options"] is not None:
            found = backticks(tail)
            if found != section["options"]:
                errors.append(
                    f"{form['file']}: opções de {label!r}: {found!r} != {section['options']!r}"
                )
        elif "Opções:" in tail:
            errors.append(f"{form['file']}: {label!r} cita opções e não é dropdown")
        if section["default"] is not None:
            chosen = section["options"][section["default"]]
            follow = ""
            for line in lines[index + 1 :]:
                if line.strip():
                    follow = line
                    break
            if chosen not in follow:
                errors.append(
                    f"{form['file']}: pré-seleção de {label!r} deveria citar {chosen!r}"
                )

    check_example(form, raw, errors)
    return doc.index(f"## {form['name']}")


def check_config(doc: str, errors: list[str]) -> None:
    data = yaml.safe_load((TEMPLATE_DIR / "config.yml").read_text(encoding="utf-8"))
    for link in data["contact_links"]:
        for key in ("name", "url", "about"):
            if link[key] not in doc:
                errors.append(f"config.yml: {key} ausente em ISSUES.md: {link[key]}")


def main() -> int:
    if not ISSUES_PATH.is_file():
        print("ISSUES.md ausente na raiz.", file=sys.stderr)
        return 1
    doc = ISSUES_PATH.read_text(encoding="utf-8")
    errors: list[str] = []
    positions: list[int] = []
    for filename in FORMS:
        form = load_form(TEMPLATE_DIR / filename)
        position = check_form(doc, form, errors)
        if position is not None:
            positions.append(position)
    if positions != sorted(positions):
        errors.append("A ordem dos tipos em ISSUES.md não segue o seletor.")
    check_config(doc, errors)
    if EMPTY_TEXT not in doc:
        errors.append("ISSUES.md não cita _No response_.")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("ISSUES.md confere com os formulários.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
