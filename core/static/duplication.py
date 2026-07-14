import subprocess
import json

def analyze_duplication(path: str, output_dir: str = "jscpd-report") -> dict[str, list[str]]:
    subprocess.run(["npx", "jscpd", path, "--reporters", "json", "--output", output_dir], check=True)
    with open(f"{output_dir}/jscpd-report.json") as file:
        data = json.load(file)
    # Obtener el porcentaje total de duplicación
    total_percentage = data["statistics"]["total"]["percentage"]
    # Obtener los nombres de los archivos duplicados en una lista
    name_duplication_files = []
    for file in data["duplicates"]:
        name_duplication_files.append(file["firstFile"]["name"])
        name_duplication_files.append(file["secondFile"]["name"])
    result = {"total_percentaje": total_percentage, "name_duplication_files": name_duplication_files}
    return result

if __name__ == "__main__":
    print(analyze_duplication("."))
