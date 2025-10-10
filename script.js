// jengquin.io v1 demo script

const $ = sel => document.querySelector(sel);
const $$ = sel => Array.from(document.querySelectorAll(sel));

function fmtTime(d){
  return new Intl.DateTimeFormat(undefined, { hour:'numeric', minute:'2-digit' }).format(d);
}
function fmtDate(d){
  return new Intl.DateTimeFormat(undefined, { month:'short', day:'numeric' }).format(d);
}
function addDays(d, n){ const c = new Date(d); c.setDate(c.getDate()+n); return c; }
function escapeHtml(s){ return String(s).replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])) }

let DEMO = true;

// ------------ Mock data
function mockTop3(){
  return [
    { title: "Ship GenCoin v1 page", due: "", completed: false, tag:"#Admin" },
    { title: "Record 'Album Stream' bumper", due: "", completed: false, tag:"#Creative" },
    { title: "7-Day Crash pass → prune tasks", due: "", completed: true, tag:"#Review" },
  ];
}
function mockCrash(){
  const now = new Date();
  return [
    { title: "Bank statements → sort & tag", due: addDays(now,1), completed:false, tag:"#Finance"},
    { title: "Mom Log: weekly summary", due: addDays(now,2), completed:false, tag:"#Caregiving"},
    { title: "Raspberry Pi: stream loop", due: addDays(now,3), completed:false, tag:"#Infra"},
    { title: "Nova → Quick Add Shortcut", due: addDays(now,4), completed:true, tag:"#Flow"},
  ];
}
function mockCalendar(){
  const now = new Date();
  return [...Array(7)].map((_,i)=>{
    const d = addDays(now, i);
    const events = [];
    if(i===0) events.push({ t:"Standup (self)", at: new Date(d.setHours(10,0)), color:"blue"});
    if(i===1) events.push({ t:"Studio hour", at: new Date(addDays(now,1).setHours(14,0)), color:"green"});
    if(i===2) events.push({ t:"Groceries + meal prep", at: new Date(addDays(now,2).setHours(18,0)), color:"blue"});
    return { date: addDays(new Date(),i), events };
  });
}

// ------------ Live fetch helpers (wire these to your API later)
async function apiGet(path){
  // Replace with: return fetch(path).then(r=>r.json())
  if(path==="/top3") return mockTop3();
  if(path==="/crash7") return mockCrash();
  if(path==="/calendar") return mockCalendar();
  return [];
}
async function apiPost(path, payload){
  // Replace with real fetch POST when backend is ready
  return { ok:true };
}

// ------------ Renderers
function renderTop3(items){
  const wrap = $('#top3List'); wrap.innerHTML = "";
  items.forEach((it, idx)=>{
    const row = document.createElement('div');
    row.className = 'item' + (it.completed ? ' done' : '');
    row.innerHTML = `
      <label class="chx" aria-label="toggle done"><span class="dot"></span></label>
      <div>
        <div class="title">${escapeHtml(it.title)}</div>
        <div class="meta">${it.tag ? escapeHtml(it.tag) : ''}</div>
      </div>
      <div class="row">
        <span class="tag">Top 3</span>
        <button class="btn ghost kebab" data-action="remove" title="Remove">⋯</button>
      </div>`;
    row.querySelector('.chx').addEventListener('click', async ()=>{
      row.classList.toggle('done');
      // later: await apiPost('/reminder/toggle', { list:'Top 3', index: idx })
    });
    row.querySelector('[data-action="remove"]').addEventListener('click', async ()=>{
      row.style.opacity = .5;
      // later: await apiPost('/reminder/delete', { list:'Top 3', index: idx })
      setTimeout(()=> row.remove(), 180);
    });
    wrap.appendChild(row);
  });
}

function renderCrash(items){
  const wrap = $('#crashList'); wrap.innerHTML = "";
  items.forEach((it, idx)=>{
    const due = it.due ? fmtDate(new Date(it.due)) : "—";
    const row = document.createElement('div');
    row.className = 'item' + (it.completed ? ' done' : '');
    row.innerHTML = `
      <label class="chx" aria-label="toggle done"><span class="dot"></span></label>
      <div>
        <div class="title">${escapeHtml(it.title)}</div>
        <div class="meta">Due: ${due} ${it.tag ? '· ' + escapeHtml(it.tag) : ''}</div>
      </div>
      <span class="tag">Crash 7</span>`;
    row.querySelector('.chx').addEventListener('click', async ()=>{
      row.classList.toggle('done');
      // later: await apiPost('/reminder/toggle', { list:'Crash Plan', index: idx })
    });
    wrap.appendChild(row);
  });
}

function renderCal(days){
  const grid = $('#calGrid'); grid.innerHTML="";
  days.forEach(day=>{
    const div = document.createElement('div');
    div.className = 'day';
    div.innerHTML = `<div class="d">${fmtDate(new Date(day.date))}</div>`;
    if(day.events && day.events.length){
      day.events.forEach(ev=>{
        const pill = document.createElement('div');
        pill.className = 'pill ' + (ev.color || 'blue');
        pill.title = ev.t;
        pill.textContent = `${fmtTime(new Date(ev.at))} • ${ev.t}`;
        div.appendChild(pill);
      });
    } else {
      const none = document.createElement('div');
      none.className = 'faded'; none.textContent = '—';
      div.appendChild(none);
    }
    grid.appendChild(div);
  });
}

// ------------ Quick add
function wireEvents(){
  $('#top3Form').addEventListener('submit', async (e)=>{
    e.preventDefault();
    const fd = new FormData(e.target);
    const title = String(fd.get('title')||'').trim();
    if(!title) return;
    if(DEMO){
      const items = mockTop3();
      items.unshift({title, due:"", completed:false, tag:"#QuickAdd"});
      renderTop3(items);
    }else{
      await apiPost('/reminder', { list:"Top 3", title });
      await loadTop3();
    }
    e.target.reset();
  });

  // Simulated native app actions
  $('#revealTop3').addEventListener('click', ()=> alert('Would call /open { list:"Top 3" } → opens Reminders'));
  $('#revealCrash').addEventListener('click', ()=> alert('Would call /open { list:"Crash Plan" } → opens Reminders'));
  $('#openCalendar').addEventListener('click', ()=> alert('Would call /open-calendar → opens Calendar'));
  $('#openReminders').addEventListener('click', ()=> alert('Opening Reminders (simulated)…'));
  $('#quickAddTop').addEventListener('click', ()=> $('.in[name="title"]').focus());

  // Demo toggle
  $('#toggleDemo').addEventListener('click', () => {
    DEMO = !DEMO;
    $('#toggleDemo').textContent = `Demo: ${DEMO ? 'Demo: On' : 'Demo: Off'}`;
    loadAll();
  });
}

// ------------ Loaders
async function loadTop3(){
  const items = DEMO ? mockTop3() : await apiGet('/top3');
  renderTop3(items);
}
async function loadCrash(){
  const items = DEMO ? mockCrash() : await apiGet('/crash7');
  renderCrash(items);
}
async function loadCalendar(){
  const days = DEMO ? mockCalendar() : await apiGet('/calendar');
  renderCal(days);
}
async function loadAll(){
  const now = new Date();
  $('#nowHint').textContent = fmtDate(now) + " · " + fmtTime(now);
  $('#rangeHint').textContent = `${fmtDate(now)} → ${fmtDate(addDays(now,6))}`;
  $('#tzHint').textContent = `Local time: ${Intl.DateTimeFormat().resolvedOptions().timeZone}`;
  $('#year').textContent = new Date().getFullYear();
  await Promise.all([loadTop3(), loadCrash(), loadCalendar()]);
}

// Init
document.addEventListener('DOMContentLoaded', ()=>{
  wireEvents();
  loadAll();
});
