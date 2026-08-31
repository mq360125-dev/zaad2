# Global Opportunities Platform — FastAPI

تم تطوير المشروع الحالي **بدون إعادة بنائه من الصفر**. البنية الأصلية كانت FastAPI + SQLite + Static Frontend، وتم الحفاظ عليها مع إضافة دليل منصات، كورسات، فرص موحدة، صفحات منصات، API filtering/pagination، Admin API/Dashboard، وOfficial API importer.

## ما تم فحصه أولًا
- Framework: FastAPI 0.115.6
- Database: SQLite (`opportunities.db`)
- Frontend: HTML/CSS/JavaScript داخل `static/`
- البيانات الأصلية: `seed.py` + SQLite
- لا يوجد ORM، لذلك تم الإبقاء على SQLite/raw SQL لتقليل التغييرات.

## الملفات الجديدة
- `importers.py` — importers لمصادر رسمية فقط؛ حاليًا ScholarshipOwl Business API.
- `static/platform.html` — صفحة تفصيلية لكل منصة (`/platform/{slug}`).
- `static/admin.html` — لوحة الإدارة.
- `.env.example` — متغيرات الأسرار.

## الملفات المعدلة
- `main.py` — endpoints، pagination، aliases للمنح/التطوع/المسابقات، حماية Admin، صفحة المنصة ولوحة الإدارة.
- `static/app.js` — روابط صفحات المنصات.
- `update_sources.py` — تحديث التحقق وتشغيل importers الرسمية.
- `requirements.txt` — نفس dependencies الأساسية؛ لا توجد dependency خارجية جديدة.

## نماذج البيانات
- `Platform`
- `Course`
- `Opportunity` كأساس موحد للفرص، مع `type=scholarship|volunteer|competition|internship|program`.
- `Scholarship`, `VolunteerOpportunity`, `Competition` ممثلة كأنواع متخصصة داخل Opportunity لتجنب تكرار البيانات في SQLite.

كل سجل يحتفظ بـ `source_type`, `official_source/source`, `verified`, `last_checked`.

مصادر البيانات المقصودة:
1. API
2. RSS/Feed
3. Official public data
4. Manual verified data
5. Official website

لا يوجد scraping عشوائي.

## Seed
```bash
python seed.py --reset
```

Seed الحالي يحتوي على 17 منصة، 16 كورسًا، و22 فرصة أولية منها 9 منح، مع روابط رسمية فقط. إذا لم تكن معلومة مؤكدة لا يتم تحويلها إلى ادعاء مؤكد.

## التشغيل
```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python seed.py --reset
uvicorn main:app --reload
```

الواجهة: `http://127.0.0.1:8000/`

صفحة المنصة: `http://127.0.0.1:8000/platform/google`

صفحة تفاصيل الفرصة: `http://127.0.0.1:8000/opportunity/1`

صفحة تفاصيل الكورس: `http://127.0.0.1:8000/course/1`

لوحة الإدارة: `http://127.0.0.1:8000/admin`

## Admin
قبل تشغيل الإنتاج:
```bash
set ADMIN_TOKEN=ضع_سرًا_طويلًا_هنا
```
على Linux/macOS:
```bash
export ADMIN_TOKEN='ضع-سرًا-طويلًا-هنا'
```

كل `/api/admin/*` محمي بـ `X-Admin-Token`. إذا لم يتم ضبط `ADMIN_TOKEN` يبقى Admin API معطلًا.

## API
```text
GET /api/platforms
GET /api/platforms/{slug}
GET /api/courses
GET /api/courses/{id}
GET /api/opportunities
GET /api/opportunities/{id}
GET /api/scholarships
GET /api/volunteering
GET /api/competitions
GET /api/meta
GET /api/health
GET /api/live?type=course&search=python
GET /api/live?type=scholarship&search=engineering
```

أمثلة:
```text
/api/courses?free=true
/api/courses?certificate=true
/api/courses?platform=huawei
/api/opportunities?type=scholarship&funding=Fully%20Funded
/api/volunteering?online=true
/api/competitions?age=16
/api/opportunities?country=Egypt&page=1&page_size=24
```

## Admin API
```text
POST   /api/admin/platforms
PUT    /api/admin/platforms/{id}
DELETE /api/admin/platforms/{id}
POST   /api/admin/courses
DELETE /api/admin/courses/{id}
POST   /api/admin/opportunities
PATCH  /api/admin/opportunities/{id}
DELETE /api/admin/opportunities/{id}
PATCH  /api/admin/courses/{id}/verification?verified=true
PATCH  /api/admin/opportunities/{id}/verification?verified=true
GET    /api/admin/stats
```

## تحديث المصادر
```bash
python update_sources.py
```

### ScholarshipOwl
الـ API الرسمي يستخدم JSON:API، ويدعم `GET /api/scholarship` مع pagination بصيغة `page[number]` و`page[size]`. لا تضع مفتاح API داخل الكود.

اضبط:
```bash
SCHOLARSHIPOWL_API_KEY=your-api-key
```
ثم:
```bash
python update_sources.py
```

إذا لم يوجد المفتاح، يتم تخطي importer بدل إيقاف المشروع.

### Live APIs
`/api/live` يجمع النتائج من كل عنوان JSON رسمي تضعه في `LIVE_COURSE_API_URLS` أو
`LIVE_SCHOLARSHIP_API_URLS`، ويعيد `providers` بحالة كل مزود. يدعم القالبين `{query}` و`{limit}`،
ويستخدم cache مؤقتًا وtimeout مستقلًا حتى لا يؤدي تعطل مصدر واحد إلى تعطيل الموقع. كما يدعم
ScholarshipOwl تلقائيًا عند ضبط `SCHOLARSHIPOWL_API_KEY`.

مهم: الـ importer لا يخمّن المنظمة أو الدولة أو التمويل أو شروط الأهلية عندما لا يعيدها المصدر؛ يتركها `Unknown`.

## إضافة منصة جديدة
من Admin Dashboard أو:
```text
POST /api/admin/platforms
```
استخدم `platform_id` في الكورسات بدل تكرار اسم المنصة.

## إضافة Course يدويًا
```text
POST /api/admin/courses
```
ويجب أن يكون `platform_id` موجودًا، مع `official_url` و`source`.

## إضافة Scholarship يدويًا
استخدم:
```text
POST /api/admin/opportunities
```
مع:
```json
{
  "type": "scholarship",
  "title": "...",
  "organization": "...",
  "funding_type": "Fully Funded",
  "application_url": "https://official.example/apply",
  "official_source": "https://official.example/page"
}
```

## Architecture
```text
Official API / RSS / Public Data / Manual Verified Data
                         ↓
                    Importers
                         ↓
                   Normalization
                         ↓
                    Validation
                         ↓
                       SQLite
                         ↓
                    FastAPI API
                         ↓
                      Frontend
```

المشروع لا يعتمد على وجود API لكل منصة؛ المنصة يمكن أن تكون موجودة في دليل الموقع بمعلومات وروابط رسمية حتى لو كانت بياناتها Manual.
\n\n### Expanded catalog\nThe bundled catalog now targets 100+ scholarships, 100+ volunteering opportunities, 100+ programs/other opportunities, and 100+ platform/organization profiles.\nAll newly added records use official organization URLs and intentionally avoid inventing fixed deadlines or financial amounts when the official source varies by cycle. Last checked: 2026-08-28.\n

## Catalog target

This build keeps the legacy embedded catalog and adds the expanded catalog. The SQLite database is seeded with exactly 500 scholarship records and at least 500 non-scholarship opportunity records, plus the existing course and platform catalog. Records with cycle-dependent details are marked `check_source` so the site does not imply a deadline or amount that was not verified for the current cycle.

## إضافات المحتوى الرسمية — 2026-08-29
تمت إضافة كتالوج تكميلي **بدون حذف الكتالوج السابق** عبر `supplemental_catalog.py`، ويشمل:
- منح وفرص رسمية من فرنسا، ألمانيا، هولندا، المجر، كوريا الجنوبية، اليابان، روسيا، المملكة المتحدة، كندا.
- مسارات لغات رسمية/مؤسسية للفرنسية والألمانية واليابانية والإسبانية والروسية والإيطالية والتركية والهولندية والصينية.
- فرص تطوع وبرامج ومسابقات وتدريبات إضافية بمصادر رسمية.
- كل إضافة تحمل رابط المصدر الرسمي وحالة `check_source` عندما تكون الشروط أو المواعيد متغيرة.

لتحديث قاعدة البيانات بعد فك الضغط:
```bash
python seed.py
```
ولا تستخدم `--reset` إذا أردت الاحتفاظ بأي بيانات أضفتها يدويًا خارج ملفات seed.


## تحديث 2026-08-30
- 172 منصة، 253 كورسًا، 961 فرصة.
- 17 فرصة/موردًا مصنفًا تحت 18، تشمل كورسات وشهادات وتطوعًا علميًا أونلاين.
- بطاقات الفرص والكورسات والمنصات تفتح صفحات التفاصيل مباشرة.
- أزيل اختصار Ctrl+K من الواجهة.
- تفاصيل الفرص تتضمن الوصف، الأهلية، المتطلبات، المستندات، خطوات التقديم، والمصدر الرسمي.
