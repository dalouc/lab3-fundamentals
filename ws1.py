from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import requests

URL = (
    "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ei_bsco_m"
    "?format=JSON&lang=en&indic=BS-CSMCI&s_adj=SA&unit=BAL"
)

EU = "EU27_2020"
SPAIN = "ES"
LAST_5_YEARS = (2021, 2022, 2023, 2024, 2025)
MONTHS = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)
FIGURES = Path("figures")


def bar_chart(
    labels: tuple[str, ...], values: list[float], title: str, name: str
) -> None:
    figure, axes = plt.subplots(figsize=(8, 4.5))
    axes.bar(labels, values, color="steelblue")
    axes.axhline(0, color="black", linewidth=0.8)
    axes.set_title(title)
    axes.set_ylabel("Balance")
    figure.tight_layout()
    FIGURES.mkdir(exist_ok=True)
    figure.savefig(FIGURES / name)


def report(title: str, labels: tuple[str, ...], values: list[float]) -> None:
    print(f"\n{title}")
    for label, value in zip(labels, values, strict=True):
        print(f"  {label}  {value:6.1f}")


def main() -> None:
    answer = requests.get(URL, timeout=60)
    answer.raise_for_status()
    dataset: dict[str, Any] = answer.json()

    months: dict[str, int] = dataset["dimension"]["time"]["category"]["index"]
    places: dict[str, int] = dataset["dimension"]["geo"]["category"]["index"]
    cells: dict[str, float] = dataset["value"]
    series: dict[str, dict[str, float]] = {}
    for geo in (EU, SPAIN):
        first = places[geo] * len(months)
        series[geo] = {
            month: cells[str(first + position)]
            for month, position in months.items()
            if str(first + position) in cells
        }
    eu = series[EU]
    spain = series[SPAIN]

    years = tuple(str(year) for year in LAST_5_YEARS)
    eu_by_year: list[float] = []
    for year in years:
        balances = [value for month, value in eu.items() if month[:4] == year]
        eu_by_year.append(sum(balances) / len(balances))

    months_2024 = [f"2024-{number:02d}" for number in range(1, 13)]
    eu_2024 = [eu[month] for month in months_2024]
    spain_2024 = [spain[month] for month in months_2024]

    report("Average EU consumer confidence, last 5 years", years, eu_by_year)
    report("Average EU consumer confidence, 2024", MONTHS, eu_2024)
    report("Average Spanish consumer confidence, 2024", MONTHS, spain_2024)

    bar_chart(
        years,
        eu_by_year,
        "Average EU consumer confidence (2021-2025)",
        "ws1_eu_by_year.png",
    )
    bar_chart(
        MONTHS, eu_2024, "Average EU consumer confidence (2024)", "ws1_eu_by_month.png"
    )
    bar_chart(
        MONTHS,
        spain_2024,
        "Average Spanish consumer confidence (2024)",
        "ws1_spain_by_month.png",
    )
    plt.show()


if __name__ == "__main__":
    main()
