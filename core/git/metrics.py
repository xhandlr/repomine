from collections import Counter, defaultdict

from .extractor import CommitRecord


def summary(commits: list[CommitRecord]) -> dict:
    if not commits:
        return {}
    dates = [c.date for c in commits]
    return {
        "total_commits": len(commits),
        "total_authors": len({c.author for c in commits}),
        "authors": sorted({c.author for c in commits}),
        "first_commit": min(dates).isoformat(),
        "last_commit": max(dates).isoformat(),
        "total_files_touched": len({f for c in commits for f in c.files}),
    }


def hotspots(commits: list[CommitRecord], top_n: int = 20) -> list[dict]:
    """Files ranked by number of times they were modified."""
    counts = Counter(f for c in commits for f in c.files)
    return [
        {"file": file, "modifications": count}
        for file, count in counts.most_common(top_n)
    ]


def activity_by_hour(commits: list[CommitRecord]) -> dict[int, int]:
    """Commit count per hour of day (0–23)."""
    counts = Counter(c.date.hour for c in commits)
    return {hour: counts.get(hour, 0) for hour in range(24)}


def bus_factor(commits: list[CommitRecord]) -> dict:
    """
    Minimum number of authors whose removal would leave
    more than 50% of files with no remaining contributor.
    """
    file_authors: dict[str, set[str]] = defaultdict(set)
    for commit in commits:
        for file in commit.files:
            file_authors[file].add(commit.author)

    total_files = len(file_authors)
    if total_files == 0:
        return {"bus_factor": 0, "authors_ranked": []}

    author_files: dict[str, set[str]] = defaultdict(set)
    for file, authors in file_authors.items():
        for author in authors:
            author_files[author].add(file)

    ranked = sorted(author_files.items(), key=lambda x: len(x[1]), reverse=True)

    covered: set[str] = set()
    factor = 0
    for author, files in ranked:
        covered |= files
        factor += 1
        if len(covered) / total_files >= 0.5:
            break

    return {
        "bus_factor": factor,
        "authors_ranked": [
            {"author": a, "files_owned": len(f)} for a, f in ranked[:10]
        ],
    }
