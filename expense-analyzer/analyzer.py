import csv
import sys
from datetime import datetime
from collections import defaultdict

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8")


def load_expenses(filepath="data/expenses.csv"):
    expenses = []
    with open(filepath, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append({
                "date": datetime.strptime(row["date"], "%Y-%m-%d"),
                "category": row["category"],
                "amount": float(row["amount"]),
                "description": row["description"],
            })
    return expenses


def analyze(expenses):
    total = sum(e["amount"] for e in expenses)

    by_category = defaultdict(float)
    for e in expenses:
        by_category[e["category"]] += e["amount"]

    dates = {e["date"].date() for e in expenses}
    avg_per_day = total / len(dates) if dates else 0

    biggest = max(expenses, key=lambda e: e["amount"])

    return {
        "total": total,
        "by_category": dict(by_category),
        "avg_per_day": avg_per_day,
        "biggest": biggest,
    }


def print_report(stats):
    total = stats["total"]
    by_category = stats["by_category"]
    avg_per_day = stats["avg_per_day"]
    biggest = stats["biggest"]

    print("=" * 40)
    print("       ОТЧЁТ ПО РАСХОДАМ")
    print("=" * 40)
    print()
    print(f"  Всего потрачено: {total:.2f} руб.")
    print(f"  Средний расход в день: {avg_per_day:.2f} руб.")
    print()
    print("  По категориям:")
    sorted_cats = sorted(by_category.items(), key=lambda x: x[1], reverse=True)
    for cat, amount in sorted_cats:
        pct = amount / total * 100
        print(f"    {cat:<16} {amount:>8.2f} руб.  ({pct:.1f}%)")
    print()
    b = biggest
    print(f"  Самая большая трата:")
    print(f"    {b['description']} — {b['amount']:.2f} руб. ({b['date'].strftime('%d.%m.%Y')})")
    print()


if __name__ == "__main__":
    expenses = load_expenses()
    stats = analyze(expenses)
    print_report(stats)
