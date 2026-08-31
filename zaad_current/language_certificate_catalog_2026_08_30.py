import sqlite3, json
from pathlib import Path
from datetime import date
DB=Path(__file__).resolve().parent/'opportunities.db'
TODAY='2026-08-30'
platforms=[
 ('tv5monde-french','TV5MONDE – Apprendre le français','منصة رسمية مجانية لتعلم الفرنسية بالفيديو والتمارين، مع آلاف الأنشطة من المبتدئ إلى المتقدم.','https://apprendre.tv5monde.com/','https://apprendre.tv5monde.com/','https://support-apprendre.tv5monde.com/fr/support/solutions/articles/61000281843-o%C3%B9-passer-le-tcf-comment-obtenir-une-attestation-','France / Global',['French','Languages']),
 ('goethe-institut-german','Goethe-Institut – Deutsch lernen','موارد مجانية رسمية لتعلم الألمانية، مع مسار منفصل لاختبارات Goethe-Zertifikat الرسمية.','https://www.goethe.de/en/spr/ueb.html','https://www.goethe.de/en/spr/ueb.html','https://www.goethe.de/en/spr/prf.html','Germany / Global',['German','Languages']),
 ('nhk-japanese','NHK WORLD-JAPAN – Easy Japanese','دروس يابانية مجانية للمبتدئين بالصوت والحوار والمفردات.','https://www3.nhk.or.jp/nhkworld/en/learnjapanese/','https://www3.nhk.or.jp/nhkworld/en/learnjapanese/','https://www.jlpt.jp/e/','Japan / Global',['Japanese','Languages']),
 ('cervantes-spanish','Instituto Cervantes – Spanish','موارد ودورات إسبانية من معهد ثربانتس، مع مسارات رسمية منفصلة مثل DELE/SIELE.','https://www.cervantes.es/','https://ave.cervantes.es/','https://examenes.cervantes.es/es/dele','Spain / Global',['Spanish','Languages']),
 ('rai-italian','Rai Scuola – Italiano','مواد إيطالية مجانية من Rai Scuola للفهم والمفردات والثقافة.','https://www.raiscuola.rai.it/italiano','https://www.raiscuola.rai.it/italiano','https://www.unistrapg.it/it/certificazioni-linguistiche/celi','Italy / Global',['Italian','Languages']),
 ('pushkin-russian','Pushkin Institute – Russian','موارد تعلم الروسية الرسمية من معهد بوشكين، مع مسارات اختبار/شهادة حسب البرنامج.','https://pushkininstitute.ru/learn','https://pushkininstitute.ru/learn','https://pushkininstitute.ru/learn','Russia / Global',['Russian','Languages']),
 ('king-sejong-korean','Online King Sejong Institute','تعلم الكورية عبر منصة معهد الملك سيجونغ؛ بعض المقررات تصدر شهادة إتمام.','https://www.iksi.or.kr/lms/main/main.do','https://www.iksi.or.kr/lms/main/main.do','https://www.iksi.or.kr/lms/main/userGuide.do','Korea / Global',['Korean','Languages']),
 ('chineseplus-chinese','ChinesePlus','موارد ودورات صينية للمبتدئين والمتوسطين، مع فصل واضح بين التعلم المجاني واختبارات اللغة الرسمية.','https://www.chineseplus.net/','https://www.chineseplus.net/en/learning','https://www.chinesetest.cn/','China / Global',['Chinese','Languages']),
 ('rug-dutch','University of Groningen – Dutch','موارد ودورة مقدمة مجانية لتعلم الهولندية، مع مسار شهادة NT2 رسمي منفصل.','https://www.rug.nl/language-centre/language-courses/dutch/','https://www.rug.nl/language-centre/language-courses/dutch/','https://www.staatsexamensnt2.nl/','Netherlands / Global',['Dutch','Languages']),
 ('navoica-polish','NAVOICA – Polish','منصة MOOC بولندية تضم دورات لغة بولندية، وبعضها يمنح شهادة إتمام وفق شروط الدورة.','https://navoica.pl','https://navoica.pl','https://certyfikatpolski.pl/en/','Poland / Global',['Polish','Languages']),
 ('yunus-emre-turkish','Yunus Emre – Turkish','موارد رسمية لتعلم التركية ومسار TYS الرسمي لإثبات الكفاءة.','https://turkce.yee.org.tr/','https://turkce.yee.org.tr/','https://www.tys.yee.org.tr/','Türkiye / Global',['Turkish','Languages']),
 ('british-council-english','British Council – LearnEnglish','موارد مجانية قوية للإنجليزية، مع اختبارات وشهادات رسمية منفصلة حسب الاختبار.','https://learnenglish.britishcouncil.org/','https://learnenglish.britishcouncil.org/','https://www.britishcouncil.org/exam','UK / Global',['English','Languages']),
]
cert_paths=[
 ('French','الفرنسية','TV5MONDE – تدريب مجاني + TCF رسمي','دورة مجانية للتعلم ثم مسار TCF الرسمي لإثبات المستوى. اختبار TCF نفسه ليس دورة مجانية ولا تفترض المنصة أن التدريب يمنح شهادة.','https://apprendre.tv5monde.com/','https://france-education-international.fr/test/tcf-tout-public','مجاني للتدريب؛ الاختبار الرسمي برسوم حسب المركز','شهادة لغة رسمية TCF'),
 ('German','الألمانية','Goethe-Institut – تعلم + Goethe-Zertifikat','تدريب مجاني من Goethe ثم اختبار Goethe-Zertifikat الرسمي. الشهادة الرسمية تأتي من الاختبار وليست مجانية لمجرد استخدام الموارد.','https://www.goethe.de/en/spr/ueb.html','https://www.goethe.de/en/spr/prf.html','التدريب مجاني؛ الامتحان برسوم حسب المركز','Goethe-Zertifikat A1–C2'),
 ('Japanese','اليابانية','NHK Easy Japanese + JLPT','دروس NHK مجانية للممارسة، ثم JLPT كاختبار رسمي لإثبات الكفاءة.','https://www3.nhk.or.jp/nhkworld/en/learnjapanese/','https://www.jlpt.jp/e/','الدروس مجانية؛ الاختبار برسوم','JLPT Certificate of Proficiency'),
 ('Spanish','الإسبانية','Instituto Cervantes + DELE','تعلم الإسبانية عبر موارد ثربانتس ثم التقدم لاختبار DELE الرسمي.','https://ave.cervantes.es/','https://examenes.cervantes.es/es/dele','الدورة/الموارد بحسب المسار؛ الاختبار الرسمي برسوم','DELE'),
 ('Italian','الإيطالية','Rai Scuola + CELI','استخدم موارد Rai Scuola المجانية ثم مسار CELI الرسمي لإثبات الكفاءة.','https://www.raiscuola.rai.it/italiano','https://www.unistrapg.it/it/certificazioni-linguistiche/celi','التعلم مجاني؛ الاختبار برسوم حسب المركز','CELI'),
 ('Russian','الروسية','Pushkin Institute – Russian + TORFL pathway','تعلم الروسية عبر معهد بوشكين، ثم تحقق من مسار الاختبار/الشهادة المتاح في البرنامج الحالي.','https://pushkininstitute.ru/learn','https://pushkininstitute.ru/learn','يتغير حسب البرنامج/المركز','شهادة/اختبار روسي حسب البرنامج'),
 ('Korean','الكورية','Online King Sejong + TOPIK','مقررات Online KSI مجانية، وبعضها يصدر شهادة إتمام؛ TOPIK هو مسار إثبات الكفاءة الرسمي.','https://www.iksi.or.kr/lms/main/main.do','https://www.topik.go.kr/','مقررات KSI المجانية حسب المقرر؛ TOPIK برسوم حسب الدولة','TOPIK / Certificate of Completion حسب المقرر'),
 ('Chinese','الصينية','ChinesePlus + HSK pathway','موارد ChinesePlus للتعلم، مع HSK كاختبار كفاءة رسمي منفصل.','https://www.chineseplus.net/en/learning','https://www.chinesetest.cn/','التعلم المجاني حسب المورد؛ الاختبار برسوم','HSK'),
 ('Dutch','الهولندية','University of Groningen Dutch + Staatsexamen Nt2','دورة مقدمة مجانية من Groningen، ثم Staatsexamen Nt2 لإثبات الكفاءة في هولندا.','https://www.rug.nl/language-centre/language-courses/dutch/','https://www.staatsexamensnt2.nl/','الدورة المجانية؛ الامتحان برسوم','Staatsexamen Nt2 B1/B2'),
 ('Polish','البولندية','NAVOICA + State Polish Certificate','دورات NAVOICA المجانية حسب الدورة، ثم الشهادة الحكومية البولندية عبر State Commission.','https://navoica.pl','https://certyfikatpolski.pl/en/','الدورة حسب شروطها؛ الامتحان برسوم','State Certificate of Proficiency in Polish'),
 ('Turkish','التركية','Yunus Emre + TYS','موارد Yunus Emre للتعلم، ثم TYS الرسمي الذي يمنح B2 أو C1 عند النجاح.','https://turkce.yee.org.tr/','https://www.tys.yee.org.tr/','التعلم حسب المورد؛ الاختبار برسوم','TYS B2/C1'),
 ('English','الإنجليزية','British Council LearnEnglish + official exam routes','تعلم مجاني عبر British Council، بينما الشهادات الرسمية مثل IELTS/اختبارات أخرى لها مسار امتحان منفصل.','https://learnenglish.britishcouncil.org/','https://www.britishcouncil.org/exam','الموارد مجانية؛ الاختبارات الرسمية برسوم','اختبار رسمي حسب الاختيار'),
 ('Portuguese','البرتغالية','Portuguese learning + CAPLE pathway','قسم مستقل لمسار البرتغالية مع التنبيه أن الشهادة الرسمية تأتي من اختبار معتمد وليس من كل مورد مجاني.','https://caple.letras.ulisboa.pt/','https://caple.letras.ulisboa.pt/','حسب الاختبار/المركز','CAPLE'),
]
con=sqlite3.connect(DB)
con.row_factory=sqlite3.Row
for slug,name,desc,official,courses,cert,country,cats in platforms:
    r=con.execute('select id from platforms where slug=?',(slug,)).fetchone()
    if r: pid=r['id']
    else:
        con.execute('''insert into platforms(slug,name,description,official_url,courses_url,certificates_url,country,categories,free_courses_available,certificates_available,financial_aid_available,free_access_guide,source_type,official_source,verified,last_checked) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(slug,name,desc,official,courses,cert,country,json.dumps(cats,ensure_ascii=False),1,1,0,'تحقق من كل مقرر أو اختبار؛ لا نعتبر الدورة المجانية شهادة لغة رسمية إلا إذا ذكر المصدر ذلك صراحة.','official',official,1,TODAY))
        pid=con.execute('select id from platforms where slug=?',(slug,)).fetchone()['id']
    for lang,lang_ar,title,desc2,free_url,cert_url,price,ctype in cert_paths:
        if lang_ar not in name and lang.lower() not in slug: continue
        cslug='zaad-'+slug+'-credential-path'
        if not con.execute('select 1 from courses where slug=?',(cslug,)).fetchone():
            con.execute('''insert into courses(slug,title,platform_id,description,category,level,language,duration,free,certificate_available,certificate_type,price,financial_aid,official_url,source,source_type,verified,status,last_checked) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(cslug,title,pid,desc2,'Language Certification','All levels',lang,'مرن',1 if 'التعلم مجاني' in price or 'الدروس مجانية' in price or 'الدورة المجانية' in price or 'موارد' in price else 0,1,ctype,price,0,free_url,cert_url,'official',1,'open',TODAY))
con.commit(); con.close()
print('language certification catalog updated')
