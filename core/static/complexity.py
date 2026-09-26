import lizard

_EXCLUDE = ["*/node_modules/*", "node_modules/*", "*/dist/*", "dist/*", "*/.git/*", ".git/*"]


def analyze_complexity(path: str, top_n: int = 10) -> dict:
    functions = []
    total_ccn = 0
    total_nloc = 0

    for file in lizard.analyze([path], exclude_pattern=_EXCLUDE):
        total_nloc += file.nloc
        for func in file.function_list:
            total_ccn += func.cyclomatic_complexity
            functions.append({
                "file": func.filename,
                "function": func.name,
                "cyclomatic_complexity": func.cyclomatic_complexity,
                "nloc": func.nloc,
                "line": func.start_line,
            })

    functions.sort(key=lambda f: f["cyclomatic_complexity"], reverse=True)
    total_functions = len(functions)

    return {
        "total_functions": total_functions,
        "total_nloc": total_nloc,
        "average_complexity": round(total_ccn / total_functions, 2) if total_functions else 0,
        "most_complex_functions": functions[:top_n],
    }
