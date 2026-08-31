import json
from datetime import date

PLATFORMS = [
('tv5monde-apprendre','TV5MONDE – Apprendre le français','منصة فرنسية مجانية لتعلم الفرنسية عبر الفيديو والأنشطة من مستويات متعددة. لا تصدر DELF/DALF نفسها.','https://apprendre.tv5monde.com','https://apprendre.tv5monde.com','https://apprendre.tv5monde.com','France / Global',['French'],1,0,'التعلم مجاني؛ شهادة DELF/DALF الرسمية ليست من TV5MONDE.'),
('rfi-savoirs-french','RFI Savoirs – Français facile','موارد RFI المجانية لتعلم الفرنسية عبر الأخبار والملفات الصوتية والتمارين.','https://savoirs.rfi.fr','https://savoirs.rfi.fr/fr/apprendre-enseigner','https://savoirs.rfi.fr','France / Global',['French'],1,0,'المحتوى مجاني، ولا توجد شهادة لغة رسمية مجانية عامة معلنة.'),
('goethe-free-german','Goethe-Institut – Deutsch üben','تمارين مجانية من Goethe-Institut للألمانية تشمل تطبيقات وفيديوهات وبودكاست ومجتمع Deutsch für dich.','https://www.goethe.de/en/spr/ueb.html','https://www.goethe.de/en/spr/ueb.html','https://www.goethe.de/en/spr/kup/prf.html','Germany / Global',['German'],1,0,'التدريب مجاني؛ Goethe-Zertifikat امتحان رسمي منفصل وليس مجانيًا عادة.'),
('nhk-easy-japanese','NHK WORLD-JAPAN – Easy Japanese','دروس يابانية مجانية للمبتدئين عبر حوارات ومفردات وملفات صوتية.','https://www3.nhk.or.jp/nhkworld/en/learnjapanese/','https://www3.nhk.or.jp/nhkworld/en/learnjapanese/','https://www3.nhk.or.jp/nhkworld/en/learnjapanese/','Japan / Global',['Japanese'],1,0,'الدروس مجانية ولا توجد شهادة عامة مجانية معلنة في المصدر.'),
('cervantes-ave','Instituto Cervantes – AVE Global','منصة Instituto Cervantes الرسمية لتعلم الإسبانية وفق مستويات CEFR. الوصول والشهادة يختلفان حسب العرض.','https://ave.cervantes.es','https://ave.cervantes.es','https://examenes.cervantes.es','Spain / Global',['Spanish'],0,1,'تحقق من العرض الحالي؛ DELE/SIELE امتحانات رسمية منفصلة.'),
('rai-scuola-italiano','Rai Scuola – Italiano','موارد مجانية من Rai Scuola لممارسة الإيطالية عبر فيديوهات وبرامج تعليمية.','https://www.raiscuola.rai.it/italiano','https://www.raiscuola.rai.it/italiano','https://www.raiscuola.rai.it/italiano','Italy / Global',['Italian'],1,0,'المحتوى مجاني ولا توجد شهادة لغة رسمية مجانية عامة معلنة.'),
('pushkin-russian','Pushkin Institute – Russian','مورد روسي متخصص في تعليم الروسية كلغة أجنبية مع مواد ودورات رقمية.','https://pushkininstitute.ru','https://pushkininstitute.ru/learn','https://pushkininstitute.ru','Russia / Global',['Russian'],1,1,'المسارات المجانية تختلف؛ تحقق من صفحة الدورة قبل اعتبار الشهادة مجانية.'),
('sejong-korean','Online King Sejong Institute – Korean','منصة معهد الملك سيجونغ لتعلم الكورية عبر الإنترنت بمسارات منظمة.','https://www.iksi.or.kr','https://www.iksi.or.kr/lms/main/main.do','https://www.iksi.or.kr','South Korea / Global',['Korean'],1,1,'المواد مجانية حسب المسار؛ تحقق من الشهادة داخل الدورة.'),
('chineseplus','ChinesePlus','موارد رقمية لتعلم الصينية من مؤسسات تعليمية صينية، تشمل النطق والمفردات والاستماع.','https://www.chineseplus.net','https://www.chineseplus.net','https://www.chineseplus.net','China / Global',['Chinese'],1,0,'المحتوى المجاني يختلف حسب المورد ولا نثبت شهادة مجانية عامة دون إعلان رسمي.'),
('rug-language-centre','University of Groningen Language Centre','موارد ودورات للغات، ومنها الهولندية، مرتبطة بجامعة Groningen.','https://www.rug.nl/language-centre/','https://www.rug.nl/language-centre/','https://www.rug.nl/language-centre/','Netherlands',['Dutch'],1,0,'ابدأ بالموارد المفتوحة وتحقق من تكلفة الدورة والشهادة المحددة.'),
('navoica-polish-plus','NAVOICA – Polish MOOCs','منصة MOOCs بولندية مفتوحة تحتوي دورات لغة بولندية مجانية، وبعضها يمنح شهادة إتمام وفق شروط الدورة.','https://navoica.pl','https://navoica.pl','https://navoica.pl','Poland',['Polish'],1,1,'أكمل وحدات الدورة والاختبار، ثم تحقق من شروط شهادة الإتمام الخاصة بالدورة.'),
]

COURSES = [
('tv5monde-french-a1','Première classe – French A1','tv5monde-apprendre','مسار مجاني للمبتدئين في الفرنسية عبر فيديوهات وأنشطة للحياة اليومية والاستماع والمفردات.','لغات','مبتدئ','French','ذاتي',1,0,'لا توجد شهادة رسمية عامة معلنة','مجاني','لا','https://apprendre.tv5monde.com/fr','official'),
('rfi-french-easy','Le français facile avec RFI','rfi-savoirs-french','تعلم الفرنسية من خلال الأخبار والملفات الصوتية والتمارين، مناسب من المبتدئ إلى المتقدم.','لغات','مبتدئ إلى متقدم','French','ذاتي',1,0,'لا توجد شهادة عامة معلنة','مجاني','لا','https://savoirs.rfi.fr/fr/apprendre-enseigner','official'),
('goethe-deutsch-free','Deutsch üben – Goethe-Institut','goethe-free-german','تمارين مجانية في الألمانية للمفردات والاستماع والقراءة والنطق مع مستويات متعددة.','لغات','مبتدئ إلى متقدم','German','ذاتي',1,0,'لا توجد شهادة مجانية عامة؛ امتحان Goethe منفصل','مجاني','لا','https://www.goethe.de/en/spr/ueb.html','official'),
('nhk-easy-japanese-course','Easy Japanese – NHK WORLD-JAPAN','nhk-easy-japanese','دروس يابانية مجانية للمبتدئين عبر حوارات قصيرة وملفات صوتية ومفردات.','لغات','مبتدئ','Japanese','ذاتي',1,0,'لا توجد شهادة مجانية عامة معلنة','مجاني','لا','https://www3.nhk.or.jp/nhkworld/en/learnjapanese/','official'),
('cervantes-ave-global','AVE Global – Spanish','cervantes-ave','دورات إسبانية منظمة وفق مستويات CEFR من Instituto Cervantes. الوصول الكامل والشهادة يعتمدان على المسار الحالي.','لغات','A1–C1','Spanish','متغير',0,1,'شهادة حسب المسار؛ DELE/SIELE منفصلان','حسب الدورة','لا','https://ave.cervantes.es','official'),
('rai-italiano-free','Italiano – Rai Scuola','rai-scuola-italiano','فيديوهات ومواد تعليمية مجانية لتطوير الإيطالية والفهم السمعي والمفردات والثقافة.','لغات','مبتدئ إلى متوسط','Italian','ذاتي',1,0,'لا توجد شهادة رسمية مجانية عامة معلنة','مجاني','لا','https://www.raiscuola.rai.it/italiano','official'),
('pushkin-russian-free','تعلم الروسية مع معهد بوشكين','pushkin-russian','مواد ومسارات رقمية من معهد بوشكين لتعلم الروسية كلغة أجنبية.','لغات','مبتدئ إلى متقدم','Russian','متغير',1,1,'شهادة عند توفرها في البرنامج المحدد','مجاني حسب البرنامج','نعم','https://pushkininstitute.ru/learn','official'),
('sejong-korean-online','Online King Sejong Institute – Korean','sejong-korean','دروس كورية منظمة من معهد الملك سيجونغ مع تدريب القراءة والاستماع والمحادثة.','لغات','مبتدئ إلى متقدم','Korean','منظم/ذاتي',1,1,'شهادة حسب البرنامج','مجاني حسب المسار','لا','https://www.iksi.or.kr/lms/main/main.do','official'),
('chineseplus-beginner','ChinesePlus – Chinese','chineseplus','موارد للمبتدئين في الصينية تشمل النطق والمفردات والاستماع والمواقف اليومية.','لغات','مبتدئ','Chinese','ذاتي',1,0,'لا توجد شهادة عامة مجانية مؤكدة','مجاني حسب المورد','لا','https://www.chineseplus.net','official'),
('navoica-polish-free','Polish for Everyone – NAVOICA','navoica-polish-plus','دورة MOOC مجانية لتعلم البولندية كلغة أجنبية، وبعض الدورات تمنح شهادة إتمام عند استيفاء شروط النجاح.','لغات','مبتدئ/متوسط','Polish','متغير',1,1,'شهادة إتمام عند استيفاء شروط الدورة','مجاني','لا','https://navoica.pl','official'),
('openlearn-how-language-plus','How to learn a language – OpenLearn','openlearn-languages','دورة مجانية من The Open University في استراتيجيات تعلم اللغات، ويمكن الحصول على Statement of Participation مجاني عند الإتمام.','لغات','مبتدئ','English','حوالي 24 ساعة',1,1,'Statement of Participation + Digital Badge عند توفره','مجاني','لا','https://www.open.edu/openlearn/languages/how-learn-language','official'),
('openlearn-why-languages-plus','Why study languages? – OpenLearn','openlearn-languages','دورة مناسبة للطلاب الثانويين تقريبًا 11–16 سنة عن أهمية اللغات والثقافات ومسارات دراسة اللغات، مع إثبات مشاركة مجاني عند الإتمام.','لغات','مبتدئ','English','حوالي 5 ساعات',1,1,'Statement of Participation / Digital Badge عند توفره','مجاني','لا','https://www.open.edu/openlearn/languages/why-study-languages/content-section-0','official'),
]

def merge(conn):
    today=date.today().isoformat()
    for p in PLATFORMS:
        slug,name,desc,official,courses,certs,country,cats,free,certs_av,guide=p
        conn.execute('''INSERT OR IGNORE INTO platforms
        (slug,name,logo,description,official_url,courses_url,certificates_url,scholarships_url,volunteering_url,country,categories,free_courses_available,certificates_available,financial_aid_available,free_access_guide,source_type,official_source,verified,last_checked)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(slug,name,None,desc,official,courses,certs,None,None,country,json.dumps(cats,ensure_ascii=False),free,certs_av,0,guide,'official',official,1,today))
    ids={r[0]:r[1] for r in conn.execute('SELECT slug,id FROM platforms')}
    for c in COURSES:
        slug,title,pslug,desc,cat,level,lang,duration,free,cert,ctype,price,aid,url,source=c
        pid=ids.get(pslug)
        if not pid: continue
        conn.execute('''INSERT OR IGNORE INTO courses
        (slug,title,platform_id,description,category,level,language,duration,free,certificate_available,certificate_type,price,financial_aid,official_url,source,source_type,verified,status,last_checked)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(slug,title,pid,desc,cat,level,lang,duration,free,cert,ctype,price,1 if aid=='نعم' else 0,url,source,'official',1,'open',today))
    conn.commit()
