#!/usr/bin/env python3

import os
import argparse
import pandas as pd
from datetime import datetime, timedelta

INPUT_FILE = "/data/raw_data/favorita-grocery-sales-forecasting/train.csv"
OUTPUT_DIR = "/data/raw_data/favorita-grocery-sales-forecasting/weeks"
CHUNK_SIZE = 1_000_000

def parse_args():
    parser = argparse.ArgumentParser(description="Split train.csv by week.")
    parser.add_argument("--overview", action="store_true", help="Show data overview.")
    parser.add_argument("--all", action="store_true", help="Split all data into weekly files.")
    parser.add_argument("--from", dest="from_date", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--to", dest="to_date", type=str, help="End date (YYYY-MM-DD)")
    parser.add_argument("--year", type=int, help="Target year for weekly splitting.")
    parser.add_argument("--start-week", type=int, default=1, help="Start week number (ISO, default: 1)")
    parser.add_argument("--weeks", type=int, help="Number of weeks to extract from --start-week")
    return parser.parse_args()

def load_dates_only():
    print("Scanning dataset for date overview...")
    dates = pd.read_csv(INPUT_FILE, usecols=["date"], parse_dates=["date"])
    min_date = dates["date"].min()
    max_date = dates["date"].max()
    delta = max_date - min_date
    print("\n📊 Dataset Overview:")
    print(f"- Oldest date : {min_date.date()}")
    print(f"- Newest date : {max_date.date()}")
    print(f"- Total days  : {delta.days + 1}")
    print(f"- Total weeks : {(delta.days + 1) // 7}")
    print(f"- Total years : {delta.days / 365:.2f}\n")
    return min_date, max_date

def iso_week_key(date):
    return date.strftime("%Y-W%V")  # ISO week key like 2016-W01

def get_monday_of_iso_week(year, week):
    return datetime.strptime(f'{year}-W{int(week):02d}-1', "%G-W%V-%u")  # Monday of ISO week

def split_weeks(start=None, end=None):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    week_buckets = {}

    print(f"📦 Splitting data from {start.date() if start else 'START'} to {end.date() if end else 'END'}")

    for chunk in pd.read_csv(INPUT_FILE, parse_dates=["date"], chunksize=CHUNK_SIZE):
        if start:
            chunk = chunk[chunk["date"] >= start]
        if end:
            chunk = chunk[chunk["date"] <= end]
        if chunk.empty:
            continue

        chunk["week_key"] = chunk["date"].apply(iso_week_key)
        for week, group in chunk.groupby("week_key"):
            if week not in week_buckets:
                week_buckets[week] = []
            week_buckets[week].append(group)

    print(f"📝 Writing weekly files to: {OUTPUT_DIR}")
    for week, dfs in sorted(week_buckets.items()):
        week_df = pd.concat(dfs)
        week_df.drop(columns=["week_key"], inplace=True)
        file_path = os.path.join(OUTPUT_DIR, f"train_{week}.csv")
        week_df.to_csv(file_path, index=False)
        print(f"✅ Saved {file_path} — {len(week_df)} rows")

def split_by_year_weeks(year, start_week, num_weeks):
    start_date = get_monday_of_iso_week(year, start_week)
    end_date = start_date + timedelta(weeks=num_weeks) - timedelta(days=1)
    print(f"🗓️ Splitting {num_weeks} week(s) starting from Week {start_week}, {year}")
    print(f"From {start_date.date()} to {end_date.date()}")
    split_weeks(start=start_date, end=end_date)

def main():
    args = parse_args()

    if args.overview:
        load_dates_only()
        return

    if args.year and args.weeks:
        split_by_year_weeks(args.year, args.start_week, args.weeks)
        return

    from_date = pd.to_datetime(args.from_date) if args.from_date else None
    to_date = pd.to_datetime(args.to_date) if args.to_date else None

    if args.all or (from_date and to_date):
        split_weeks(start=from_date, end=to_date)
    else:
        print("❗ No valid option provided. Use one of:")
        print("   --overview                         Show dataset summary")
        print("   --all                              Split full dataset by week")
        print("   --from DATE --to DATE              Split only specific date range")
        print("   --year YYYY --weeks N              Split N weeks from ISO Week 1")
        print("   --year YYYY --start-week W --weeks N  Start from ISO Week W")

if __name__ == "__main__":
    main()
