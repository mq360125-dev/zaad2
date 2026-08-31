from __future__ import annotations
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False

import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, HttpUrl

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
DB_PATH = BASE_DIR / "opportunities.db"

app = FastAPI(
    title="Global Opportunities Platform API",
    version="3.0.0",
    description="Curated educational opportunities directory with official sources and platform profiles.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CATEGORIES = {
    "scholarship": {"label": "المنح الدراسية", "icon": "🎓"},
    "course": {"label": "الكورسات", "icon": "💻"},
    "volunteer": {"label": "التطوع", "icon": "🤝"},
    "competition": {"label": "المسابقات", "icon": "🏆"},
    "internship": {"label": "التدريبات", "icon": "💼"},
    "program": {"label": "البرامج التعليمية", "icon": "🚀"},
}

SCHEMA = {
    "sources": """
        CREATE TABLE IF NOT EXISTS platforms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            logo TEXT,
            description TEXT NOT NULL,
            official_url TEXT NOT NULL,
            courses_url TEXT,
            certificates_url TEXT,
            scholarships_url TEXT,
            volunteering_url TEXT,
            country TEXT,
            categories TEXT NOT NULL DEFAULT '[]',
            free_courses_available INTEGER NOT NULL DEFAULT 0,
            certificates_available INTEGER NOT NULL DEFAULT 0,
            financial_aid_available INTEGER NOT NULL DEFAULT 0,
            free_access_guide TEXT,
            source_type TEXT NOT NULL DEFAULT 'official',
            official_source TEXT NOT NULL,
            verified INTEGER NOT NULL DEFAULT 1,
            last_checked TEXT NOT NULL
        )
    """,
    "courses": """
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            platform_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            level TEXT,
            language TEXT,
            duration TEXT,
            free INTEGER NOT NULL DEFAULT 0,
            certificate_available INTEGER NOT NULL DEFAULT 0,
            certificate_type TEXT,
            price TEXT,
            financial_aid INTEGER NOT NULL DEFAULT 0,
            official_url TEXT NOT NULL,
            source TEXT NOT NULL,
            source_type TEXT NOT NULL DEFAULT 'official',
            verified INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'open',
            last_checked TEXT NOT NULL,
            FOREIGN KEY(platform_id) REFERENCES platforms(id)
        )
    """,
    "opportunities": """
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            organization TEXT NOT NULL,
            description TEXT NOT NULL,
            country TEXT,
            online INTEGER NOT NULL DEFAULT 0,
            age_min INTEGER,
            age_max INTEGER,
            education_level TEXT,
            category TEXT,
            language TEXT,
            funding_type TEXT,
            tuition_covered INTEGER,
            accommodation INTEGER,
            meals INTEGER,
            travel INTEGER,
            stipend TEXT,
            duration TEXT,
            certificate INTEGER,
            deadline TEXT,
            application_url TEXT NOT NULL,
            official_source TEXT NOT NULL,
            source_type TEXT NOT NULL DEFAULT 'official',
            verified INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'open',
            last_checked TEXT NOT NULL,
            amount TEXT,
            awards INTEGER,
            start_date TEXT,
            timezone TEXT,
            recurring_type TEXT,
            recurring_value TEXT,
            expired_at TEXT,
            eligibility TEXT,
            requirements TEXT
        )
    """,
}


def now_iso() -> str:
    return datetime.now(timezone.utc).date().isoformat()

def admin_guard(x_admin_token: Optional[str]) -> None:
    expected = os.getenv("ADMIN_TOKEN")
    if not expected:
        raise HTTPException(503, "Admin API is disabled. Set ADMIN_TOKEN in the environment.")
    if not x_admin_token or not hashlib.sha256(x_admin_token.encode()).hexdigest() == hashlib.sha256(expected.encode()).hexdigest():
        raise HTTPException(401, "Invalid admin token")



def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = db()
    try:
        for statement in SCHEMA.values():
            conn.execute(statement)
        # Lightweight migrations for databases created by earlier versions.
        migrations = {
            "platforms": {"free_access_guide": "TEXT"},
            "opportunities": {
                "amount": "TEXT", "awards": "INTEGER", "start_date": "TEXT", "timezone": "TEXT",
                "recurring_type": "TEXT", "recurring_value": "TEXT", "expired_at": "TEXT",
                "eligibility": "TEXT", "requirements": "TEXT", "required_documents": "TEXT", "application_steps": "TEXT", "about_opportunity": "TEXT", "keywords": "TEXT",
            },
        }
        for table, cols in migrations.items():
            existing = {r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
            for name, typ in cols.items():
                if name not in existing:
                    conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {typ}")
        conn.commit()
    finally:
        conn.close()


def rows(sql: str, params: tuple = ()) -> list[dict]:
    conn = db()
    try:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()


def row(sql: str, params: tuple = ()) -> Optional[dict]:
    result = rows(sql, params)
    return result[0] if result else None


LANGUAGE_SEARCH_ALIASES = {
    "روسيا": ["روسيا", "روسي", "russia", "russian", "русский"],
    "روسي": ["روسيا", "روسي", "russia", "russian", "русский"],
    "russia": ["روسيا", "روسي", "russia", "russian", "русский"],
    "russian": ["روسيا", "روسي", "russia", "russian", "русский"],
    "فرنسا": ["فرنسا", "فرنسي", "france", "french", "français"],
    "فرنسي": ["فرنسا", "فرنسي", "france", "french", "français"],
    "france": ["فرنسا", "فرنسي", "france", "french", "français"],
    "french": ["فرنسا", "فرنسي", "france", "french", "français"],
    "ألمانيا": ["ألمانيا", "الماني", "ألماني", "germany", "german", "deutsch"],
    "الماني": ["ألمانيا", "الماني", "ألماني", "germany", "german", "deutsch"],
    "ألماني": ["ألمانيا", "الماني", "ألماني", "germany", "german", "deutsch"],
    "germany": ["ألمانيا", "الماني", "ألماني", "germany", "german", "deutsch"],
    "german": ["ألمانيا", "الماني", "ألماني", "germany", "german", "deutsch"],
    "اليابان": ["اليابان", "ياباني", "japan", "japanese", "日本語"],
    "ياباني": ["اليابان", "ياباني", "japan", "japanese", "日本語"],
    "japan": ["اليابان", "ياباني", "japan", "japanese", "日本語"],
    "japanese": ["اليابان", "ياباني", "japan", "japanese", "日本語"],
    "هولندا": ["هولندا", "هولندي", "netherlands", "dutch", "nederlands"],
    "هولندي": ["هولندا", "هولندي", "netherlands", "dutch", "nederlands"],
    "netherlands": ["هولندا", "هولندي", "netherlands", "dutch", "nederlands"],
    "dutch": ["هولندا", "هولندي", "netherlands", "dutch", "nederlands"],
    "إسبانيا": ["إسبانيا", "اسباني", "إسباني", "spain", "spanish", "español"],
    "اسباني": ["إسبانيا", "اسباني", "إسباني", "spain", "spanish", "español"],
    "إسباني": ["إسبانيا", "اسباني", "إسباني", "spain", "spanish", "español"],
    "spain": ["إسبانيا", "اسباني", "إسباني", "spain", "spanish", "español"],
    "spanish": ["إسبانيا", "اسباني", "إسباني", "spain", "spanish", "español"],
    "إيطاليا": ["إيطاليا", "ايطالي", "إيطالي", "italy", "italian", "italiano"],
    "ايطالي": ["إيطاليا", "ايطالي", "إيطالي", "italy", "italian", "italiano"],
    "إيطالي": ["إيطاليا", "ايطالي", "إيطالي", "italy", "italian", "italiano"],
    "italy": ["إيطاليا", "ايطالي", "إيطالي", "italy", "italian", "italiano"],
    "italian": ["إيطاليا", "ايطالي", "إيطالي", "italy", "italian", "italiano"],
    "تركيا": ["تركيا", "تركي", "turkey", "turkish", "türkçe"],
    "تركي": ["تركيا", "تركي", "turkey", "turkish", "türkçe"],
    "turkey": ["تركيا", "تركي", "turkey", "turkish", "türkçe"],
    "turkish": ["تركيا", "تركي", "turkey", "turkish", "türkçe"],
    "الصين": ["الصين", "صيني", "china", "chinese", "中文"],
    "صيني": ["الصين", "صيني", "china", "chinese", "中文"],
    "china": ["الصين", "صيني", "china", "chinese", "中文"],
    "chinese": ["الصين", "صيني", "china", "chinese", "中文"],
    "كوريا": ["كوريا", "كوري", "korea", "korean", "한국어"],
    "كوري": ["كوريا", "كوري", "korea", "korean", "한국어"],
    "korea": ["كوريا", "كوري", "korea", "korean", "한국어"],
    "korean": ["كوريا", "كوري", "korea", "korean", "한국어"],
    "بولندا": ["بولندا", "بولندي", "poland", "polish", "polski"],
    "بولندي": ["بولندا", "بولندي", "poland", "polish", "polski"],
    "poland": ["بولندا", "بولندي", "poland", "polish", "polski"],
    "polish": ["بولندا", "بولندي", "poland", "polish", "polski"],
}

BRAND_SEARCH_ALIASES = {
    "جوجل": ["google", "جوجل", "غوغل"],
    "غوغل": ["google", "جوجل", "غوغل"],
    "google": ["google", "جوجل", "غوغل"],
    "هواوي": ["huawei", "هواوي", "huaweicloud", "huawei cloud", "ict academy"],
    "huawei": ["huawei", "هواوي", "huaweicloud", "huawei cloud", "ict academy"],
    "مايكروسوفت": ["microsoft", "مايكروسوفت", "microsoft learn", "azure"],
    "مايكروسوفت": ["microsoft", "مايكروسوفت", "microsoft learn", "azure"],
    "microsoft": ["microsoft", "مايكروسوفت", "microsoft learn", "azure"],
    "هارفارد": ["harvard", "هارفارد", "cs50", "cs50x", "cs50p"],
    "harvard": ["harvard", "هارفارد", "cs50", "cs50x", "cs50p"],
    "ibm": ["ibm", "ibm skillsbuild", "skillsbuild", "آي بي إم"],
    "آي بي إم": ["ibm", "ibm skillsbuild", "skillsbuild", "آي بي إم"],
    "سيسكو": ["cisco", "سيسكو", "networking academy", "netacad"],
    "cisco": ["cisco", "سيسكو", "networking academy", "netacad"],
    "أمازون": ["aws", "amazon", "أمازون", "amazon web services"],
    "aws": ["aws", "amazon", "أمازون", "amazon web services"],
    "ميتا": ["meta", "ميتا", "meta blueprint"],
    "meta": ["meta", "ميتا", "meta blueprint"],
    "أوراكل": ["oracle", "أوراكل", "oracle academy"],
    "oracle": ["oracle", "أوراكل", "oracle academy"],
    "نفيديا": ["nvidia", "نفيديا", "nvidia deep learning institute"],
    "nvidia": ["nvidia", "نفيديا", "nvidia deep learning institute"],
    "كورسيرا": ["coursera", "كورسيرا"],
    "coursera": ["coursera", "كورسيرا"],
    "إدكس": ["edx", "edx", "إدكس"],
    "edx": ["edx", "إدكس"],
}

def expanded_search_terms(value: str | None) -> list[str]:
    if not value:
        return []
    raw = str(value).strip().lower()
    terms = [raw]
    all_aliases = {**LANGUAGE_SEARCH_ALIASES, **BRAND_SEARCH_ALIASES}
    for token in raw.replace(',', ' ').split():
        terms.extend(all_aliases.get(token, []))
    terms.extend(all_aliases.get(raw, []))
    # Allow Arabic/English country, language, and brand names embedded in a phrase.
    for key, aliases in all_aliases.items():
        if key in raw and len(key) > 2:
            terms.extend(aliases)
    # Common generic words should not make brand searches noisy.
    stopwords = {"كورس", "كورسات", "دورة", "دورات", "منحة", "منح", "فرصة", "فرص", "تعلم", "مجاني", "مجانية", "شهادة", "شهادات"}
    return list(dict.fromkeys(t for t in terms if t and t not in stopwords))

def parse_bool(value):
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def platform_out(item: dict) -> dict:
    item = dict(item)
    if isinstance(item.get("categories"), str):
        try:
            item["categories"] = json.loads(item["categories"] or "[]")
        except (TypeError, ValueError):
            item["categories"] = []
    for key in ("free_courses_available", "certificates_available", "financial_aid_available", "verified"):
        if key in item:
            item[key] = parse_bool(item[key])
    return item


def course_out(item: dict) -> dict:
    item = dict(item)
    if "source" in item:
        item["source_url"] = item["source"]
    for key in ("free", "certificate_available", "financial_aid", "verified"):
        if key in item:
            item[key] = parse_bool(item[key])
    # Keep a consistent detail shape for every course without inventing provider claims.
    item["about_opportunity"] = item.get("description") or "لا يوجد وصف منشور في السجل."
    item["eligibility_details"] = item.get("eligibility") or "شروط الالتحاق التفصيلية تعتمد على صفحة الكورس الرسمية ومتطلبات المنصة."
    item["requirements_details"] = item.get("requirements") or "تحقق من متطلبات التسجيل والشهادة في الصفحة الرسمية قبل البدء."
    item["required_documents"] = item.get("required_documents") or "عادةً لا توجد مستندات للتسجيل في المحتوى المفتوح، ما لم تطلب المنصة خلاف ذلك."
    item["application_steps"] = item.get("application_steps") or [
        "افتح الرابط الرسمي للكورس وتأكد من اسم الجهة والكورس.",
        "أنشئ حسابًا أو سجّل الدخول إذا طلبت المنصة ذلك.",
        "اختر الكورس أو المسار المناسب وراجع السعر وشروط الشهادة قبل البدء.",
        "أكمل المحتوى والاختبارات المطلوبة للحصول على إثبات الإتمام أو الشهادة إذا كانت الصفحة الرسمية تنص على توفرها."
    ]
    return item


def opportunity_out(item: dict) -> dict:
    item = dict(item)
    if "official_source" in item:
        item["source_url"] = item["official_source"]
    for key in ("eligibility", "requirements", "required_documents", "application_steps", "keywords"):
        if key in item and isinstance(item[key], str):
            try:
                item[key] = json.loads(item[key])
            except (TypeError, ValueError):
                pass
    for key in ("online", "tuition_covered", "accommodation", "meals", "travel", "certificate", "verified"):
        if key in item:
            item[key] = parse_bool(item[key]) if item[key] is not None else None

    item["about_opportunity"] = item.get("about_opportunity") or item.get("description") or "لا يوجد وصف منشور في السجل."
    item["eligibility_details"] = item.get("eligibility") or (
        "شروط الأهلية التفصيلية غير مسجلة في الكتالوج الحالي؛ يجب اعتماد الشروط المنشورة في المصدر الرسمي فقط."
    )
    item["requirements_details"] = item.get("requirements") or (
        "المتطلبات التفصيلية غير مسجلة في الكتالوج الحالي؛ يجب مراجعة صفحة الجهة الرسمية قبل التقديم."
    )
    item["required_documents"] = item.get("required_documents") or (
        "لم تُحدد مستندات إضافية في السجل؛ راجع قائمة المستندات في صفحة التقديم الرسمية."
    )
    if not item.get("application_steps"):
        type_steps = {
            "scholarship": [
                "افتح صفحة التقديم الرسمية وتحقق من الدورة الحالية وموعدها.",
                "أنشئ حسابًا في بوابة الجهة أو الجامعة إذا كان مطلوبًا.",
                "اقرأ شروط الأهلية وقائمة المستندات حرفيًا قبل البدء.",
                "أكمل نموذج الطلب وارفع المستندات المطلوبة بالصيغة والحجم المطلوبين.",
                "أرسل الطلب واحتفظ برقم الطلب أو رسالة التأكيد، ثم تابع البريد أو حسابك الرسمي."
            ],
            "internship": [
                "افتح صفحة التدريب الرسمية وتحقق من فتح التقديم للفترة الحالية.",
                "راجع العمر والمرحلة الدراسية ومتطلبات المهارات.",
                "جهز السيرة الذاتية وأي مستندات أو نماذج تطلبها الجهة.",
                "قدّم عبر البوابة الرسمية فقط، ثم تابع رسالة التأكيد وحالة الطلب."
            ],
            "volunteer": [
                "افتح صفحة التطوع الرسمية وتحقق من أن التسجيل متاح حاليًا.",
                "راجع شرط العمر وطبيعة النشاط وهل هو أونلاين أم حضوري.",
                "أنشئ الحساب أو املأ نموذج المشاركة وأرسل البيانات المطلوبة.",
                "احتفظ بتأكيد التسجيل واتبع تعليمات الجهة للحصول على إثبات المشاركة إن كان متاحًا."
            ],
        }
        item["application_steps"] = type_steps.get(item.get("type"), [
            "افتح المصدر الرسمي وتحقق من حالة الفرصة الحالية.",
            "اقرأ شروط الأهلية والمتطلبات قبل التسجيل.",
            "أنشئ حسابًا إذا لزم وأكمل النموذج الرسمي.",
            "ارفع المستندات المطلوبة وأرسل الطلب.",
            "احتفظ بتأكيد التقديم وتابع تعليمات الجهة الرسمية."
        ])
    return item


class PlatformCreate(BaseModel):
    slug: str
    name: str
    logo: Optional[str] = None
    description: str
    official_url: HttpUrl
    courses_url: Optional[HttpUrl] = None
    certificates_url: Optional[HttpUrl] = None
    scholarships_url: Optional[HttpUrl] = None
    volunteering_url: Optional[HttpUrl] = None
    country: Optional[str] = None
    categories: list[str] = Field(default_factory=list)
    free_courses_available: bool = False
    certificates_available: bool = False
    financial_aid_available: bool = False
    source_type: str = "official"
    official_source: HttpUrl


class CourseCreate(BaseModel):
    slug: str
    title: str
    platform_id: int
    description: str
    category: str
    level: Optional[str] = None
    language: Optional[str] = None
    duration: Optional[str] = None
    free: bool = False
    certificate_available: bool = False
    certificate_type: Optional[str] = None
    price: Optional[str] = None
    financial_aid: bool = False
    official_url: HttpUrl
    source: HttpUrl


class OpportunityCreate(BaseModel):
    slug: str
    type: str
    title: str
    organization: str
    description: str
    country: Optional[str] = None
    online: bool = False
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    education_level: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None
    funding_type: Optional[str] = None
    tuition_covered: Optional[bool] = None
    accommodation: Optional[bool] = None
    meals: Optional[bool] = None
    travel: Optional[bool] = None
    stipend: Optional[str] = None
    duration: Optional[str] = None
    certificate: Optional[bool] = None
    deadline: Optional[str] = None
    application_url: HttpUrl
    official_source: HttpUrl


@app.on_event("startup")
def startup() -> None:
    init_db()
    from seed import merge_expanded_catalog, seed_database
    seed_database()
    merge_expanded_catalog()
    from under18_catalog import merge_under18_catalog
    merge_under18_catalog()


@app.get("/api/health")
def health():
    return {"status": "ok", "database": str(DB_PATH.name), "version": app.version}


@app.get("/api/meta")
def meta():
    counts = {key: (row("SELECT COUNT(*) AS n FROM opportunities WHERE type = ?", (key,)) or {"n": 0})["n"] for key in CATEGORIES}
    course_count = (row("SELECT COUNT(*) AS n FROM courses") or {"n": 0})["n"]
    platform_count = (row("SELECT COUNT(*) AS n FROM platforms") or {"n": 0})["n"]
    return {"categories": CATEGORIES, "counts": counts, "courses": course_count, "platforms": platform_count}


@app.get("/api/live")
def live_discovery(
    type: str = Query("course", pattern="^(course|scholarship)$"),
    search: str = "",
    limit: int = Query(30, ge=1, le=100),
):
    """Aggregate configured official APIs without making the catalog depend on them."""
    from live_sources import discover

    results, providers = discover(type, search, limit)
    return {"type": type, "query": search, "total": len(results), "results": results, "providers": providers}


@app.get("/api/platforms")
def get_platforms(
    search: Optional[str] = None,
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(24, ge=1, le=100),
):
    sql = "SELECT * FROM platforms WHERE 1=1"
    params: list = []
    if search:
        terms = expanded_search_terms(search)
        clauses=[]
        for term in terms:
            like=f"%{term}%"
            clauses.append("(name LIKE ? OR description LIKE ? OR country LIKE ? OR categories LIKE ?)")
            params.extend([like,like,like,like])
        sql += " AND (" + " OR ".join(clauses) + ")"
    if category:
        sql += " AND categories LIKE ?"
        params.append(f'%"{category}"%')
    count = row("SELECT COUNT(*) AS n FROM (" + sql + ")", tuple(params))["n"]
    sql += " ORDER BY name LIMIT ? OFFSET ?"
    params += [page_size, (page - 1) * page_size]
    return {"total": count, "page": page, "page_size": page_size, "results": [platform_out(x) for x in rows(sql, tuple(params))]}


@app.get("/api/platforms/{slug}")
def get_platform(slug: str):
    item = row("SELECT * FROM platforms WHERE slug = ?", (slug,))
    if not item:
        raise HTTPException(404, "Platform not found")
    item = platform_out(item)
    item["courses"] = [course_out(x) for x in rows("SELECT * FROM courses WHERE platform_id = ? ORDER BY title", (item["id"],))]
    item["opportunities"] = [opportunity_out(x) for x in rows("SELECT * FROM opportunities WHERE organization = ? ORDER BY title", (item["name"],))]
    item["course_count"] = len(item["courses"])
    item["opportunity_count"] = len(item["opportunities"])
    return item


@app.get("/api/courses")
def get_courses(
    search: Optional[str] = None,
    platform: Optional[str] = None,
    category: Optional[str] = None,
    free: Optional[bool] = None,
    certificate: Optional[bool] = None,
    language: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(24, ge=1, le=100),
):
    sql = """
        SELECT c.*, p.name AS platform, p.slug AS platform_slug
        FROM courses c JOIN platforms p ON p.id = c.platform_id WHERE 1=1
    """
    params: list = []
    if search:
        terms = expanded_search_terms(search)
        clauses=[]
        for term in terms:
            like=f"%{term}%"
            clauses.append("(c.title LIKE ? OR c.description LIKE ? OR p.name LIKE ? OR c.language LIKE ? OR c.category LIKE ? OR p.country LIKE ? OR p.categories LIKE ?)")
            params.extend([like,like,like,like,like,like,like])
        sql += " AND (" + " OR ".join(clauses) + ")"
    if platform:
        sql += " AND p.slug = ?"; params.append(platform)
    if category:
        sql += " AND c.category = ?"; params.append(category)
    if free is not None:
        sql += " AND c.free = ?"; params.append(int(free))
    if certificate is not None:
        sql += " AND c.certificate_available = ?"; params.append(int(certificate))
    if language:
        sql += " AND c.language LIKE ?"; params.append(f"%{language}%")
    count_sql = "SELECT COUNT(*) AS n FROM (" + sql + ")"
    total = row(count_sql, tuple(params))["n"]
    sql += " ORDER BY c.title LIMIT ? OFFSET ?"
    params += [page_size, (page - 1) * page_size]
    return {"total": total, "page": page, "page_size": page_size, "results": [course_out(x) for x in rows(sql, tuple(params))]}


@app.get("/api/courses/{course_id}")
def get_course(course_id: int):
    item = row("""SELECT c.*, p.name AS platform, p.slug AS platform_slug FROM courses c JOIN platforms p ON p.id=c.platform_id WHERE c.id=?""", (course_id,))
    if not item:
        raise HTTPException(404, "Course not found")
    return course_out(item)


@app.get("/api/opportunities")
def get_opportunities(
    category: Optional[str] = None,
    type: Optional[str] = None,
    search: Optional[str] = None,
    platform: Optional[str] = None,
    country: Optional[str] = None,
    online: Optional[bool] = None,
    free: Optional[bool] = None,
    certificate: Optional[bool] = None,
    age: Optional[int] = Query(None, ge=0, le=100),
    education_level: Optional[str] = None,
    language: Optional[str] = None,
    funding: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(24, ge=1, le=100),
):
    sql = "SELECT * FROM opportunities WHERE 1=1"
    params: list = []
    if category and category != "all": sql += " AND category = ?"; params.append(category)
    if type and type != "all": sql += " AND type = ?"; params.append(type)
    if search:
        terms = expanded_search_terms(search)
        clauses=[]
        for term in terms:
            like=f"%{term}%"
            clauses.append("(title LIKE ? OR description LIKE ? OR organization LIKE ? OR country LIKE ? OR language LIKE ? OR category LIKE ? OR education_level LIKE ?)")
            params.extend([like,like,like,like,like,like,like])
        sql += " AND (" + " OR ".join(clauses) + ")"
    if platform:
        sql += " AND organization = (SELECT name FROM platforms WHERE slug = ?)"; params.append(platform)
    if country: sql += " AND country LIKE ?"; params.append(f"%{country}%")
    if online is not None: sql += " AND online = ?"; params.append(int(online))
    if free is True: sql += " AND (funding_type = 'Free Program' OR tuition_covered = 1)"
    if certificate is not None: sql += " AND certificate = ?"; params.append(int(certificate))
    if age is not None: sql += " AND (age_min IS NULL OR age_min <= ?) AND (age_max IS NULL OR age_max >= ?)"; params += [age, age]
    if education_level: sql += " AND education_level LIKE ?"; params.append(f"%{education_level}%")
    if language: sql += " AND language LIKE ?"; params.append(f"%{language}%")
    if funding: sql += " AND funding_type = ?"; params.append(funding)
    count_sql = "SELECT COUNT(*) AS n FROM (" + sql + ")"
    total = row(count_sql, tuple(params))["n"]
    sql += " ORDER BY CASE status WHEN 'open' THEN 0 ELSE 1 END, title LIMIT ? OFFSET ?"
    params += [page_size, (page - 1) * page_size]
    return {"total": total, "page": page, "page_size": page_size, "results": [opportunity_out(x) for x in rows(sql, tuple(params))]}


@app.get("/api/opportunities/{opportunity_id}")
def get_opportunity(opportunity_id: int):
    item = row("SELECT * FROM opportunities WHERE id = ?", (opportunity_id,))
    if not item:
        raise HTTPException(404, "Opportunity not found")
    return opportunity_out(item)


@app.get("/api/scholarships")
def get_scholarships(search: Optional[str] = None, country: Optional[str] = None, free: Optional[bool] = None, certificate: Optional[bool] = None, age: Optional[int] = Query(None, ge=0, le=100), education_level: Optional[str] = None, language: Optional[str] = None, funding: Optional[str] = None, page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100)):
    return get_opportunities(type="scholarship", search=search, country=country, free=free, certificate=certificate, age=age, education_level=education_level, language=language, funding=funding, page=page, page_size=page_size)


@app.get("/api/volunteering")
def get_volunteering(search: Optional[str] = None, country: Optional[str] = None, online: Optional[bool] = None, certificate: Optional[bool] = None, age: Optional[int] = Query(None, ge=0, le=100), language: Optional[str] = None, page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100)):
    return get_opportunities(type="volunteer", search=search, country=country, online=online, certificate=certificate, age=age, language=language, page=page, page_size=page_size)


@app.get("/api/competitions")
def get_competitions(search: Optional[str] = None, country: Optional[str] = None, online: Optional[bool] = None, age: Optional[int] = Query(None, ge=0, le=100), education_level: Optional[str] = None, language: Optional[str] = None, page: int = Query(1, ge=1), page_size: int = Query(24, ge=1, le=100)):
    return get_opportunities(type="competition", search=search, country=country, online=online, age=age, education_level=education_level, language=language, page=page, page_size=page_size)


@app.post("/api/admin/platforms")
def create_platform(payload: PlatformCreate, x_admin_token: Optional[str] = Header(None)):
    admin_guard(x_admin_token)
    data = payload.model_dump(mode="json")
    try:
        conn = db()
        cur = conn.execute("""INSERT INTO platforms (slug,name,logo,description,official_url,courses_url,certificates_url,scholarships_url,volunteering_url,country,categories,free_courses_available,certificates_available,financial_aid_available,source_type,official_source,verified,last_checked) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            data["slug"], data["name"], data["logo"], data["description"], str(data["official_url"]), str(data["courses_url"]) if data["courses_url"] else None,
            str(data["certificates_url"]) if data["certificates_url"] else None, str(data["scholarships_url"]) if data["scholarships_url"] else None,
            str(data["volunteering_url"]) if data["volunteering_url"] else None, data["country"], __import__("json").dumps(data["categories"]), int(data["free_courses_available"]), int(data["certificates_available"]), int(data["financial_aid_available"]), data["source_type"], str(data["official_source"]), 1, now_iso()))
        conn.commit(); conn.close()
        return {"id": cur.lastrowid, "message": "Platform created"}
    except sqlite3.IntegrityError as exc:
        raise HTTPException(409, str(exc))


@app.post("/api/admin/courses")
def create_course(payload: CourseCreate, x_admin_token: Optional[str] = Header(None)):
    admin_guard(x_admin_token)
    data = payload.model_dump(mode="json")
    if not row("SELECT id FROM platforms WHERE id=?", (data["platform_id"],)):
        raise HTTPException(400, "platform_id does not exist")
    conn = db()
    try:
        cur = conn.execute("""INSERT INTO courses (slug,title,platform_id,description,category,level,language,duration,free,certificate_available,certificate_type,price,financial_aid,official_url,source,verified,status,last_checked) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            data["slug"],data["title"],data["platform_id"],data["description"],data["category"],data["level"],data["language"],data["duration"],int(data["free"]),int(data["certificate_available"]),data["certificate_type"],data["price"],int(data["financial_aid"]),str(data["official_url"]),str(data["source"]),1,"open",now_iso()))
        conn.commit(); return {"id": cur.lastrowid, "message": "Course created"}
    except sqlite3.IntegrityError as exc:
        raise HTTPException(409, str(exc))
    finally: conn.close()


@app.post("/api/admin/opportunities")
def create_opportunity(payload: OpportunityCreate, x_admin_token: Optional[str] = Header(None)):
    admin_guard(x_admin_token)
    data = payload.model_dump(mode="json")
    if data["type"] not in CATEGORIES:
        raise HTTPException(400, "Unsupported opportunity type")
    conn = db()
    try:
        cur = conn.execute("""INSERT INTO opportunities (slug,type,title,organization,description,country,online,age_min,age_max,education_level,category,language,funding_type,tuition_covered,accommodation,meals,travel,stipend,duration,certificate,deadline,application_url,official_source,verified,status,last_checked) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            data["slug"],data["type"],data["title"],data["organization"],data["description"],data["country"],int(data["online"]),data["age_min"],data["age_max"],data["education_level"],data["category"],data["language"],data["funding_type"],None if data["tuition_covered"] is None else int(data["tuition_covered"]),None if data["accommodation"] is None else int(data["accommodation"]),None if data["meals"] is None else int(data["meals"]),None if data["travel"] is None else int(data["travel"]),data["stipend"],data["duration"],None if data["certificate"] is None else int(data["certificate"]),data["deadline"],str(data["application_url"]),str(data["official_source"]),1,"open",now_iso()))
        conn.commit(); return {"id": cur.lastrowid, "message": "Opportunity created"}
    except sqlite3.IntegrityError as exc:
        raise HTTPException(409, str(exc))
    finally: conn.close()



@app.put("/api/admin/platforms/{platform_id}")
def update_platform(platform_id: int, payload: PlatformCreate, x_admin_token: Optional[str] = Header(None)):
    admin_guard(x_admin_token)
    data = payload.model_dump(mode="json")
    if not row("SELECT id FROM platforms WHERE id=?", (platform_id,)):
        raise HTTPException(404, "Platform not found")
    conn = db()
    try:
        conn.execute("""UPDATE platforms SET slug=?,name=?,logo=?,description=?,official_url=?,courses_url=?,certificates_url=?,scholarships_url=?,volunteering_url=?,country=?,categories=?,free_courses_available=?,certificates_available=?,financial_aid_available=?,source_type=?,official_source=?,last_checked=? WHERE id=?""", (data["slug"],data["name"],data["logo"],data["description"],str(data["official_url"]),str(data["courses_url"]) if data["courses_url"] else None,str(data["certificates_url"]) if data["certificates_url"] else None,str(data["scholarships_url"]) if data["scholarships_url"] else None,str(data["volunteering_url"]) if data["volunteering_url"] else None,data["country"],__import__("json").dumps(data["categories"]),int(data["free_courses_available"]),int(data["certificates_available"]),int(data["financial_aid_available"]),data["source_type"],str(data["official_source"]),now_iso(),platform_id))
        conn.commit()
        return {"message":"Platform updated"}
    except sqlite3.IntegrityError as exc:
        raise HTTPException(409, str(exc))
    finally: conn.close()


@app.delete("/api/admin/platforms/{platform_id}")
def delete_platform(platform_id: int, x_admin_token: Optional[str] = Header(None)):
    admin_guard(x_admin_token)
    conn = db()
    try:
        cur = conn.execute("DELETE FROM platforms WHERE id=?", (platform_id,))
        conn.commit()
        if not cur.rowcount: raise HTTPException(404, "Platform not found")
        return {"message":"Platform deleted"}
    except sqlite3.IntegrityError:
        raise HTTPException(409, "Cannot delete a platform that still has courses")
    finally: conn.close()


@app.patch("/api/admin/opportunities/{opportunity_id}")
def update_opportunity(opportunity_id: int, payload: OpportunityCreate, x_admin_token: Optional[str] = Header(None)):
    admin_guard(x_admin_token)
    data = payload.model_dump(mode="json")
    if data["type"] not in CATEGORIES: raise HTTPException(400, "Unsupported opportunity type")
    conn = db()
    try:
        cur = conn.execute("""UPDATE opportunities SET slug=?,type=?,title=?,organization=?,description=?,country=?,online=?,age_min=?,age_max=?,education_level=?,category=?,language=?,funding_type=?,tuition_covered=?,accommodation=?,meals=?,travel=?,stipend=?,duration=?,certificate=?,deadline=?,application_url=?,official_source=?,last_checked=? WHERE id=?""", (data["slug"],data["type"],data["title"],data["organization"],data["description"],data["country"],int(data["online"]),data["age_min"],data["age_max"],data["education_level"],data["category"],data["language"],data["funding_type"],None if data["tuition_covered"] is None else int(data["tuition_covered"]),None if data["accommodation"] is None else int(data["accommodation"]),None if data["meals"] is None else int(data["meals"]),None if data["travel"] is None else int(data["travel"]),data["stipend"],data["duration"],None if data["certificate"] is None else int(data["certificate"]),data["deadline"],str(data["application_url"]),str(data["official_source"]),now_iso(),opportunity_id))
        conn.commit()
        if not cur.rowcount: raise HTTPException(404, "Opportunity not found")
        return {"message":"Opportunity updated"}
    except sqlite3.IntegrityError as exc: raise HTTPException(409, str(exc))
    finally: conn.close()


@app.delete("/api/admin/courses/{course_id}")
def delete_course(course_id: int, x_admin_token: Optional[str] = Header(None)):
    admin_guard(x_admin_token)
    conn=db()
    try:
        cur=conn.execute("DELETE FROM courses WHERE id=?",(course_id,)); conn.commit()
        if not cur.rowcount: raise HTTPException(404,"Course not found")
        return {"message":"Course deleted"}
    finally: conn.close()


@app.patch("/api/admin/courses/{course_id}/verification")
def verify_course(course_id: int, verified: bool = Query(...), x_admin_token: Optional[str] = Header(None)):
    admin_guard(x_admin_token)
    conn=db()
    try:
        cur=conn.execute("UPDATE courses SET verified=?, last_checked=? WHERE id=?",(int(verified),now_iso(),course_id)); conn.commit()
        if not cur.rowcount: raise HTTPException(404,"Course not found")
        return {"message":"Course verification updated","verified":verified}
    finally: conn.close()


@app.patch("/api/admin/opportunities/{opportunity_id}/verification")
def verify_opportunity(opportunity_id: int, verified: bool = Query(...), x_admin_token: Optional[str] = Header(None)):
    admin_guard(x_admin_token)
    conn=db()
    try:
        cur=conn.execute("UPDATE opportunities SET verified=?, last_checked=? WHERE id=?",(int(verified),now_iso(),opportunity_id)); conn.commit()
        if not cur.rowcount: raise HTTPException(404,"Opportunity not found")
        return {"message":"Opportunity verification updated","verified":verified}
    finally: conn.close()


@app.get("/api/admin/stats")
def admin_stats(x_admin_token: Optional[str] = Header(None)):
    admin_guard(x_admin_token)
    return {"platforms": row("SELECT COUNT(*) n FROM platforms")["n"], "courses": row("SELECT COUNT(*) n FROM courses")["n"], "opportunities": row("SELECT COUNT(*) n FROM opportunities")["n"], "unverified": row("SELECT COUNT(*) n FROM opportunities WHERE verified=0")["n"] + row("SELECT COUNT(*) n FROM courses WHERE verified=0")["n"] + row("SELECT COUNT(*) n FROM platforms WHERE verified=0")["n"]}

@app.delete("/api/admin/opportunities/{opportunity_id}")
def delete_opportunity(opportunity_id: int, x_admin_token: Optional[str] = Header(None)):
    admin_guard(x_admin_token)
    conn = db(); cur = conn.execute("DELETE FROM opportunities WHERE id=?", (opportunity_id,)); conn.commit(); conn.close()
    if not cur.rowcount: raise HTTPException(404, "Opportunity not found")
    return {"message": "Opportunity deleted"}



@app.get("/admin")
def admin_page():
    from fastapi.responses import FileResponse
    return FileResponse(BASE_DIR / "static" / "admin.html")


@app.get("/platform/{slug}")
def platform_page(slug: str):
    item = row("SELECT id FROM platforms WHERE slug=?", (slug,))
    if not item:
        raise HTTPException(404, "Platform not found")
    from fastapi.responses import FileResponse
    return FileResponse(BASE_DIR / "static" / "platform.html")


@app.get("/opportunity/{opportunity_id}")
def opportunity_page(opportunity_id: int):
    if not row("SELECT id FROM opportunities WHERE id=?", (opportunity_id,)):
        raise HTTPException(404, "Opportunity not found")
    from fastapi.responses import FileResponse
    return FileResponse(BASE_DIR / "static" / "detail.html")

@app.get("/course/{course_id}")
def course_page(course_id: int):
    if not row("SELECT id FROM courses WHERE id=?", (course_id,)):
        raise HTTPException(404, "Course not found")
    from fastapi.responses import FileResponse
    return FileResponse(BASE_DIR / "static" / "detail.html")

# Keep the original site's static frontend compatible.
app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static")
