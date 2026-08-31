"""Run official API/RSS importers and refresh verification timestamps for manual data."""
from datetime import date
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "opportunities.db"


def touch_manual_records(conn):
    today = date.today().isoformat()
    for table in ("platforms", "courses", "opportunities"):
        conn.execute(f"UPDATE {table} SET last_checked=? WHERE source_type IN ('official','manual','rss','api')", (today,))


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        touch_manual_records(conn)
        conn.commit()
    finally:
        conn.close()

    results = {}
    try:
        from importers import sync_scholarshipowl
        results["scholarshipowl"] = sync_scholarshipowl()
    except Exception as exc:
        results["scholarshipowl"] = {"skipped": str(exc)}

    conn = sqlite3.connect(DB_PATH)
    try:
        print({
            "platforms": conn.execute("SELECT COUNT(*) FROM platforms").fetchone()[0],
            "courses": conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0],
            "opportunities": conn.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0],
            "importers": results,
        })
    finally:
        conn.close()


if __name__ == "__main__":
    main()
