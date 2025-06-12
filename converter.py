#!/usr/bin/env python3
"""
CLI-конвертер валют без API-ключей.
Пример:
    python converter.py 150 EUR USD
    → 150.00 EUR = 162.85 USD
"""
from __future__ import annotations
import sys
import requests
from typing import Final

OPEN_API: Final[str] = "https://open.er-api.com/v6/latest/{}"


def get_rate(base: str, target: str) -> float:
    """Возвращает коэффициент base→target. Бросает RuntimeError при ошибке."""
    url = OPEN_API.format(base.upper())
    r = requests.get(url, timeout=10)
    r.raise_for_status()

    data: dict = r.json()
    if data.get("result") != "success":
        raise RuntimeError(data.get("error-type", "API returned non-success"))

    rates: dict = data["rates"]
    try:
        return float(rates[target.upper()])
    except KeyError:
        raise RuntimeError(f"Unknown currency code '{target}'") from None


def main(argv: list[str]) -> None:
    if len(argv) != 4:
        print("Usage: python converter.py <amount> <FROM> <TO>")
        sys.exit(2)

    amt_str, src, dst = argv[1:4]
    try:
        amount = float(amt_str.replace(",", "."))
    except ValueError:
        sys.exit("Amount must be a number")

    try:
        rate = get_rate(src, dst)
        print(f"{amount:.2f} {src.upper()} = {amount * rate:.2f} {dst.upper()}")
    except Exception as e:
        sys.exit(f"Error: {e}")


if __name__ == "__main__":
    main(sys.argv)
