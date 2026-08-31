"""Official-source importers. No scraping is performed here."""
from __future__ import annotations
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

import json
import os
import sqlite3
from datetime import date
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
DB_PATH = BASE_DIR / "opportunities.db"
API_BASE = "https://api.business.scholarshipowl.com"


def fetch_json(url: str, headers: dict[str, str]) -> dict:
    req = Request(url, headers={"Accept": "application/vnd.api+json", **headers})
    with urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def safe_related(base: str, sid: str, relation: str, headers: dict[str, str]):
    try:
        data = fetch_json(f"{base}/api/scholarship/{sid}/{relation}", headers)
        return data.get("data", [])
    except (HTTPError, URLError, TimeoutError, ValueError):
        return []


def sync_scholarshipowl(page_size: int = 100) -> int:
    """Import published ScholarshipOwl scholarships into the unified opportunity table.

    The provider exposes JSON:API. We intentionally map only fields the API documents;
    unknown eligibility/funding/application details stay Unknown rather than being inferred.
    """
    token = os.getenv("SCHOLARSHIPOWL_API_KEY")
    if not token:
        raise RuntimeError("SCHOLARSHIPOWL_API_KEY is not set")

    imported = 0
    page = 1
    conn = sqlite3.connect(DB_PATH)
    try:
        while True:
            data = fetch_json(
                f"{API_BASE}/api/scholarship?page[number]={page}&page[size]={page_size}",
                {"SCHOLARSHIP-APP-API-Key": token},
            )
            items = data.get("data", [])
            if not items:
                break
            for item in items:
                attrs = item.get("attributes", {})
                sid = str(item.get("id"))
                slug = "scholarshipowl-" + sid.lower().replace("/", "-")
                deadline = attrs.get("deadline")
                expired = attrs.get("expiredAt")
                status = "expired" if expired else "open"
                title = attrs.get("title") or "Untitled scholarship"
                description = attrs.get("description") or "Scholarship details provided by ScholarshipOwl."
                amount = attrs.get("amount")
                awards = attrs.get("awards")
                amount_text = str(amount) if amount is not None else None
                source_url = f"{API_BASE}/api/scholarship/{sid}"
                fields = safe_related(API_BASE, sid, "fields", {"SCHOLARSHIP-APP-API-Key": token})
                requirements = safe_related(API_BASE, sid, "requirements", {"SCHOLARSHIP-APP-API-Key": token})
                eligibility = json.dumps(fields, ensure_ascii=False) if fields else None
                requirement_text = json.dumps(requirements, ensure_ascii=False) if requirements else None
                conn.execute(
                    """INSERT INTO opportunities
                    (slug,type,title,organization,description,country,online,age_min,age_max,education_level,category,language,funding_type,tuition_covered,accommodation,meals,travel,stipend,duration,certificate,deadline,application_url,official_source,source_type,verified,status,last_checked,amount,awards,start_date,timezone,recurring_type,recurring_value,expired_at,eligibility,requirements)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(slug) DO UPDATE SET
                      title=excluded.title, description=excluded.description, deadline=excluded.deadline,
                      status=excluded.status, stipend=excluded.stipend, official_source=excluded.official_source,
                      source_type=excluded.source_type, verified=excluded.verified, last_checked=excluded.last_checked,
                      amount=excluded.amount, awards=excluded.awards, start_date=excluded.start_date, timezone=excluded.timezone,
                      recurring_type=excluded.recurring_type, recurring_value=excluded.recurring_value, expired_at=excluded.expired_at,
                      eligibility=excluded.eligibility, requirements=excluded.requirements""",
                    (slug, "scholarship", title, "Unknown", description, "Unknown", False, None, None,
                     "Unknown", "Scholarship", "Unknown", "Unknown", None, None, None, None,
                     amount_text, None, None, deadline, "https://scholarshipowl.com/",
                     source_url, "api", True, status, date.today().isoformat(), amount_text, awards, attrs.get("start"), attrs.get("timezone"), attrs.get("recurringType"), attrs.get("recurringValue"), expired, eligibility, requirement_text),
                )
                imported += 1
            if len(items) < page_size:
                break
            page += 1
        conn.commit()
    finally:
        conn.close()
    return imported
