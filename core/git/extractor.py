from dataclasses import dataclass, field
from datetime import datetime
from pydriller import Repository


@dataclass
class CommitRecord:
    hash: str
    message: str
    author: str
    co_authors: list[str]
    date: datetime
    files: list[str]
    lines_added: int
    lines_deleted: int


def extract(repo: str) -> list[CommitRecord]:
    """Extract all commits from a local path or public URL."""
    records = []
    for commit in Repository(repo).traverse_commits():
        records.append(CommitRecord(
            hash=commit.hash,
            message=commit.msg,
            author=commit.author.name,
            co_authors=_parse_co_authors(commit.msg),
            date=commit.author_date,
            files=[f.filename for f in commit.modified_files],
            lines_added=sum(f.added_lines for f in commit.modified_files),
            lines_deleted=sum(f.deleted_lines for f in commit.modified_files),
        ))
    return records


def _parse_co_authors(message: str) -> list[str]:
    co_authors = []
    for line in message.splitlines():
        if line.lower().startswith("co-authored-by:"):
            name = line.split(":", 1)[1].strip()
            if "<" in name:
                name = name[:name.index("<")].strip()
            co_authors.append(name)
    return co_authors
