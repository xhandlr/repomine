import json
import csv
from pathlib import Path
from enum import Enum

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

from core.git.runner import run_all

app = typer.Typer(help="repomine — análisis de repositorios git")
console = Console()


class Framework(str, Enum):
    nestjs  = "nestjs"
    angular = "angular"
    react   = "react"
    generic = "generic"


class OutputFormat(str, Enum):
    json = "json"
    csv  = "csv"


@app.command()
def analyze(
    repo: str = typer.Argument(..., help="Path local o URL pública del repositorio"),
    framework: Framework = typer.Option(Framework.generic, "--framework", "-f", help="Framework principal"),
    output: Path | None = typer.Option(None, "--output", "-o", help="Exportar resultados (ej: report.json, report.csv)"),
):
    """Analiza un repositorio y muestra sus métricas."""

    console.print(Panel.fit("[bold cyan]repomine[/bold cyan]  v0.1.0", box=box.ROUNDED))
    console.print()

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task(f"Analizando [bold]{repo}[/bold]...", total=None)
        result = run_all(repo)
        progress.update(task, description="[green]✔[/green] Análisis completado")

    console.print()
    _print_summary(result["summary"])
    _print_hotspots(result["hotspots"])
    _print_commit_types(result["commit_types"])
    _print_bus_factor(result["bus_factor"])
    _print_peak_hour(result["activity_by_hour"])

    if output:
        _export(result, output)
        console.print(f"\n[green]✔[/green] Exportado en [bold]{output}[/bold]")


def _print_summary(s: dict) -> None:
    table = Table(title="Resumen", box=box.ROUNDED, show_header=False)
    table.add_column(style="dim")
    table.add_column()
    table.add_row("Total commits",    str(s.get("total_commits", "-")))
    table.add_row("Autores",          str(s.get("total_authors", "-")))
    table.add_row("Archivos tocados", str(s.get("total_files_touched", "-")))
    table.add_row("Primer commit",    s.get("first_commit", "-")[:10])
    table.add_row("Último commit",    s.get("last_commit", "-")[:10])
    console.print(table)
    console.print()


def _print_hotspots(hotspots: list[dict]) -> None:
    table = Table(title="Hotspots — archivos más modificados", box=box.ROUNDED)
    table.add_column("Archivo", style="cyan")
    table.add_column("Modificaciones", justify="right")
    for h in hotspots[:10]:
        table.add_row(h["file"], str(h["modifications"]))
    console.print(table)
    console.print()


def _print_commit_types(types: dict[str, int]) -> None:
    table = Table(title="Tipos de commits", box=box.ROUNDED)
    table.add_column("Tipo", style="magenta")
    table.add_column("Total", justify="right")
    for t, n in sorted(types.items(), key=lambda x: -x[1]):
        table.add_row(t, str(n))
    console.print(table)
    console.print()


def _print_bus_factor(bf: dict) -> None:
    factor = bf.get("bus_factor", 0)
    color = "red" if factor <= 2 else "yellow" if factor <= 4 else "green"
    console.print(Panel(
        f"[{color}]Bus Factor: {factor}[/{color}]\n"
        + ("[red]⚠  Conocimiento concentrado en pocas personas[/red]" if factor <= 2
           else "[green]✔  Conocimiento bien distribuido[/green]"),
        title="Bus Factor",
        box=box.ROUNDED,
    ))
    console.print()


def _print_peak_hour(activity: dict[int, int]) -> None:
    peak = max(activity, key=activity.get)
    console.print(f"[dim]Hora más activa:[/dim] [bold]{peak}:00[/bold] ({activity[peak]} commits)\n")


def _export(result: dict, path: Path) -> None:
    if path.suffix == ".csv":
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["hash", "author", "date", "type", "message"])
            writer.writeheader()
            writer.writerows(result["commits"])
    else:
        with open(path, "w") as f:
            json.dump(result, f, indent=2, default=str)


if __name__ == "__main__":
    app()
