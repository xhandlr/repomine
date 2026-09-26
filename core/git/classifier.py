from collections import Counter

from .extractor import CommitRecord

# Conventional Commits types mapped to their keyword prefixes (English + Spanish)
_TYPES: dict[str, set[str]] = {
    "feat":     {"feat", "feature",
                 "agregado", "agregada", "agregados", "agregadas", "agrega", "agregar",
                 "nuevo", "nueva", "implementado", "implementada", "implementa", "implementar"},
    "fix":      {"fix", "bug", "hotfix", "patch", "defect", "error", "crash",
                 "arreglado", "arreglada", "arregla", "arreglar",
                 "corregido", "corregida", "corrige", "corregir",
                 "soluciona", "solucionado"},
    "refactor": {"refactor", "restructure",
                 "reestructura", "reestructurado", "reestructurada", "refactoriza", "refactorizado"},
    "chore":    {"chore", "bump", "update", "upgrade", "deps",
                 "actualizado", "actualizada", "actualiza", "actualizar",
                 "eliminado", "eliminada", "elimina", "eliminar"},
    "docs":     {"docs", "doc", "documentation", "documentacion", "documentación"},
    "test":     {"test", "tests", "spec", "prueba", "pruebas"},
    "perf":     {"perf", "performance", "optimize", "optimise", "optimizado", "optimizada", "optimiza"},
    "ci":       {"ci", "cd", "pipeline", "workflow", "github-actions"},
    "style":    {"style", "format", "lint", "whitespace", "formato"},
    "revert":   {"revert", "revertido", "revertida", "revierte"},
}


def classify(message: str) -> str:
    """Classify a commit message using Conventional Commits types."""
    first_line = message.splitlines()[0].lower() if message else ""

    # Try to extract the conventional commit prefix: "type(scope): ..."
    prefix = first_line.split("(")[0].split(":")[0].strip()
    for commit_type, keywords in _TYPES.items():
        if prefix in keywords:
            return commit_type

    # Fall back: check all words in the first line
    words = set(first_line.replace(":", " ").replace("(", " ").replace(")", " ").split())
    for commit_type, keywords in _TYPES.items():
        if words & keywords:
            return commit_type

    return "unknown"


def classify_all(commits: list[CommitRecord]) -> list[dict]:
    return [
        {
            "hash": c.hash[:8],
            "author": c.author,
            "date": c.date.isoformat(),
            "type": classify(c.message),
            "message": c.message.splitlines()[0][:100],
        }
        for c in commits
    ]


def type_distribution(commits: list[CommitRecord]) -> dict[str, int]:
    return dict(Counter(classify(c.message) for c in commits))
