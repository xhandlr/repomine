from .complexity import analyze_complexity
from .dependencies import analyze_circular_dependencies
from .duplication import analyze_duplication

def run_all(path: str) -> dict:
    return {
        "duplication": analyze_duplication(path),
        "dependencies": analyze_circular_dependencies(path),
        "complexity": analyze_complexity(path),
    }
