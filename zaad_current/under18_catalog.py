"""Verified opportunities suitable for learners under 18.
All entries use official first-party sources checked on 2026-08-29.
"""
from datetime import datetime, timezone
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "opportunities.db"
TODAY = "2026-08-30"

UNDER18_OPPORTUNITIES = [
    {
        "slug": "u18-google-gemini-certified-student",
        "type": "course",
        "title": "Gemini Certified Student — شهادة Google للطلاب من 13 سنة",
        "organization": "Google for Education",
        "description": "مسار رسمي من Google for Education مخصص لطلاب K-12، ويتيح للطلاب من عمر 13 سنة فأكثر الاستعداد لاختبار Gemini Certified Student والحصول على شهادة مجانية صالحة لمدة ثلاث سنوات وفق صفحة Google الرسمية. البرنامج مناسب للطلاب تحت 18 سنة الذين يريدون إضافة اعتماد رسمي من Google إلى سجلهم التعليمي.",
        "about_opportunity": "تقدم Google for Education اعتماد Gemini Certified Student للطلاب في مرحلة K-12. صفحة Google الرسمية توضح أن الشهادة متاحة للطلاب من عمر 13 سنة فأكثر ومجانية، مع صلاحية ثلاث سنوات. يبدأ الطالب بالمادة التحضيرية الرسمية ثم يؤدي الاختبار للحصول على الشهادة إذا استوفى متطلبات Google.",
        "country": "أونلاين / عالمي",
        "online": 1,
        "age_min": 13,
        "age_max": 17,
        "education_level": "المرحلة الثانوية وطلاب K-12",
        "category": "الذكاء الاصطناعي والمهارات الرقمية",
        "language": "الإنجليزية",
        "funding_type": "مجاني بالكامل",
        "tuition_covered": 1,
        "accommodation": 0,
        "meals": 0,
        "travel": 0,
        "stipend": "لا يوجد",
        "duration": "حسب وقت الاستعداد والاختبار",
        "certificate": 1,
        "deadline": "مفتوح حسب توفر التسجيل والاختبار",
        "application_url": "https://edu.google.com/learning-center/",
        "official_source": "https://edu.google.com/learning-center/",
        "eligibility": json.dumps([
            "البرنامج مخصص لطلاب K-12.",
            "الاختبار متاح للطلاب بعمر 13 سنة فأكثر وفق Google for Education.",
            "يجب مراجعة صفحة التسجيل الرسمية لمعرفة أي متطلبات حساب أو بلد أو مدرسة وقت التسجيل."
        ], ensure_ascii=False),
        "requirements": json.dumps([
            "إنشاء/استخدام حساب مناسب للتسجيل.",
            "مراجعة مادة Enhance Your Learning with Gemini الرسمية قبل الاختبار.",
            "إكمال متطلبات الاختبار المنشورة من Google وقت التسجيل."
        ], ensure_ascii=False),
        "required_documents": json.dumps([
            "لا توجد مستندات أكاديمية معلنة كشرط عام في صفحة البرنامج.",
            "قد يطلب النظام بيانات الحساب أو التحقق من أهلية الطالب."
        ], ensure_ascii=False),
        "application_steps": json.dumps([
            "افتح صفحة Google for Education الرسمية.",
            "انتقل إلى قسم Gemini Certified Student للطلاب.",
            "راجع المادة التحضيرية الرسمية.",
            "سجّل للاختبار عندما يكون التسجيل متاحًا لحسابك.",
            "أكمل الاختبار وفق تعليمات Google.",
            "بعد النجاح، اتبع تعليمات Google للحصول على الشهادة الرقمية."
        ], ensure_ascii=False),
        "keywords": json.dumps(["تحت 18", "13-17", "ثانوي", "جوجل", "Google", "Gemini", "شهادة"], ensure_ascii=False),
    },
    {
        "slug": "u18-ibm-skillsbuild-high-school",
        "type": "course",
        "title": "IBM SkillsBuild لطلاب الثانوية — تعلم تقني مجاني وشهادات رقمية",
        "organization": "IBM SkillsBuild",
        "description": "منصة IBM الرسمية للطلاب في المرحلة الثانوية، وتستهدف الطلاب من 13 إلى 18 عامًا. توفر تعلمًا رقميًا مجانيًا في الذكاء الاصطناعي والأمن السيبراني والبيانات والتصميم والبرمجيات والسحابة، مع إمكانية الحصول على شارات واعتمادات رقمية من IBM بحسب المسار المكتمل.",
        "about_opportunity": "IBM SkillsBuild يقدم مسارات تعلم مجانية لطلاب المدارس الثانوية في مرحلة استكشاف المستقبل المهني. الكتالوج الرسمي يحدد مسار الثانوية للطلاب من 13 إلى 18 عامًا ويضم موضوعات مثل الذكاء الاصطناعي والأمن السيبراني والبيانات والبرمجيات والسحابة. بعض المسارات تؤهل للحصول على IBM Digital Credentials، ويختلف نوع الاعتماد حسب النشاط أو المسار.",
        "country": "أونلاين / عالمي",
        "online": 1,
        "age_min": 13,
        "age_max": 17,
        "education_level": "المرحلة الثانوية",
        "category": "البرمجة والذكاء الاصطناعي والأمن السيبراني",
        "language": "متعدد اللغات",
        "funding_type": "مجاني بالكامل",
        "tuition_covered": 1,
        "accommodation": 0,
        "meals": 0,
        "travel": 0,
        "stipend": "لا يوجد",
        "duration": "من أقل من ساعة إلى مسارات أطول حسب الكورس",
        "certificate": 1,
        "deadline": "مفتوح",
        "application_url": "https://skillsbuild.org/learning-catalog/high-school-catalog",
        "official_source": "https://skillsbuild.org/learning-catalog/high-school-catalog",
        "eligibility": json.dumps([
            "طلاب المدارس الثانوية في المسار المخصص للمرحلة الثانوية.",
            "العمر المستهدف في الكتالوج الرسمي 13–18 عامًا.",
            "قد تتطلب بعض إجراءات التسجيل موافقة ولي الأمر بحسب قوانين السن الرقمي في بلد الطالب."
        ], ensure_ascii=False),
        "requirements": json.dumps([
            "حساب IBM SkillsBuild.",
            "اختيار مسار High School أو الكتالوج المخصص للثانوية.",
            "إكمال أنشطة التعلم أو الاختبارات المطلوبة لأي اعتماد رقمي محدد."
        ], ensure_ascii=False),
        "required_documents": json.dumps([
            "لا توجد أوراق دراسية عامة مطلوبة لبدء الكورسات المجانية.",
            "قد تُطلب موافقة ولي الأمر للطلاب دون سن الموافقة الرقمية في بلدهم."
        ], ensure_ascii=False),
        "application_steps": json.dumps([
            "افتح كتالوج IBM SkillsBuild للمرحلة الثانوية.",
            "أنشئ حسابًا مجانيًا واختر أنك طالب ثانوي.",
            "اختر مجالًا مثل AI أو Cybersecurity أو Data أو Software Development.",
            "ابدأ الكورس أو المسار المناسب.",
            "أكمل المتطلبات المحددة للكورس أو الاعتماد الرقمي.",
            "تحقق من قسم Digital Credentials في حسابك لمعرفة الاعتمادات التي أصبحت مؤهلاً لها."
        ], ensure_ascii=False),
        "keywords": json.dumps(["تحت 18", "13-18", "ثانوي", "IBM", "SkillsBuild", "تدريب", "شهادة", "ذكاء اصطناعي"], ensure_ascii=False),
    },
    {
        "slug": "u18-openlearn-free-courses",
        "type": "course",
        "title": "OpenLearn — كورسات مجانية مع Statement of Participation للطلاب",
        "organization": "The Open University",
        "description": "OpenLearn هي منصة التعلم المجاني التابعة للجامعة المفتوحة في بريطانيا. لا يوجد حد أدنى لاستخدام المحتوى، وإنشاء الحساب متاح من عمر 13 سنة، وبعد إكمال الكورس وفق شروطه يمكن الحصول على Statement of Participation مجاني، وبعض الكورسات تمنح Digital Badge مجانيًا.",
        "about_opportunity": "توفر OpenLearn مئات الدورات المجانية في موضوعات أكاديمية ومهارية متنوعة. الصفحة الرسمية تؤكد أن إنشاء الحساب متاح لمن بلغ 13 عامًا فأكثر، وأن إكمال الكورسات المؤهلة يتيح Statement of Participation مجانيًا، وبعضها يتيح شارة رقمية مجانية. هذه الوثيقة ليست مؤهلًا جامعيًا رسميًا ولا تحمل رصيدًا أكاديميًا.",
        "country": "أونلاين / المملكة المتحدة",
        "online": 1,
        "age_min": 13,
        "age_max": 17,
        "education_level": "ثانوي / تعلم ذاتي",
        "category": "مجالات متعددة",
        "language": "الإنجليزية",
        "funding_type": "مجاني بالكامل",
        "tuition_covered": 1,
        "accommodation": 0,
        "meals": 0,
        "travel": 0,
        "stipend": "لا يوجد",
        "duration": "متغير حسب الكورس",
        "certificate": 1,
        "deadline": "مفتوح",
        "application_url": "https://www.open.edu/openlearn/free-courses",
        "official_source": "https://www.open.edu/openlearn/free-courses",
        "eligibility": json.dumps([
            "لا يوجد حد أدنى لاستخدام الموقع والمحتوى العام.",
            "إنشاء حساب OpenLearn متاح من عمر 13 سنة فأكثر.",
            "كل كورس قد يحدد مستوى الدراسة والمتطلبات السابقة الخاصة به."
        ], ensure_ascii=False),
        "requirements": json.dumps([
            "إنشاء حساب مجاني إذا أردت التسجيل وتتبع التقدم والحصول على Statement of Participation.",
            "قراءة صفحات الكورس المطلوبة وإكمال الاختبارات الإلزامية عند وجودها."
        ], ensure_ascii=False),
        "required_documents": json.dumps([
            "لا توجد مستندات أكاديمية عامة مطلوبة للكورسات المجانية.",
            "قد تختلف متطلبات بعض الكورسات، لذلك يجب قراءة صفحة الكورس المحدد."
        ], ensure_ascii=False),
        "application_steps": json.dumps([
            "افتح كتالوج OpenLearn المجاني.",
            "اختر الكورس المناسب لمستواك.",
            "أنشئ حسابًا مجانيًا بعمر 13 سنة فأكثر إذا كنت تريد التسجيل.",
            "سجّل في الكورس وأكمل جميع الصفحات والاختبارات المطلوبة.",
            "بعد الإكمال، افتح قسم Achievements في ملفك.",
            "نزّل Statement of Participation أو الشارة الرقمية إذا كان الكورس مؤهلًا لها."
        ], ensure_ascii=False),
        "keywords": json.dumps(["تحت 18", "13+", "ثانوي", "OpenLearn", "الجامعة المفتوحة", "شهادة", "badge"], ensure_ascii=False),
    },
    {
        "slug": "u18-zooniverse-citizen-science",
        "type": "volunteer",
        "title": "Zooniverse — تطوع علمي أونلاين للطلاب والمراهقين",
        "organization": "Zooniverse / Oxford University",
        "description": "منصة بحث علمي تشاركي تسمح للمتطوعين بمساعدة فرق بحث حقيقية في تحليل صور وبيانات ومشروعات في الفلك والبيئة والحياة البرية وغيرها. Zooniverse توضح أن المشاركة مفتوحة لجميع الأعمار، وأن من هم دون 16 عامًا يحتاجون موافقة ولي الأمر قبل إنشاء حسابهم الخاص، كما تتوفر شهادات تطوع في بعض المشروعات.",
        "about_opportunity": "يتيح Zooniverse للطلاب المشاركة في أبحاث علمية حقيقية عبر الإنترنت دون الحاجة إلى شهادة جامعية أو خبرة بحثية متقدمة. يختار الطالب مشروعًا مناسبًا ثم يتعلم من الدليل التعليمي ويبدأ تصنيف البيانات أو الصور. بعض مشروعات Zooniverse توفر شهادات توثق وقت التطوع، بينما تختلف طريقة إصدارها حسب المشروع.",
        "country": "أونلاين / عالمي",
        "online": 1,
        "age_min": 0,
        "age_max": 17,
        "education_level": "ثانوي / جميع المستويات",
        "category": "تطوع علمي وبحث علمي",
        "language": "الإنجليزية",
        "funding_type": "مجاني بالكامل",
        "tuition_covered": 1,
        "accommodation": 0,
        "meals": 0,
        "travel": 0,
        "stipend": "لا يوجد",
        "duration": "مرن حسب المشروع",
        "certificate": 1,
        "deadline": "مفتوح حسب المشروع",
        "application_url": "https://www.zooniverse.org/projects",
        "official_source": "https://www.zooniverse.org/",
        "eligibility": json.dumps([
            "Zooniverse تذكر أن جميع الأعمار يمكنها المشاركة في مشروعاتها.",
            "الأطفال دون 16 عامًا يحتاجون موافقة ولي الأمر قبل إنشاء حسابهم الخاص وفق إرشادات Zooniverse المنشورة.",
            "قد تكون بعض المشروعات الفردية لها متطلبات أو تعليمات إضافية."
        ], ensure_ascii=False),
        "requirements": json.dumps([
            "اتصال بالإنترنت وحساب Zooniverse إذا أردت حفظ سجل مشاركتك.",
            "قراءة Tutorial أو Field Guide الخاص بالمشروع قبل التصنيف.",
            "اختيار مشروع مناسب للعمر والقدرات."
        ], ensure_ascii=False),
        "required_documents": json.dumps([
            "لا توجد مستندات أكاديمية عامة.",
            "لمن هم دون 16 عامًا: موافقة ولي الأمر مطلوبة قبل إنشاء الحساب وفق إرشادات Zooniverse."
        ], ensure_ascii=False),
        "application_steps": json.dumps([
            "افتح قائمة مشروعات Zooniverse.",
            "اختر مشروعًا علميًا مناسبًا.",
            "اقرأ صفحة About والدليل التعليمي.",
            "أنشئ حسابًا إذا أردت تسجيل ساعات ومساهماتك، مع الالتزام بمتطلبات العمر.",
            "ابدأ مهام التصنيف أو تحليل البيانات.",
            "تحقق من قسم الإحصاءات أو تعليمات المشروع لمعرفة إمكانية إصدار شهادة تطوع."
        ], ensure_ascii=False),
        "keywords": json.dumps(["تحت 18", "أقل من 16", "تطوع", "أونلاين", "Zooniverse", "بحث علمي", "شهادة تطوع"], ensure_ascii=False),
    },
    {
        "slug": "u18-nasa-citizen-science",
        "type": "volunteer",
        "title": "NASA Citizen Science — مشروعات علمية أونلاين لجميع الأعمار",
        "organization": "NASA Science",
        "description": "بوابة NASA الرسمية لمشروعات Citizen Science التي تتيح للجمهور المساعدة في أبحاث حقيقية في الفضاء والأرض والمناخ. NASA تؤكد أن العمر ليس عائقًا في مشروعات citizen science، وتضم القائمة مشروعات أونلاين يمكن تنفيذها من المنزل.",
        "about_opportunity": "تفتح NASA باب المشاركة في العلم الحقيقي أمام الجمهور من خلال مشروعات Citizen Science. يمكن للطلاب تحليل صور وبيانات أو تنفيذ ملاحظات ومهام بحثية تساعد العلماء في موضوعات مثل الكواكب والنجوم والأرض والمناخ. بعض المشروعات تعليمية ومناسبة للطلاب، وتختلف طريقة المشاركة والمهام من مشروع إلى آخر.",
        "country": "أونلاين / عالمي",
        "online": 1,
        "age_min": 0,
        "age_max": 17,
        "education_level": "طلاب المدارس / جميع الأعمار",
        "category": "علوم وفلك وبيئة",
        "language": "الإنجليزية",
        "funding_type": "مجاني بالكامل",
        "tuition_covered": 1,
        "accommodation": 0,
        "meals": 0,
        "travel": 0,
        "stipend": "لا يوجد",
        "duration": "مرن حسب المشروع",
        "certificate": 0,
        "deadline": "مفتوح حسب المشروع",
        "application_url": "https://science.nasa.gov/citizen-science/",
        "official_source": "https://science.nasa.gov/get-involved/citizen-science/how-to-contribute-to-citizen-science/",
        "eligibility": json.dumps([
            "NASA توضح أن الناس من جميع الأعمار يمكنهم المشاركة في Citizen Science.",
            "بعض المشروعات موجهة أو مناسبة لفئات عمرية محددة، لذلك يجب قراءة صفحة المشروع قبل البدء.",
            "لا يشترط أن يكون المشارك مواطنًا أمريكيًا في مشروعات Citizen Science العامة."
        ], ensure_ascii=False),
        "requirements": json.dumps([
            "هاتف أو كمبيوتر واتصال بالإنترنت بحسب المشروع.",
            "قراءة تعليمات المشروع والتدريب القصير قبل تنفيذ المهمة.",
            "بعض المشاريع قد تتطلب تطبيقًا أو أدوات إضافية."
        ], ensure_ascii=False),
        "required_documents": json.dumps([
            "لا توجد مستندات أكاديمية عامة مطلوبة للمشاركة في Citizen Science.",
            "تحقق من شروط المشروع المحدد إذا طلب تسجيلًا أو تطبيقًا خاصًا."
        ], ensure_ascii=False),
        "application_steps": json.dumps([
            "افتح بوابة NASA Citizen Science.",
            "استعرض المشروعات الحالية واختر مشروعًا أونلاين مناسبًا.",
            "اقرأ وصف المشروع وتعليماته.",
            "ثبّت التطبيق أو افتح أداة المشاركة إذا كانت مطلوبة.",
            "نفّذ المهام أو حلّل البيانات وفق الإرشادات.",
            "احتفظ بسجل مشاركتك إذا كنت تحتاج إلى توثيق نشاطك المدرسي."
        ], ensure_ascii=False),
        "keywords": json.dumps(["تحت 18", "جميع الأعمار", "تطوع", "NASA", "ناسا", "علوم", "فلك", "أونلاين"], ensure_ascii=False),
    },
    {
        "slug": "u18-unicef-u-report",
        "type": "program",
        "title": "UNICEF U-Report — منصة مشاركة رقمية للشباب من 13 سنة",
        "organization": "UNICEF",
        "description": "U-Report منصة رقمية عالمية مدعومة من UNICEF تتيح للمراهقين والشباب التعبير عن آرائهم والمشاركة في استطلاعات وحوارات حول قضايا التعليم والمناخ والصحة وحقوق الطفل وغيرها. الحد العمري يختلف حسب البرنامج المحلي، وتؤكد مصادر UNICEF أن المنصة تستهدف الشباب من 13 عامًا في عدد من الدول.",
        "about_opportunity": "U-Report ليست وظيفة تطوعية تقليدية، بل منصة مشاركة وتمكين شبابي رقمية. يستطيع المراهقون في الدول التي يتوفر فيها البرنامج المشاركة في الاستطلاعات والحوارات والمبادرات المحلية، وقد تنشر المنصة فرصًا إضافية مثل ورش العمل والفعاليات. يجب اختيار U-Report المحلي لأن آلية التسجيل والعمر والفرص تختلف حسب الدولة.",
        "country": "أونلاين / حسب الدولة",
        "online": 1,
        "age_min": 13,
        "age_max": 17,
        "education_level": "طلاب المدارس والشباب",
        "category": "مشاركة شبابية ومجتمعية",
        "language": "حسب U-Report المحلي",
        "funding_type": "مجاني",
        "tuition_covered": 1,
        "accommodation": 0,
        "meals": 0,
        "travel": 0,
        "stipend": "لا يوجد",
        "duration": "مرن",
        "certificate": 0,
        "deadline": "مفتوح حسب الدولة والحملة",
        "application_url": "https://www.unicef.org/innovation/ureport",
        "official_source": "https://www.unicef.org/innovation/ureport",
        "eligibility": json.dumps([
            "تستهدف U-Report الشباب والمراهقين، ويختلف نطاق العمر حسب الدولة.",
            "توجد برامج محلية موثقة تستقبل المشاركين من عمر 13 عامًا.",
            "يجب التأكد من صفحة U-Report المحلية في بلد الطالب قبل التسجيل."
        ], ensure_ascii=False),
        "requirements": json.dumps([
            "هاتف أو حساب مراسلة/قناة رقمية يدعمها برنامج U-Report المحلي.",
            "الموافقة على شروط الخصوصية والاستخدام المحلية.",
            "اتباع تعليمات التسجيل التي تحددها UNICEF أو الشريك المحلي."
        ], ensure_ascii=False),
        "required_documents": json.dumps([
            "لا توجد مستندات أكاديمية عامة للمشاركة في الاستطلاعات.",
            "قد تختلف بيانات التسجيل المطلوبة حسب الدولة والقناة المستخدمة."
        ], ensure_ascii=False),
        "application_steps": json.dumps([
            "افتح صفحة U-Report الرسمية.",
            "حدد U-Report المتاح في بلدك.",
            "اقرأ شروط العمر والخصوصية المحلية.",
            "سجّل عبر القناة الرسمية مثل الموقع أو WhatsApp أو Messenger إذا كانت متاحة.",
            "شارك في الاستطلاعات والأنشطة الرقمية.",
            "تابع الإعلانات المحلية لمعرفة ورش العمل أو فرص المشاركة الجديدة."
        ], ensure_ascii=False),
        "keywords": json.dumps(["تحت 18", "13+", "UNICEF", "يونيسف", "U-Report", "شباب", "مشاركة", "تطوع"], ensure_ascii=False),
    },
]

def merge_under18_catalog():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    for item in UNDER18_OPPORTUNITIES:
        exists = conn.execute("SELECT 1 FROM opportunities WHERE slug=?", (item["slug"],)).fetchone()
        if exists:
            continue
        conn.execute(
            """INSERT INTO opportunities
            (slug,type,title,organization,description,country,online,age_min,age_max,education_level,category,language,
             funding_type,tuition_covered,accommodation,meals,travel,stipend,duration,certificate,deadline,application_url,
             official_source,source_type,verified,status,last_checked,eligibility,requirements,required_documents,application_steps)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                item["slug"], item["type"], item["title"], item["organization"], item["description"], item["country"],
                item["online"], item["age_min"], item["age_max"], item["education_level"], item["category"], item["language"],
                item["funding_type"], item["tuition_covered"], item["accommodation"], item["meals"], item["travel"],
                item["stipend"], item["duration"], item["certificate"], item["deadline"], item["application_url"],
                item["official_source"], "official", 1, "open", TODAY, item["eligibility"], item["requirements"],
                item["required_documents"], item["application_steps"]
            )
        )
        conn.execute("UPDATE opportunities SET keywords=? WHERE slug=?", (item["keywords"], item["slug"]))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    merge_under18_catalog()
