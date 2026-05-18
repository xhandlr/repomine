from collections import Counter

from .extractor import CommitRecord

# Conventional Commits types mapped to their keyword prefixes
_TYPES: dict[str, set[str]] = {
    "feat":     {"feat", "feature"},
    "fix":      {"fix", "bug", "hotfix", "patch", "defect", "error", "crash"},
    "refactor": {"refactor", "restructure"},
    "chore":    {"chore", "bump", "update", "upgrade", "deps"},
    "docs":     {"docs", "doc", "documentation"},
    "test":     {"test", "tests", "spec"},
    "perf":     {"perf", "performance", "optimize", "optimise"},
    "ci":       {"ci", "cd", "pipeline", "workflow", "github-actions"},
    "style":    {"style", "format", "lint", "whitespace"},
    "revert":   {"revert"},
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
