import subprocess
import json

def analyze_circular_dependencies(path: str):
    result = subprocess.run(
        ["npx", "madge", "--circular", "--json", path],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)
    return {
        "total_circular_dependencies": len(data),
        "circular_dependencies": data
    }
