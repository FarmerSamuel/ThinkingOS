#!/usr/bin/env python3
"""Dependency-free structural validator for the ThinkingOS repository."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:  # Dependency-free local validation remains supported.
    jsonschema = None

try:
    import yaml
except ImportError:  # CI installs requirements-dev.txt for complete YAML validation.
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SKILL_FILES = {
    "README.md", "metadata.yaml", "skill.json", "workflow.md", "validation.md",
    "evaluation.md", "rubric.md", "examples.md", "tests.md", "references.md", "CHANGELOG.md",
}


def parse_registry() -> dict[str, dict]:
    text = (ROOT / "skills" / "registry.yaml").read_text(encoding="utf-8")
    blocks = re.split(r"(?m)(?=^  - id: )", text)
    result = {}
    for block in blocks:
        match = re.match(r"  - id: ([a-z0-9-]+)\n", block)
        if not match:
            continue
        skill_id = match.group(1)
        status = re.search(r"(?m)^    status: ([a-z-]+)$", block)
        version = re.search(r"(?m)^    version: ([0-9A-Za-z.-]+)$", block)
        dep_section = re.search(r"(?ms)^    dependencies:(.*?)(?=^    produces:)", block)
        dependencies = re.findall(r"(?m)^      - ([a-z0-9-]+)$", dep_section.group(1) if dep_section else "")
        result[skill_id] = {
            "status": status.group(1) if status else None,
            "version": version.group(1) if version else None,
            "dependencies": dependencies,
        }
    return result


def validate_graph(registry: dict[str, dict], errors: list[str]) -> None:
    for skill_id, entry in registry.items():
        for dependency in entry["dependencies"]:
            if dependency not in registry:
                errors.append(f"registry: {skill_id} has unknown dependency {dependency}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(skill_id: str) -> None:
        if skill_id in visiting:
            errors.append(f"registry: dependency cycle at {skill_id}")
            return
        if skill_id in visited:
            return
        visiting.add(skill_id)
        for dependency in registry[skill_id]["dependencies"]:
            if dependency in registry:
                visit(dependency)
        visiting.remove(skill_id)
        visited.add(skill_id)

    for skill_id in registry:
        visit(skill_id)


def metadata_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}: (.+)$", text)
    return match.group(1).strip() if match else None


def validate_skill(directory: Path, registry: dict[str, dict], schema: dict, errors: list[str]) -> None:
    skill_id = directory.name
    missing_files = REQUIRED_SKILL_FILES - {p.name for p in directory.iterdir() if p.is_file()}
    if missing_files:
        errors.append(f"{skill_id}: missing files {sorted(missing_files)}")
        return
    try:
        data = json.loads((directory / "skill.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        errors.append(f"{skill_id}: invalid skill.json: {exc}")
        return
    required = set(schema["required"])
    allowed = set(schema["properties"])
    if missing := required - set(data):
        errors.append(f"{skill_id}: missing skill.json fields {sorted(missing)}")
    if extra := set(data) - allowed:
        errors.append(f"{skill_id}: unexpected skill.json fields {sorted(extra)}")
    if data.get("name") != skill_id:
        errors.append(f"{skill_id}: skill.json name mismatch")
    if jsonschema is not None:
        for violation in jsonschema.Draft202012Validator(schema).iter_errors(data):
            location = ".".join(str(part) for part in violation.absolute_path) or "<root>"
            errors.append(f"{skill_id}: schema violation at {location}: {violation.message}")
    if not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?", data.get("version", "")):
        errors.append(f"{skill_id}: invalid semantic version")
    for field in ("thinkingElements", "requiredInputs", "validation", "logic", "conversationRules", "neverRules", "examples", "tests"):
        if not isinstance(data.get(field), list) or not data[field]:
            errors.append(f"{skill_id}: {field} must be a non-empty array")
    if len(data.get("tests", [])) < 5:
        errors.append(f"{skill_id}: skill.json must include at least five contract tests")
    documented_tests = len(re.findall(r"(?m)^\| [A-Z][A-Z0-9]*-[0-9]{2,3} \|", (directory / "tests.md").read_text(encoding="utf-8")))
    if documented_tests < 10:
        errors.append(f"{skill_id}: tests.md has fewer than ten cases")
    metadata = (directory / "metadata.yaml").read_text(encoding="utf-8")
    for field in ("id", "name", "version", "status", "category", "author", "requires", "produces", "dependencies", "nextSkill"):
        if not re.search(rf"(?m)^{field}:", metadata):
            errors.append(f"{skill_id}: metadata missing {field}")
    if metadata_value(metadata, "id") != skill_id:
        errors.append(f"{skill_id}: metadata id mismatch")
    if metadata_value(metadata, "version") != data.get("version"):
        errors.append(f"{skill_id}: metadata/skill version mismatch")
    if skill_id not in registry:
        errors.append(f"{skill_id}: not registered")
    elif metadata_value(metadata, "status") != registry[skill_id]["status"]:
        errors.append(f"{skill_id}: metadata/registry status mismatch")
    elif data.get("version") != registry[skill_id]["version"]:
        errors.append(f"{skill_id}: skill/registry version mismatch")


def validate_project_version(errors: list[str]) -> None:
    version_file = ROOT / "VERSION"
    if not version_file.exists():
        return
    version = version_file.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version):
        errors.append("VERSION: invalid stable semantic version")
        return
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    sdk = (ROOT / "thinkingos" / "__init__.py").read_text(encoding="utf-8")
    if not re.search(rf'(?m)^version = "{re.escape(version)}"$', pyproject):
        errors.append("VERSION: pyproject.toml version mismatch")
    if not re.search(rf'(?m)^__version__ = "{re.escape(version)}"$', sdk):
        errors.append("VERSION: SDK version mismatch")
    if not re.search(rf"(?m)^## \[{re.escape(version)}\]", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")):
        errors.append("VERSION: CHANGELOG.md release entry missing")


def validate_docs(errors: list[str]) -> None:
    docs = ROOT / "docs"
    config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8") if (ROOT / "mkdocs.yml").exists() else ""
    default_docs = {path.name for path in docs.glob("*.md") if not path.name.endswith(".zh.md")}
    localized_docs = {path.name.removesuffix(".zh.md") + ".md" for path in docs.glob("*.zh.md")}
    for missing in sorted(default_docs - localized_docs):
        errors.append(f"docs i18n: missing Traditional Chinese counterpart for {missing}")
    for orphan in sorted(localized_docs - default_docs):
        errors.append(f"docs i18n: localized page has no English source {orphan}")
    for nav_path in re.findall(r"(?m)^\s+- [^:\n]+: ([a-z0-9][a-z0-9./-]*\.md)$", config):
        if not (docs / nav_path).exists():
            errors.append(f"mkdocs nav: missing docs/{nav_path}")
    link_pattern = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)#]+)(?:#[^)]+)?\)")
    for document in docs.rglob("*.md"):
        text = document.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            resolved = (document.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{document.relative_to(ROOT)}: broken relative link {target}")


def validate_yaml(errors: list[str]) -> None:
    if yaml is None:
        return
    candidates = [ROOT / "skills" / "registry.yaml"]
    candidates.extend((ROOT / "skills").glob("*/metadata.yaml"))
    candidates.extend((ROOT / ".github").rglob("*.yml"))
    candidates.extend((ROOT / ".github").rglob("*.yaml"))
    for path in sorted(set(candidates)):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid YAML: {exc}")


def main() -> int:
    errors: list[str] = []
    registry = parse_registry()
    validate_graph(registry, errors)
    validate_project_version(errors)
    validate_docs(errors)
    validate_yaml(errors)
    schema = json.loads((ROOT / "schemas" / "skill.schema.json").read_text(encoding="utf-8"))
    for directory in sorted((ROOT / "skills").iterdir()):
        if directory.is_dir():
            validate_skill(directory, registry, schema, errors)
    for schema_file in sorted((ROOT / "schemas").glob("*.json")):
        try:
            schema_data = json.loads(schema_file.read_text(encoding="utf-8"))
            if jsonschema is not None:
                jsonschema.Draft202012Validator.check_schema(schema_data)
        except json.JSONDecodeError as exc:
            errors.append(f"{schema_file.relative_to(ROOT)}: invalid JSON: {exc}")
        except Exception as exc:  # jsonschema raises schema-specific subclasses.
            errors.append(f"{schema_file.relative_to(ROOT)}: invalid JSON Schema: {exc}")
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    mode = "full" if jsonschema is not None and yaml is not None else "dependency-free"
    print(f"Repository validation passed ({mode}): {len(registry)} registered skills, dependency graph acyclic.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
