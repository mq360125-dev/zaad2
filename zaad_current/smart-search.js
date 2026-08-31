/* ZAAD Smart Search — Google-like instant suggestions and language/country intent search. */
(() => {
  const LANGS = [
    {name:'الإنجليزية', aliases:['انجليزي','انجليزية','english','uk','بريطانيا'], country:'بريطانيا', flag:'🇬🇧'},
    {name:'الفرنسية', aliases:['فرنسي','فرنسا','français','french','france'], country:'فرنسا', flag:'🇫🇷'},
    {name:'الألمانية', aliases:['الماني','ألماني','german','germany','deutsch'], country:'ألمانيا', flag:'🇩🇪'},
    {name:'اليابانية', aliases:['ياباني','اليابان','japanese','japan','日本語'], country:'اليابان', flag:'🇯🇵'},
    {name:'الإسبانية', aliases:['اسباني','إسباني','اسبانيا','إسبانيا','spanish','spain','español'], country:'إسبانيا', flag:'🇪🇸'},
    {name:'الإيطالية', aliases:['ايطالي','إيطالي','ايطاليا','إيطاليا','italian','italy','italiano'], country:'إيطاليا', flag:'🇮🇹'},
    {name:'الروسية', aliases:['روسي','روسيا','russian','russia','русский','россия'], country:'روسيا', flag:'🇷🇺'},
    {name:'الكورية', aliases:['كوري','كوريا','korean','korea','한국어'], country:'كوريا الجنوبية', flag:'🇰🇷'},
    {name:'الصينية', aliases:['صيني','الصين','chinese','china','中文'], country:'الصين', flag:'🇨🇳'},
    {name:'الهولندية', aliases:['هولندي','هولندا','dutch','netherlands','nederlands'], country:'هولندا', flag:'🇳🇱'},
    {name:'البولندية', aliases:['بولندي','بولندا','polish','poland','polski'], country:'بولندا', flag:'🇵🇱'},
    {name:'التركية', aliases:['تركي','تركيا','turkish','turkey','türkçe'], country:'تركيا', flag:'🇹🇷'},
    {name:'البرتغالية', aliases:['برتغالي','البرتغال','portuguese','portugal'], country:'البرتغال', flag:'🇵🇹'},
    {name:'العربية', aliases:['عربي','العربية','arabic'], country:'الدول العربية', flag:'🌍'}
  ];
  const COMPANIES = [
    ['Google',['جوجل','غوغل','google','gemini']],
    ['IBM',['ibm','آي بي إم','اي بي ام','skillsbuild']],
    ['OpenLearn',['openlearn','open learn','المفتوحة']],
    ['Harvard CS50',['harvard','هارفارد','cs50']],
    ['Microsoft Learn',['microsoft','مايكروسوفت','azure']],
    ['AWS Skill Builder',['aws','amazon','أمازون','skill builder']],
    ['Cisco Networking Academy',['cisco','سيسكو','netacad']],
    ['NASA',['nasa','ناسا']],
    ['UNICEF',['unicef','يونيسف']],
    ['Zooniverse',['zooniverse']],
    ['Goethe-Institut',['goethe','غوته']],
    ['Instituto Cervantes',['cervantes','سرفانتس']],
    ['King Sejong Institute',['sejong','سيجونغ']],
    ['Pushkin Institute',['pushkin','بوشكين']]
  ];
  const TYPE_WORDS = {
    scholarship:['منحة','منح','scholarship','scholarships','grant'],
    course:['كورس','كورسات','دورة','دورات','course','courses'],
    internship:['تدريب','تدريبات','internship','internships'],
    volunteer:['تطوع','تطوعات','volunteer','volunteering'],
    platform:['منصة','منصات','platform','platforms'],
    certificate:['شهادة','شهادات','certificate','certification','credential','اعتماد']
  };
  const esc = v => String(v ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
  const norm = v => String(v ?? '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[إأآ]/g,'ا').replace(/ة/g,'ه').replace(/ى/g,'ي').replace(/ـ/g,'').trim();
  const input = document.getElementById('search-input');
  const box = document.getElementById('search-suggestions');
  if (!input || !box) return;
  const shell = input.closest('.search-shell');
  const allData = {opportunities:[], courses:[], platforms:[]};
  let timer;
  async function fetchPages(endpoint){
    const out=[]; for(let page=1; page<=12; page++){
      try{const r=await fetch(`${endpoint}${endpoint.includes('?')?'&':'?'}page=${page}&page_size=100`,{headers:{Accept:'application/json'}}); if(!r.ok) break; const j=await r.json(); const b=Array.isArray(j.results)?j.results:[]; out.push(...b); if(!b.length || b.length<100 || out.length>=Number(j.total||0)) break;}catch(e){break;}
    } return out;
  }
  async function load(){
    const [o,c,p]=await Promise.all([fetchPages('/api/opportunities?type=all'),fetchPages('/api/courses'),fetchPages('/api/platforms')]);
    allData.opportunities=o; allData.courses=c; allData.platforms=p;
  }
  function typeLabel(x){return x.type==='scholarship'?'منحة':x.type==='internship'?'تدريب':x.type==='volunteer'?'تطوع':x.type==='program'?'برنامج':x.type==='competition'?'مسابقة':x.type==='platform'?'منصة':'كورس'}
  function itemText(x){return norm([x.title,x.name,x.description,x.organization,x.platform_name,x.country,x.language,x.category,x.certificate_type,...(Array.isArray(x.categories)?x.categories:[])].filter(Boolean).join(' '));}
  function languageFor(q){const n=norm(q); return LANGS.find(l => n===norm(l.name) || l.aliases.some(a=>n===norm(a)) || n.includes(norm(l.name)) || l.aliases.some(a=>n.includes(norm(a))));}
  function companyFor(q){const n=norm(q); return COMPANIES.find(([name,a])=>n===norm(name)||a.some(v=>n.includes(norm(v))));}
  function hasWord(q,list){const n=norm(q); return list.some(v=>n===norm(v)||n.includes(norm(v)));}
  function queryTerms(q){
    const n=norm(q); const lang=languageFor(q); const comp=companyFor(q); const terms=[n];
    if(lang) terms.push(norm(lang.name),...lang.aliases.map(norm),norm(lang.country));
    if(comp) terms.push(norm(comp[0]),...comp[1].map(norm));
    return [...new Set(terms.filter(Boolean))];
  }
  function matches(x,q){const terms=queryTerms(q); const text=itemText(x); return terms.some(t=>text.includes(t));}
  function typeMatches(x,type){if(type==='platform') return false; if(type==='certificate') return !!(x.certificate_available||x.certificate); return x.type===type || (type==='course' && !x.type && x.title);}
  function queryButton(label,q,icon='⌕'){return `<button class="zs-query" data-zs-query="${esc(q)}"><span>${icon}</span><strong>${esc(label)}</strong><em>›</em></button>`}
  function resultButton(x){const t=x.type||'course'; const id=x.id; return `<button class="zs-result" data-zs-id="${esc(id)}" data-zs-type="${esc(t)}"><span class="zs-result-icon">${t==='scholarship'?'🎓':t==='course'?'📘':t==='internship'?'💼':t==='volunteer'?'🤝':t==='platform'?'🏛️':'✨'}</span><span><strong>${esc(x.title||x.name)}</strong><small>${esc(typeLabel(x))}${x.organization?` • ${esc(x.organization)}`:''}${x.country?` • ${esc(x.country)}`:''}</small></span><em>›</em></button>`}
  function render(){
    const q=input.value.trim(); if(!q){box.classList.add('hidden');input.setAttribute('aria-expanded','false');return;}
    const lang=languageFor(q), comp=companyFor(q); let html='';
    html += `<div class="zs-head">بحث سريع <span>${esc(q)}</span></div>`;
    if(lang){
      html += `<div class="zs-intent"><div class="zs-intent-title">${lang.flag} ${esc(lang.name)} <small>• ${esc(lang.country)}</small></div><div class="zs-query-grid">`;
      html += queryButton(`منح ${lang.country}`,`${lang.country} منحة`,'🎓');
      html += queryButton(`كورسات ${lang.name}`,`${lang.name} كورس`,'📚');
      html += queryButton(`تدريبات ${lang.name}`,`${lang.name} تدريب`,'💼');
      html += queryButton(`منصات ${lang.name}`,`${lang.name} منصة`,'🌐');
      html += queryButton(`شهادات ${lang.name}`,`${lang.name} شهادة`,'🏅');
      html += `</div></div>`;
    } else if(comp){
      html += `<div class="zs-intent"><div class="zs-intent-title">🏢 ${esc(comp[0])}</div><div class="zs-query-grid">${queryButton('الكورسات',`${comp[0]} كورس`,'📚')}${queryButton('الشهادات',`${comp[0]} شهادة`,'🏅')}${queryButton('الفرص',`${comp[0]} فرصة`,'✨')}</div></div>`;
    } else {
      const types=[['منح','منحة','🎓'],['كورسات','كورس','📚'],['تدريب','تدريب','💼'],['تطوع','تطوع','🤝'],['منصات','منصة','🌐']];
      html += `<div class="zs-intent"><div class="zs-intent-title">🔎 ابحث في كل أقسام زاد</div><div class="zs-query-grid">${types.map(x=>queryButton(x[0],`${q} ${x[1]}`,x[2])).join('')}</div></div>`;
    }
    const pool=[...allData.opportunities,...allData.courses,...allData.platforms].filter(x=>matches(x,q));
    const seen=new Set(); const results=pool.filter(x=>{const k=`${x.type||'course'}:${x.id}`;if(seen.has(k))return false;seen.add(k);return true;}).slice(0,8);
    if(results.length){html += `<div class="zs-head zs-results-head">نتائج قريبة</div><div class="zs-results">${results.map(resultButton).join('')}</div>`;}
    else html += `<div class="zs-empty">لا توجد نتيجة مطابقة تمامًا — جرّب اسم دولة، لغة، شركة أو نوع فرصة.</div>`;
    box.innerHTML=html; box.classList.remove('hidden'); input.setAttribute('aria-expanded','true');
    box.querySelectorAll('[data-zs-query]').forEach(b=>b.onclick=()=>{input.value=b.dataset.zsQuery; input.dispatchEvent(new Event('input',{bubbles:true})); setTimeout(render,0);});
    box.querySelectorAll('[data-zs-id]').forEach(b=>b.onclick=()=>{window.location.href=`/detail.html?type=${encodeURIComponent(b.dataset.zsType)}&id=${encodeURIComponent(b.dataset.zsId)}`;});
  }
  input.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(render,80);});
  input.addEventListener('focus',()=>{if(input.value.trim())render();});
  document.addEventListener('click',e=>{if(shell&&!shell.contains(e.target)){box.classList.add('hidden');input.setAttribute('aria-expanded','false');}});
  load().then(render);
})();
