from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import requests

SERVICE = "https://api.idescat.cat/onomastica/v1/nadons/dades.json"
MARIA = "40683"
YEARS = ["2021", "2022", "2023", "2024", "2025"]
TOP = 10
CHARTS = Path("figures")


def main() -> None:
    reply = requests.get(
        SERVICE, params={"id": MARIA, "class": "t", "lang": "en"}, timeout=60
    )
    reply.raise_for_status()
    yearly: dict[str, Any] = reply.json()
    by_year = {
        entry["c"]: entry
        for entry in yearly["onomastica_nadons"]["ff"]["f"]
        if entry["c"] in YEARS
    }

    total_rank = [int(by_year[year]["rank"]["total"]) for year in YEARS]
    female_rank = [int(by_year[year]["rank"]["sex"]) for year in YEARS]
    frequency = [int(by_year[year]["pos1"]["v"]) for year in YEARS]
    per_thousand = [float(by_year[year]["pos1"]["w"]["total"]) for year in YEARS]
    per_thousand_female = [float(by_year[year]["pos1"]["w"]["sex"]) for year in YEARS]

    figures = [
        ("Rank of MARIA among all newborns", "Rank", total_rank, "ws2_rank_total.png"),
        (
            "Rank of MARIA among newborn girls",
            "Rank",
            female_rank,
            "ws2_rank_female.png",
        ),
        ("Newborn girls named MARIA", "Girls", frequency, "ws2_frequency.png"),
        (
            "MARIA per thousand newborns",
            "Per thousand",
            per_thousand,
            "ws2_per_thousand.png",
        ),
        (
            "MARIA per thousand newborn girls",
            "Per thousand",
            per_thousand_female,
            "ws2_per_thousand_female.png",
        ),
    ]

    print("Year   Rank  Rank(F)  Girls  Per 1000  Per 1000 (F)")
    for position, year in enumerate(YEARS):
        print(
            f"{year}  {total_rank[position]:5d}  {female_rank[position]:7d}"
            f"  {frequency[position]:5d}  {per_thousand[position]:8.2f}"
            f"  {per_thousand_female[position]:12.2f}"
        )

    CHARTS.mkdir(exist_ok=True)
    for title, ylabel, values, filename in figures:
        plt.figure(figsize=(7, 4))
        plt.bar(YEARS, values, color="darkred")
        plt.title(f"{title} ({YEARS[0]}-{YEARS[-1]})")
        plt.xlabel("Year")
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.savefig(CHARTS / filename)

    reply = requests.get(
        SERVICE, params={"id": MARIA, "class": "com", "lang": "en"}, timeout=60
    )
    reply.raise_for_status()
    by_county: dict[str, Any] = reply.json()
    counties: list[tuple[int, str]] = [
        (int(entry["pos1"]["v"]), entry["c"]["content"])
        for entry in by_county["onomastica_nadons"]["ff"]["f"]
        if entry["c"] != "Total" and entry["pos1"]["v"].isdigit()
    ]
    counties.sort(reverse=True)
    births, winner = counties[0]
    print(
        f"\nMost MARIAs were born in {winner} ({births} girls, latest year available)"
    )

    plt.figure(figsize=(7, 5))
    plt.barh(
        [name for _, name in counties[:TOP]][::-1],
        [number for number, _ in counties[:TOP]][::-1],
        color="darkred",
    )
    plt.title(f"Counties with more newborn MARIAs (top {TOP})")
    plt.xlabel("Girls named MARIA")
    plt.tight_layout()
    plt.savefig(CHARTS / "ws2_counties.png")

    plt.show()


if __name__ == "__main__":
    main()
