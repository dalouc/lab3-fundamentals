# lab3-web-services

Lab 3 of *Technological Fundamentals in the Big Data World* (Master in Big
Data, UC3M): two Python programs that read open statistical data from REST web
services, summarise it and plot it. They use only `requests` to make the calls
and plain JSON (no `pandas`) to decode the answers.

| Program     | Web service                                      | Question                                                  |
| ----------- | ------------------------------------------------ | --------------------------------------------------------- |
| [`ws1.py`](ws1.py) | [EUROSTAT dissemination API](https://ec.europa.eu/eurostat/web/main/data/web-services) | Consumer confidence in the EU and in Spain |
| [`ws2.py`](ws2.py) | [Idescat Onomastics API](https://www.idescat.cat/dev/api/onomastica/) | Newborns named MARIA in Catalonia |

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --group dev
pre-commit install
```

## Running

```bash
python ws1.py
python ws2.py
```

Each program is self-contained: it makes its own requests, prints every result
as a table and opens the corresponding charts, which are also written as PNG
files to `figures/`.

## Exercise 1 — EUROSTAT

A single GET request to the *Consumer surveys - monthly data* dataset
(`ei_bsco_m`), filtered exactly as the EUROSTAT query builder was configured in
the assignment: indicator `BS-CSMCI` (consumer confidence indicator),
seasonally adjusted (`SA`), expressed as a balance (`BAL`), with time, geo and
unit code left at their default value.

The answer comes back in [JSON-stat 2.0](https://json-stat.org/): a flat
`value` mapping whose keys number the cells of the `freq × indic × s_adj ×
unit × geo × time` cube. Every dimension but `geo` and `time` has a single
category, so `main()` unfolds the mapping into one `month -> value` series
per territory, and the three requested bar charts are built from there:

1. Average EU consumer confidence for each of the last five complete years
   (2021-2025).
2. Average EU consumer confidence for each month of 2024.
3. Average Spanish consumer confidence for each month of 2024.

## Exercise 2 — Idescat

Two requests to the `dades` operation of the `nadons` subservice, for
identifier `40683` — the female given name MARIA. `class=t` returns the yearly
series for Catalonia; `class=com` breaks the latest available year down by
county. Five figures are reported for the last five available years
(2021-2025), each one as a histogram with one bar per year:

1. Total rank of the name among all newborns.
2. Rank of the name among female newborns.
3. Frequency of the name (newborn girls named MARIA).
4. Newborns named MARIA per thousand newborns.
5. Newborns named MARIA per thousand female newborns.

Plus the place where most MARIAs were born, as a bar chart of the ten leading
counties. Idescat breaks these statistics down to provinces, territorial plan
areas and counties only, so the **county** (*comarca*) is the finest
geographical level the service offers. The county answer also carries a
`Total` row for Catalonia, and marks withheld figures with `_`; both are
skipped.

## Layout

```
.
├── authors.txt
├── figures/        # charts written by the programs (generated)
├── pyproject.toml  # dependencies and every tool setting
├── ws1.py          # exercise 1 — EUROSTAT
└── ws2.py          # exercise 2 — Idescat
```

## Everyday commands

| Task             | Command                      |
| ---------------- | ---------------------------- |
| Lint             | `ruff check .`               |
| Lint and autofix | `ruff check --fix .`         |
| Format           | `ruff format .`              |
| Check formatting | `ruff format --check .`      |
| Type-check       | `pyright`                    |
| Run every hook   | `pre-commit run --all-files` |
