from collections import Counter
import subprocess
import json

def analyze_duplication(path: str, output_dir: str = "jscpd-report") -> dict:
    subprocess.run(["npx", "jscpd", path, "--reporters", "json", "--output", output_dir], check=True)
    with open(f"{output_dir}/jscpd-report.json") as file:
        data = json.load(file)

    # Obtener el porcentaje total de duplicación
    total_percentage = get_total_percentage(data)

    # Contar el total de archivos duplicados
    total_duplicate_filenames = count_duplicate_filenames(data)

    # Obtener las líneas totales duplicadas
    total_duplicate_lines = get_duplicate_lines(data)

    # Top n de archivos duplicados
    most_duplicated_files = get_most_duplicated_files(data)

    result = {
        "total_percentage": total_percentage,
        "total_duplicate_filenames": total_duplicate_filenames,
        "total_duplicate_lines": total_duplicate_lines,
        "top_duplicate_files": most_duplicated_files
    }
    return result

def get_duplicate_filenames(data: dict) -> list[str]:
    duplicate_filenames = []
    for file in data["duplicates"]:
        duplicate_filenames.append(file["firstFile"]["name"])
        duplicate_filenames.append(file["secondFile"]["name"])
    return duplicate_filenames

def get_total_percentage(data: dict) -> float:
    return data["statistics"]["total"]["percentage"]

def count_duplicate_filenames(data: dict):
    return len(data["duplicates"])

def get_duplicate_lines(data: dict):
    return data["statistics"]["total"]["duplicatedLines"]

def get_most_duplicated_files(data: dict, top_n = 10):
    duplicate_filenames = get_duplicate_filenames(data)
    counts = Counter(duplicate_filenames)
    return [
        {"filename": filename, "times": count}
        for filename, count in counts.most_common(top_n)
    ]

if __name__ == "__main__":
    print(analyze_duplication("/home/cadel/Escritorio/gestor-practicas"))
