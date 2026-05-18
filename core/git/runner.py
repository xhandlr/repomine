from .classifier import classify_all, type_distribution
from .extractor import extract
from .metrics import activity_by_hour, bus_factor, hotspots, summary


def run_all(repo: str) -> dict:
    """Run all git analyses on a repo path or public URL."""
    commits = extract(repo)
    return {
        "summary": summary(commits),
        "hotspots": hotspots(commits),
        "activity_by_hour": activity_by_hour(commits),
        "bus_factor": bus_factor(commits),
        "commit_types": type_distribution(commits),
        "commits": classify_all(commits),
    }
