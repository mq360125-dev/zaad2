import sqlite3, json
from datetime import date
DB='opportunities.db'
TODAY=date.today().isoformat()

PLATFORMS=[
('salesforce-trailhead','Salesforce Trailhead','منصة Salesforce الرسمية المجانية للتعلم العملي عبر Badges وTrails وSuperbadges في CRM والبيانات والذكاء الاصطناعي وAgentforce.','https://trailhead.salesforce.com/','https://trailhead.salesforce.com/','https://trailhead.salesforce.com/','Global',['CRM','AI','Data','Salesforce'],1,1,'الـBadges والـSuperbadges متاحة عبر Trailhead مجانًا. شهادات Salesforce المهنية الرسمية منفصلة ولها امتحانات وشروط خاصة.'),
('hubspot-academy','HubSpot Academy','أكاديمية HubSpot الرسمية: تدريب مجاني عبر الإنترنت وشهادات في التسويق الرقمي والمبيعات وخدمة العملاء وCRM والمحتوى.','https://academy.hubspot.com/','https://academy.hubspot.com/courses','https://academy.hubspot.com/courses','Global',['Marketing','Sales','CRM','Business'],1,1,'التدريب والشهادات المحددة في HubSpot Academy مجانية. تحقّق من صفحة كل شهادة قبل التسجيل.'),
('sap-learning','SAP Learning','منصة SAP الرسمية للتعلم في SAP S/4HANA والسحابة والبيانات والذكاء الاصطناعي، مع Learning Journeys وشارات رقمية.','https://learning.sap.com/','https://learning.sap.com/','https://learning.sap.com/certifications','Global',['SAP','ERP','Cloud','Data','AI'],1,1,'تتوفر Learning Journeys مجانية، ويمكن الحصول على بعض الشارات/Records of Achievement عبر متطلبات التعلم. امتحان SAP Certification منفصل ومدفوع عادةً.'),
('fortinet-training','Fortinet Training Institute','معهد Fortinet الرسمي للتدريب في الأمن السيبراني، ويقدم دورات ذاتية مجانية وشهادات NSE بمسارات منفصلة.','https://training.fortinet.com/','https://training.fortinet.com/','https://www.fortinet.com/training-certification','Global',['Cybersecurity','Networking'],1,1,'الدورات الذاتية في Training Institute مفتوحة مجانًا؛ المختبرات وبعض خدمات التدريب والامتحانات قد تكون منفصلة.'),
('redhat-academy','Red Hat Academy','برنامج Red Hat الرسمي للمؤسسات التعليمية، يوفر للطلاب المؤهلين دورات Linux وAnsible وOpenShift مع مختبرات ومسارات تؤهل لشهادات Red Hat.','https://www.redhat.com/en/services/training/red-hat-academy','https://www.redhat.com/en/services/training/red-hat-academy','https://www.redhat.com/en/services/training-and-certification','Global',['Linux','Open Source','Cloud','DevOps'],1,1,'الوصول المجاني مرتبط بالمؤسسات الأكاديمية الشريكة المؤهلة. امتحانات الشهادة لها شروط منفصلة.'),
('adobe-experience-league','Adobe Experience League','منصة Adobe الرسمية للتعلم في Adobe Experience Cloud وAnalytics وAEM وCommerce وMarketo وGenStudio، مع دورات تحضيرية للشهادات.','https://experienceleague.adobe.com/','https://experienceleague.adobe.com/','https://certification.adobe.com/','Global',['Adobe','Analytics','Marketing','Commerce','AI'],1,1,'تتوفر مواد ودورات تعلم رسمية، بينما امتحانات Adobe Certification منفصلة وقد تكون مدفوعة.'),
('mongodb-university','MongoDB University','منصة MongoDB الرسمية للتعلم المجاني عبر وحدات ومسارات ومختبرات وشارات مهارية، مع مسارات تؤهل للشهادات المهنية.','https://learn.mongodb.com/','https://learn.mongodb.com/catalog','https://learn.mongodb.com/catalog','Global',['MongoDB','Database','Python','Node.js','AI'],1,1,'التعلم المجاني متاح، وبعض المهارات تمنح Skill Badges مجانية. بعض امتحانات MongoDB Certification مدفوعة، مع عروض مجانية لبعض الطلاب المؤهلين.'),
]
COURSES=[]
def C(slug,title,platform,desc,cat,level,lang,dur,free,cert,ctype,url,price='مجاني'):
    COURSES.append((slug,title,platform,desc,cat,level,lang,dur,free,cert,ctype,url,price))

# Salesforce
C('sf-trailhead-admin-beginner','Salesforce Admin Beginner','salesforce-trailhead','مسار Trailhead تأسيسي لتعلم أساسيات Salesforce وإدارة المستخدمين والبيانات والتخصيص، مع وحدات عملية وشارات يمكن عرضها على ملف Trailblazer.','CRM وSalesforce','مبتدئ','الإنجليزية','متغير',1,1,'Trailhead Badges','https://trailhead.salesforce.com/users/strailhead/trailmixes/admin-beginner')
C('sf-agentblazer-beginner','Agentblazer — أساسيات الوكلاء الذكيين','salesforce-trailhead','مسار Salesforce لتعلم مفاهيم Agentforce والوكلاء الذكيين وتطبيقاتهم في الأعمال.','الذكاء الاصطناعي','مبتدئ','الإنجليزية','متغير',1,1,'Trailhead Badges','https://trailhead.salesforce.com/')
C('sf-data-cloud-basics','Salesforce Data Cloud Basics','salesforce-trailhead','تعلم أساسيات توحيد البيانات والملفات التعريفية والبيانات المستخدمة لبناء تجارب مخصصة داخل منظومة Salesforce.','البيانات وCRM','مبتدئ','الإنجليزية','متغير',1,1,'Trailhead Badges','https://trailhead.salesforce.com/')
C('sf-crm-basics','Salesforce CRM Basics','salesforce-trailhead','مدخل عملي لفهم CRM وإدارة العملاء والفرص والعمليات باستخدام Salesforce.','CRM','مبتدئ','الإنجليزية','متغير',1,1,'Trailhead Badges','https://trailhead.salesforce.com/')
C('sf-superbadges','Salesforce Superbadges','salesforce-trailhead','تحديات عملية متقدمة داخل Trailhead لتطبيق المهارات بدل الاكتفاء بالمشاهدة، وتمنح Superbadges عند إكمال التحدي.','تطبيق عملي','متوسط','الإنجليزية','متغير',1,1,'Trailhead Superbadge','https://trailhead.salesforce.com/superbadges')
# HubSpot
C('hubspot-digital-marketing','Digital Marketing Certification — HubSpot Academy','hubspot-academy','شهادة HubSpot مجانية في أساسيات التسويق الرقمي والاستراتيجية والقنوات الرقمية وقياس الأداء.','التسويق الرقمي','مبتدئ','الإنجليزية ولغات متعددة','نحو 3 ساعات',1,1,'HubSpot Academy Certification','https://academy.hubspot.com/courses/digital-marketing')
C('hubspot-social-media','Social Media Marketing Certification — HubSpot Academy','hubspot-academy','شهادة مجانية لتعلم استراتيجية وسائل التواصل الاجتماعي والمحتوى والقياس والنمو.','التسويق الرقمي','مبتدئ','الإنجليزية ولغات متعددة','نحو 5 ساعات',1,1,'HubSpot Academy Certification','https://academy.hubspot.com/courses/social-media')
C('hubspot-seo','SEO Certification — HubSpot Academy','hubspot-academy','دورة وشهادة مجانية في تحسين محركات البحث والبحث عن الكلمات المفتاحية وبناء المحتوى والروابط وقياس النتائج.','SEO','مبتدئ','الإنجليزية','متغير',1,1,'HubSpot Academy Certification','https://academy.hubspot.com/courses/seo-training')
C('hubspot-content-marketing','Content Marketing Certification — HubSpot Academy','hubspot-academy','شهادة مجانية في تخطيط المحتوى وإنشائه وتوزيعه وقياس أثره.','التسويق بالمحتوى','مبتدئ','الإنجليزية','متغير',1,1,'HubSpot Academy Certification','https://academy.hubspot.com/courses/content-marketing')
C('hubspot-inbound','Inbound Certification — HubSpot Academy','hubspot-academy','شهادة مجانية في منهجية Inbound وفهم رحلة العميل وبناء استراتيجيات جذب وتحويل واحتفاظ.','الأعمال والتسويق','مبتدئ','الإنجليزية','متغير',1,1,'HubSpot Academy Certification','https://academy.hubspot.com/courses/inbound')
# SAP
C('sap-discover-sap','Discovering SAP','sap-learning','مسار تعريفي من SAP لفهم منظومة SAP والعمليات المؤسسية والسحابة قبل التخصص.','SAP وERP','مبتدئ','الإنجليزية','متغير',1,1,'Learning Record / Badge حسب المسار','https://learning.sap.com/')
C('sap-s4hana-overview','SAP S/4HANA Overview','sap-learning','تعلم أساسيات SAP S/4HANA والعمليات التي تدعمها المنصة السحابية الحديثة.','SAP S/4HANA','مبتدئ','الإنجليزية','متغير',1,1,'Learning Record / Badge حسب المسار','https://learning.sap.com/')
C('sap-business-ai','SAP Business AI','sap-learning','مقدمة في الذكاء الاصطناعي للأعمال داخل منظومة SAP وحالات الاستخدام المؤسسية.','الذكاء الاصطناعي','مبتدئ','الإنجليزية','متغير',1,1,'Learning Record / Badge حسب المسار','https://learning.sap.com/')
C('sap-data-platform','SAP Data and Analytics Learning','sap-learning','مسارات SAP في البيانات والتحليلات لمساعدة المتعلم على فهم إدارة البيانات واتخاذ القرار.','البيانات والتحليلات','مبتدئ إلى متوسط','الإنجليزية','متغير',1,1,'Learning Record / Badge حسب المسار','https://learning.sap.com/')
C('sap-cloud-erp','SAP Cloud ERP Learning','sap-learning','تعلم مفاهيم ERP السحابي وعمليات الأعمال والانتقال إلى منظومة SAP السحابية.','Cloud ERP','مبتدئ','الإنجليزية','متغير',1,1,'Learning Record / Badge حسب المسار','https://learning.sap.com/')
# Fortinet
C('fortinet-nse1','NSE 1: Cybersecurity — Fortinet','fortinet-training','المستوى التأسيسي في برنامج Fortinet للأمن السيبراني، مناسب لمن يبدأ من الصفر. التدريب الذاتي النظري مجاني وفق معهد Fortinet.','الأمن السيبراني','مبتدئ','الإنجليزية ولغات حسب البرنامج','متغير',1,1,'Fortinet NSE Credential حسب المتطلبات الحالية','https://training.fortinet.com/')
C('fortinet-nse2','NSE 2: Cybersecurity','fortinet-training','مستوى يوسع المعرفة الأساسية في الأمن السيبراني ومفاهيم التهديدات والحماية ضمن مسار Fortinet.','الأمن السيبراني','مبتدئ','الإنجليزية','متغير',1,1,'Fortinet NSE Credential حسب المتطلبات الحالية','https://training.fortinet.com/')
C('fortinet-security-awareness','Fortinet Security Awareness Training','fortinet-training','محتوى توعوي رسمي في الأمن السيبراني، ومتاح مجانًا في نسخة التعليم للمؤسسات المؤهلة وفق المناطق والشروط الحالية.','التوعية الأمنية','مبتدئ','الإنجليزية','متغير',1,1,'إتمام البرنامج حسب الإصدار','https://www.fortinet.com/training/security-awareness-training/education-edition')
C('fortinet-network-security','Fortinet Network Security Fundamentals','fortinet-training','مدخل إلى مفاهيم أمن الشبكات ومنهجيات الحماية باستخدام مواد Fortinet التدريبية الرسمية.','أمن الشبكات','مبتدئ','الإنجليزية','متغير',1,0,'التدريب مجاني؛ الشهادة المهنية/الامتحان منفصل','https://training.fortinet.com/')
# Red Hat
C('redhat-rh024','Red Hat Enterprise Linux Technical Overview — RH024','redhat-academy','دروس فيديو مجانية عند الطلب تقدم مقدمة تقنية إلى Linux وRed Hat Enterprise Linux.','Linux','مبتدئ','الإنجليزية','متغير',1,0,'إتمام التعلم؛ شهادة RHCSA منفصلة','https://www.redhat.com/en/services/training-and-certification')
C('redhat-do007','Ansible Basics: Automation Technical Overview — DO007','redhat-academy','مقدمة مجانية إلى Ansible لإدارة البنية التحتية والأتمتة والتزويد والنشر.','DevOps وAnsible','مبتدئ','الإنجليزية','متغير',1,0,'إتمام التعلم؛ شهادة Ansible منفصلة','https://www.redhat.com/en/services/training-and-certification')
C('redhat-do080','Containers, Kubernetes and OpenShift Technical Overview — DO080','redhat-academy','مقدمة مجانية إلى الحاويات وKubernetes وRed Hat OpenShift وبناء بنية microservices.','Cloud وKubernetes','مبتدئ','الإنجليزية','متغير',1,0,'إتمام التعلم؛ شهادة Red Hat منفصلة','https://www.redhat.com/en/services/training-and-certification')
# Adobe
C('adobe-aem-training','Adobe Experience Manager Learning','adobe-experience-league','دروس Adobe الرسمية لتعلم أساسيات وإدارة Adobe Experience Manager وبناء تجارب رقمية.','Adobe وWeb','مبتدئ إلى متوسط','الإنجليزية','متغير',1,0,'دورة تحضيرية؛ Adobe Certification منفصلة','https://experienceleague.adobe.com/en/docs/certification')
C('adobe-analytics-training','Adobe Analytics Learning','adobe-experience-league','تدريب رسمي في Adobe Analytics لفهم البيانات والتقارير والتحليل الرقمي.','Analytics','مبتدئ إلى متوسط','الإنجليزية','متغير',1,0,'دورة تحضيرية؛ الشهادة المهنية منفصلة','https://experienceleague.adobe.com/')
C('adobe-commerce-training','Adobe Commerce Learning','adobe-experience-league','موارد ودروس رسمية لتعلم Adobe Commerce وإدارة التجارة الإلكترونية وتخصيص المتجر.','E-commerce','مبتدئ إلى متوسط','الإنجليزية','متغير',1,0,'دورة تحضيرية؛ الشهادة المهنية منفصلة','https://experienceleague.adobe.com/')
C('adobe-firefly-learning','Adobe Firefly Learning','adobe-experience-league','تعلم استخدام أدوات Adobe Firefly والذكاء الاصطناعي التوليدي في إنشاء المحتوى وسير العمل الإبداعي.','الذكاء الاصطناعي والإبداع','مبتدئ','الإنجليزية','متغير',1,0,'إتمام التعلم؛ لا نعده شهادة مهنية','https://experienceleague.adobe.com/')
# MongoDB
C('mongodb-overview-badge','MongoDB Overview Skill Badge','mongodb-university','مهارة مجانية تشرح نموذج المستند وبنية MongoDB ومفاهيم التوسع والتوافر العالي. إكمال الاختبار يمنح Credly Badge قابلة للمشاركة.','قواعد البيانات','مبتدئ','الإنجليزية ولغات متعددة','متغير',1,1,'MongoDB Skill Badge عبر Credly','https://learn.mongodb.com/courses/mongodb-overview')
C('mongodb-atlas-fundamentals','Getting Started with MongoDB Atlas','mongodb-university','مدخل مجاني إلى MongoDB Atlas والمنصة السحابية وقواعد البيانات الحديثة.','قواعد البيانات والسحابة','مبتدئ','الإنجليزية ولغات متعددة','متغير',1,1,'Course/Skill credential حسب المسار','https://learn.mongodb.com/catalog')
C('mongodb-python-developer','MongoDB Python Developer Learning Path','mongodb-university','مسار مجاني لتعلم استخدام MongoDB مع Python وبناء تطبيقات حديثة تعتمد على قاعدة بيانات المستندات.','Python وقواعد البيانات','مبتدئ إلى متوسط','الإنجليزية ولغات متعددة','متغير',1,1,'Course certificates / Skill Badges حسب المقرر','https://learn.mongodb.com/catalog')
C('mongodb-node-developer','MongoDB Node.js Developer Learning Path','mongodb-university','مسار تعلم لاستخدام MongoDB مع Node.js وبناء تطبيقات تعتمد على Atlas.','Node.js وقواعد البيانات','مبتدئ إلى متوسط','الإنجليزية ولغات متعددة','متغير',1,1,'Course certificates / Skill Badges حسب المقرر','https://learn.mongodb.com/catalog')
C('mongodb-genai-badges','MongoDB Generative AI Learning Badges','mongodb-university','مسارات مجانية في بناء تطبيقات الذكاء الاصطناعي التوليدي باستخدام MongoDB وAtlas Vector Search.','الذكاء الاصطناعي وقواعد البيانات','متوسط','الإنجليزية','متغير',1,1,'MongoDB GenAI Learning Badge','https://learn.mongodb.com/catalog')
# Meta
for slug,title,desc,cat in [
('meta-digital-marketing','Meta Digital Marketing Learning','تعلم أساسيات التسويق الرقمي عبر منظومة Meta ووسائل التواصل والمحتوى والإعلانات.','التسويق الرقمي'),
('meta-social-media','Meta Social Media Marketing Learning','موارد رسمية لتطوير استراتيجيات المحتوى وإدارة الحضور الرقمي على منصات Meta.','التسويق الرقمي'),
('meta-ads-basics','Meta Ads Fundamentals','مدخل إلى أساسيات إعلانات Meta وإدارة الحملات والجمهور وقياس الأداء.','الإعلانات الرقمية'),
('meta-ai-marketing','Meta AI and Marketing Learning','موارد تعلم في الذكاء الاصطناعي وتطبيقاته في التسويق والإبداع والإعلانات.','الذكاء الاصطناعي'),
]: C(slug,title,'meta-blueprint',desc,cat,'مبتدئ','الإنجليزية ولغات متعددة','متغير',1,0,'التعلم مجاني؛ امتحان Meta Certification منفصل','https://www.facebook.com/business/learn')
# AWS additional
for slug,title,url,desc,cat in [
('aws-data-engineering-foundations','Data Engineering on AWS — Foundations','https://aws.amazon.com/training/digital/','دورة AWS أساسية في هندسة البيانات ومفاهيم بناء حلول البيانات على AWS.','هندسة البيانات'),
('aws-connect-development','Amazon Connect Development Fundamentals','https://aws.amazon.com/training/digital/','تدريب مجاني من AWS على أساسيات تطوير حلول Amazon Connect.','Cloud وContact Center'),
('aws-ipv6-vpc','AWS IPv6 Fundamentals and VPC Connectivity','https://aws.amazon.com/training/digital/','تعلم أساسيات IPv6 والاتصال عبر VPC في AWS.','الشبكات السحابية'),
('aws-genai-executives','Generative AI for Executives — AWS','https://aws.amazon.com/training/digital/','مقدمة في الذكاء الاصطناعي التوليدي من منظور الأعمال والقيادة.','الذكاء الاصطناعي'),
('aws-security-fundamentals','AWS Security Fundamentals','https://aws.amazon.com/training/digital/','موارد تدريبية مجانية لفهم مبادئ الأمن في AWS وحماية الموارد السحابية.','الأمن السحابي'),
]: C(slug,title,'aws-skill-builder',desc,cat,'مبتدئ','العربية والإنجليزية ولغات متعددة','متغير',1,0,'التدريب مجاني؛ شهادة AWS المهنية/الامتحان منفصل','https://aws.amazon.com/training/digital/')
# Google extra
for slug,title,desc,cat in [
('google-ai-essentials','Google AI Essentials','تعلم أساسيات استخدام الذكاء الاصطناعي التوليدي بطريقة عملية ومسؤولة.','الذكاء الاصطناعي'),
('google-cloud-ai-foundations','Google Cloud AI Foundations','مقدمة في مفاهيم الذكاء الاصطناعي والتعلم الآلي على Google Cloud.','AI وCloud'),
('google-data-analytics-skills','Google Data Analytics Skills Resources','موارد Google لتطوير مهارات تحليل البيانات والعمل مع البيانات.','تحليل البيانات'),
('google-cybersecurity-skills','Google Cybersecurity Skills Resources','موارد تعلم Google في الأمن السيبراني ومهارات الدخول للمجال.','الأمن السيبراني'),
]: C(slug,title,'google-skillshop',desc,cat,'مبتدئ','الإنجليزية ولغات متعددة','متغير',1,0,'التدريب مجاني في الموارد المحددة؛ الشهادة المهنية قد تكون مدفوعة حسب البرنامج','https://www.skills.google/')
# Microsoft extra
for slug,title,url,desc,cat in [
('ms-generative-ai-agents','Introduction to generative AI and agents','https://learn.microsoft.com/en-us/training/','وحدة Microsoft Learn قصيرة في أساسيات الذكاء الاصطناعي التوليدي والوكلاء.','AI'),
('ms-explore-ai-basics','Explore AI basics','https://learn.microsoft.com/en-us/training/','وحدة تأسيسية مجانية لاستكشاف مفاهيم AI.','AI'),
('ms-powerbi-basics','Get started building with Power BI','https://learn.microsoft.com/en-us/training/','وحدة مجانية للبدء في بناء التقارير ولوحات البيانات باستخدام Power BI.','تحليل البيانات'),
('ms-copilot','Get started with Microsoft Copilot','https://learn.microsoft.com/en-us/training/','وحدة مجانية للتعرف على Microsoft Copilot واستخداماته.','AI'),
('ms-responsible-ai','Explore responsible AI','https://learn.microsoft.com/en-us/training/','وحدة مجانية لفهم مبادئ الذكاء الاصطناعي المسؤول.','AI وأخلاقياته'),
]: C(slug,title,'microsoft-learn',desc,cat,'مبتدئ','متعدد اللغات','أقل من ساعة تقريبًا',1,1,'Microsoft Learn achievement؛ Microsoft Certification/Applied Skills حسب المسار منفصل','https://learn.microsoft.com/en-us/training/')
# IBM extra
for slug,title,desc,cat in [
('ibm-ai-foundations','IBM SkillsBuild — AI Foundations','أساسيات الذكاء الاصطناعي من IBM SkillsBuild مع أنشطة ومفاهيم مناسبة للمبتدئين.','AI'),
('ibm-cybersecurity-foundations','IBM SkillsBuild — Cybersecurity Foundations','أساسيات الأمن السيبراني وحماية الأنظمة والبيانات.','Cybersecurity'),
('ibm-data-foundations','IBM SkillsBuild — Data Foundations','مقدمة في البيانات وتحليلها ومفاهيم العمل مع البيانات.','Data'),
('ibm-cloud-computing','IBM SkillsBuild — Cloud Computing Foundations','مقدمة في الحوسبة السحابية والخدمات والبنية الأساسية.','Cloud'),
('ibm-ai-ethics','IBM SkillsBuild — AI Ethics','مفاهيم أخلاقيات الذكاء الاصطناعي والمسؤولية والثقة.','AI Ethics'),
]: C(slug,title,'ibm-skillsbuild',desc,cat,'مبتدئ','العربية والإنجليزية ولغات متعددة','متغير',1,1,'IBM SkillsBuild Digital Credential حسب النشاط المؤهل','https://skillsbuild.org/learners')
# Cisco extra
for slug,title,desc,cat in [
('cisco-python-essentials','Cisco Networking Academy — Python Essentials','مدخل مجاني إلى Python ومفاهيم البرمجة الأساسية من Cisco Networking Academy.','Python'),
('cisco-networking-intro','Cisco Networking Academy — Networking Basics','أساسيات الشبكات وعناوين IP والبروتوكولات والمفاهيم العملية.','Networking'),
('cisco-cybersecurity-intro','Cisco Networking Academy — Introduction to Cybersecurity','مدخل مجاني إلى الأمن السيبراني والتهديدات والمهارات المهنية.','Cybersecurity'),
('cisco-digital-awareness','Cisco Digital Awareness','موارد تعلم رقمية وتوعية بالأمن والمهارات التقنية.','Digital Skills'),
]: C(slug,title,'cisco-networking-academy',desc,cat,'مبتدئ','الإنجليزية ولغات متعددة','متغير',1,0,'إتمام الدورة؛ الشهادات المهنية Cisco مثل CCNA منفصلة','https://www.cisco.com/site/us/en/learn/training-certifications/training/netacad/index.html')


def upsert_platform(conn,p):
    slug,name,desc,official,courses,certs,country,cats,free_count,cert_count,guide=p
    conn.execute('''INSERT INTO platforms (slug,name,description,official_url,courses_url,certificates_url,scholarships_url,volunteering_url,country,categories,free_courses_available,certificates_available,financial_aid_available,free_access_guide,official_source,verified,last_checked) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ON CONFLICT(slug) DO UPDATE SET name=excluded.name,description=excluded.description,official_url=excluded.official_url,courses_url=excluded.courses_url,certificates_url=excluded.certificates_url,country=excluded.country,categories=excluded.categories,free_courses_available=excluded.free_courses_available,certificates_available=excluded.certificates_available,free_access_guide=excluded.free_access_guide,official_source=excluded.official_source,verified=1,last_checked=excluded.last_checked''',
    (slug,name,desc,official,courses,certs,official,official,country,json.dumps(cats,ensure_ascii=False),free_count,cert_count,0,guide,official,1,TODAY))

def run():
    conn=sqlite3.connect(DB)
    for p in PLATFORMS: upsert_platform(conn,p)
    for c in COURSES:
        slug,title,platform,desc,cat,level,lang,dur,free,cert,ctype,url,price=c
        pid=conn.execute('select id from platforms where slug=?',(platform,)).fetchone()[0]
        conn.execute('''INSERT INTO courses (slug,title,platform_id,description,category,level,language,duration,free,certificate_available,certificate_type,price,financial_aid,official_url,source,source_type,verified,status,last_checked) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(slug) DO UPDATE SET title=excluded.title,platform_id=excluded.platform_id,description=excluded.description,category=excluded.category,level=excluded.level,language=excluded.language,duration=excluded.duration,free=excluded.free,certificate_available=excluded.certificate_available,certificate_type=excluded.certificate_type,price=excluded.price,official_url=excluded.official_url,source=excluded.source,source_type='official',verified=1,status='open',last_checked=excluded.last_checked''',
        (slug,title,pid,desc,cat,level,lang,dur,free,cert,ctype,price,0,url,url,'official',1,'open',TODAY))
    conn.commit()
    print('Added',len(PLATFORMS),'platforms and',len(COURSES),'company courses')
    print('Totals:',conn.execute('select count(*) from platforms').fetchone()[0], 'platforms;', conn.execute('select count(*) from courses').fetchone()[0], 'courses')
    conn.close()
if __name__=='__main__': run()
