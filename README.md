# repomine

![Python](https://img.shields.io/badge/python-3.13%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Package manager](https://img.shields.io/badge/package%20manager-uv-de5fe9)

A CLI for mining git repositories: commit history metrics, code quality, and static analysis, in one report.

## Features

**Git mining** (via [PyDriller](https://github.com/ishepard/pydriller))
- Commit summary: total commits, authors, first/last commit, files touched
- Hotspots: files modified most often
- Bus factor: minimum number of authors whose removal would leave over 50% of files with no remaining contributor
- Commit activity by hour of day
- Commit classification by type (feat/fix/refactor/chore/...), with keyword support in both English and Spanish

**Static analysis**
- Code duplication ([jscpd](https://github.com/kucherenko/jscpd))
- Circular dependencies ([madge](https://github.com/pahen/madge))
- Cyclomatic complexity per function ([lizard](https://github.com/terryyin/lizard))

Results are printed to the console and exported as JSON (or CSV) under `results/`.

## Installation

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```
uv sync
```

## Usage

```
uv run repomine <local-path-or-git-url>
```

Options:
- `-o, --output <path>` — export path (default: `results/<repo-name>.json`)
- `-f, --framework <name>` — reserved for future per-framework analysis, not yet implemented

### Sample output

Running `repomine .` against this repo's own history:

```
             Resumen
╭──────────────────┬────────────╮
│ Total commits    │ 23         │
│ Autores          │ 2          │
│ Archivos tocados │ 23         │
╰──────────────────┴────────────╯

 Tipos de commits
╭─────────┬───────╮
│ Tipo    │ Total │
├─────────┼───────┤
│ feat    │    13 │
│ chore   │     6 │
│ fix     │     2 │
│ unknown │     1 │
│ docs    │     1 │
╰─────────┴───────╯

Funciones con mayor complejidad ciclomática
╭─────────────────────────────┬────────────────────┬─────┬──────╮
│ Archivo                     │ Función             │ CCN │ NLOC │
├─────────────────────────────┼────────────────────┼─────┼──────┤
│ ./core/git/metrics.py       │ bus_factor         │   9 │   26 │
│ ./core/git/metrics.py       │ summary            │   7 │   12 │
│ ./core/git/classifier.py    │ classify           │   6 │   11 │
╰─────────────────────────────┴────────────────────┴─────┴──────╯
```

Table labels are in Spanish for now; a language option is planned.

## Roadmap

See [docs/architecture.md](docs/architecture.md) for the full design and roadmap, and the [Issues](https://github.com/xhandlr/repomine/issues) tab for near-term work in progress.

## License

[MIT](LICENSE)
