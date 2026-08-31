"""Live adapters for official JSON APIs configured through environment variables."""
from __future__ import annotations

import json
import os
import time
from string import Formatter
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
CACHE_TTL = int(os.getenv("LIVE_API_CACHE_TTL", "900"))
TIMEOUT = int(os.getenv("LIVE_API_TIMEOUT", "12"))
_cache: dict[str, tuple[float, list[dict]]] = {}


def _get_json(url: str, headers: dict[str, str] | None = None) -> object:
    request = Request(url, headers={"Accept": "application/json", **(headers or {})})
    with urlopen(request, timeout=TIMEOUT) as response:
        return json.loads(response.read().decode("utf-8"))


def _items(payload: object) -> list[dict]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("results", "data", "items", "courses", "opportunities"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def _url(template: str, query: str, limit: int) -> str:
    fields = {name for _, name, _, _ in Formatter().parse(template) if name}
    values = {"query": quote_plus(query), "limit": limit}
    return template.format(**{key: values[key] for key in fields if key in values})


def _normalise_course(item: dict, provider: str) -> dict:
    title = item.get("title") or item.get("name") or item.get("courseName")
    url = item.get("official_url") or item.get("url") or item.get("link") or item.get("course_url")
    return {
        "title": title or "Untitled course",
        "description": item.get("description") or item.get("shortDescription") or "Live course listing from the official provider.",
        "platform_name": item.get("platform_name") or item.get("provider") or provider,
        "category": item.get("category") or item.get("subject") or "General",
        "language": item.get("language") or "Unknown",
        "level": item.get("level") or "Unknown",
        "duration": item.get("duration") or "Varies",
        "free": bool(item.get("free", item.get("is_free", False))),
        "certificate_available": bool(item.get("certificate_available", item.get("certificate", False))),
        "certificate_type": item.get("certificate_type") or item.get("credential"),
        "official_url": url or "https://example.com",
        "source": url or "https://example.com",
        "source_type": "api",
        "verified": True,
        "live_provider": provider,
    }


def _normalise_scholarship(item: dict, provider: str) -> dict:
    attrs = item.get("attributes", item)
    title = attrs.get("title") or attrs.get("name") or "Untitled scholarship"
    url = attrs.get("application_url") or attrs.get("url") or attrs.get("link")
    return {
        "type": "scholarship",
        "title": title,
        "organization": attrs.get("organization") or attrs.get("provider") or provider,
        "description": attrs.get("description") or "Live scholarship listing from the official provider.",
        "country": attrs.get("country") or "Global / varies",
        "online": bool(attrs.get("online", False)),
        "education_level": attrs.get("education_level") or "Varies",
        "category": attrs.get("category") or "Scholarship",
        "language": attrs.get("language") or "Varies",
        "funding_type": attrs.get("funding_type") or attrs.get("funding") or "Varies",
        "deadline": attrs.get("deadline"),
        "application_url": url or "https://example.com",
        "official_source": attrs.get("official_source") or url or "https://example.com",
        "source_type": "api",
        "verified": True,
        "status": "open",
        "live_provider": provider,
    }


def _configured(kind: str) -> list[tuple[str, str]]:
    key = "LIVE_COURSE_API_URLS" if kind == "course" else "LIVE_SCHOLARSHIP_API_URLS"
    configured = []
    for index, template in enumerate(os.getenv(key, "").split(",")):
        template = template.strip()
        if template:
            configured.append((f"custom-{index + 1}", template))
    if kind == "scholarship" and os.getenv("SCHOLARSHIPOWL_API_KEY"):
        configured.append(("scholarshipowl", "https://api.business.scholarshipowl.com/api/scholarship?page[number]=1&page[size]={limit}"))
    return configured


def discover(kind: str, query: str = "", limit: int = 30) -> tuple[list[dict], list[dict]]:
    """Query all configured APIs; one provider failing does not hide other results."""
    result: list[dict] = []
    statuses: list[dict] = []
    for provider, template in _configured(kind):
        cache_key = f"{kind}:{provider}:{query}:{limit}"
        cached = _cache.get(cache_key)
        if cached and time.time() - cached[0] < CACHE_TTL:
            result.extend(cached[1])
            statuses.append({"provider": provider, "status": "cached", "count": len(cached[1])})
            continue
        try:
            headers = {}
            if provider == "scholarshipowl":
                headers["SCHOLARSHIP-APP-API-Key"] = os.environ["SCHOLARSHIPOWL_API_KEY"]
            payload = _get_json(_url(template, query, limit), headers)
            normalized = [(_normalise_course(item, provider) if kind == "course" else _normalise_scholarship(item, provider)) for item in _items(payload)]
            normalized = normalized[:limit]
            _cache[cache_key] = (time.time(), normalized)
            result.extend(normalized)
            statuses.append({"provider": provider, "status": "ok", "count": len(normalized)})
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
            statuses.append({"provider": provider, "status": "error", "count": 0, "message": str(exc)})
    return result, statuses