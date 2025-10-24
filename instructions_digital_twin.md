# Digital Twin Oracle - Integration Instructions

## Overview
The Digital Twin Oracle displays a glowing humanoid figure that changes color based on your current FlowOS zone (Rest & Recharge, Health, Creative, etc.).

## Integration Steps

### 1️⃣ CSS Integration
Add this CSS block to your main `<style>` section (before the closing `</style>` tag):

```css
/* --- Digital Twin (Oracle) --- */
.oracle-wrap{
  display:flex; align-items:center; justify-content:center;
  height: 260px; position:relative; overflow:hidden;
  background: radial-gradient(600px 320px at 50% -30%, rgba(125,242,201,.08), transparent 60%),
              radial-gradient(520px 280px at 120% 120%, rgba(110,168,254,.10), transparent 60%);
  border:1px solid var(--border); border-radius: var(--radius);
}

.oracle{
  position:relative; width: 160px; aspect-ratio: 3/5;
  filter: drop-shadow(0 12px 28px rgba(0,0,0,.45));
}

.oracle .aura{
  position:absolute; inset:-18%;
  border-radius: 30% 30% 36% 36% / 28% 28% 52% 52%;
  background: radial-gradient(60% 60% at 50% 35%, rgba(255,255,255,.35), transparent 60%),
              radial-gradient(80% 80% at 50% 50%, rgba(110,168,254,.25), transparent 65%);
  filter: blur(18px) saturate(1.1);
  animation: auraPulse 3.6s ease-in-out infinite;
  opacity:.9;
}

.oracle .body{
  position:absolute; inset:0; display:block;
  background:
    radial-gradient(45% 45% at 50% 20%, rgba(255,255,255,.85), rgba(255,255,255,.15) 60%),
    linear-gradient(180deg, rgba(110,168,254,.9), rgba(125,242,201,.7) 60%, rgba(110,168,254,.85));
  -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 160"><path d="M50 12c12 0 22 10 22 22s-10 22-22 22-22-10-22-22S38 12 50 12zM32 73c12-6 24-6 36 0 14 7 22 20 22 36v38H10v-38c0-16 8-29 22-36z"/></svg>') center/contain no-repeat;
  mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 160"><path d="M50 12c12 0 22 10 22 22s-10 22-22 22-22-10-22-22S38 12 50 12zM32 73c12-6 24-6 36 0 14 7 22 20 22 36v38H10v-38c0-16 8-29 22-36z"/></svg>') center/contain no-repeat;
  border-radius: 18px;
  animation: subtleFloat 6s ease-in-out infinite;
}

/* Zone colors */
.oracle[data-zone="Rest & Recharge"] .aura{background:radial-gradient(60% 60% at 50% 35%,rgba(255,255,255,.35),transparent 60%),radial-gradient(80% 80% at 50% 50%,rgba(125,242,201,.30),transparent 65%)}
.oracle[data-zone="Health"] .aura{background:radial-gradient(60% 60% at 50% 35%,rgba(255,255,255,.35),transparent 60%),radial-gradient(80% 80% at 50% 50%,rgba(118,255,155,.30),transparent 65%);animation-duration:2.2s}
.oracle[data-zone="Creative / Project Work"] .aura{background:radial-gradient(60% 60% at 50% 35%,rgba(255,255,255,.35),transparent 60%),radial-gradient(80% 80% at 50% 50%,rgba(110,168,254,.30),transparent 65%)}
.oracle[data-zone="Review & Planning"] .aura{background:radial-gradient(60% 60% at 50% 35%,rgba(255,255,255,.35),transparent 60%),radial-gradient(80% 80% at 50% 50%,rgba(179,138,255,.28),transparent 65%)}
.oracle[data-zone="Errands & Logistics"] .aura{background:radial-gradient(60% 60% at 50% 35%,rgba(255,255,255,.35),transparent 60%),radial-gradient(80% 80% at 50% 50%,rgba(255,176,90,.30),transparent 65%)}
.oracle[data-zone="Social & Relationships"] .aura{background:radial-gradient(60% 60% at 50% 35%,rgba(255,255,255,.35),transparent 60%),radial-gradient(80% 80% at 50% 50%,rgba(255,122,122,.28),transparent 65%)}
.oracle[data-zone="Flex"] .aura{background:radial-gradient(60% 60% at 50% 35%,rgba(255,255,255,.35),transparent 60%),radial-gradient(80% 80% at 50% 50%,rgba(154,163,178,.28),transparent 65%)}

/* Animations */
@keyframes auraPulse{0%,100%{transform:scale(.96);opacity:.85}50%{transform:scale(1.03);opacity:1}}
@keyframes subtleFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}

.oracle-legend{margin-top:10px;font-size:12px;color:var(--muted);text-align:center}
```

### 2️⃣ HTML Integration
Add this panel after your existing panels (e.g., after "Crash Plan"):

```html
<!-- Digital Twin (Oracle) Panel -->
<section class="panel" id="oraclePanel" style="margin-top:18px;">
  <div class="hd">
    <h2>Digital Twin</h2>
    <div class="hint"><span id="oracleZoneHint">—</span></div>
  </div>
  <div class="bd">
    <div class="oracle-wrap">
      <div id="oracle" class="oracle" data-zone="Rest & Recharge" aria-label="Digital twin state">
        <div class="aura"></div>
        <div class="body"></div>
      </div>
    </div>
    <div class="oracle-legend">
      Mirrors your current Area (Rest &amp; Recharge, Health, Creative, etc.).
    </div>
  </div>
</section>
```

### 3️⃣ JavaScript Integration
Add these functions before your closing `</script>` tag:

```javascript
/* ---------- Digital Twin wiring ---------- */
function normalizeZone(area){
  const m = {
    "Rest & Recharge": "Rest & Recharge",
    "Health": "Health",
    "Creative / Project Work": "Creative / Project Work",
    "Review & Planning": "Review & Planning",
    "Errands & Logistics": "Errands & Logistics",
    "Social & Relationships": "Social & Relationships",
    "Flex": "Flex",
    "Prep & Maintenance": "Review & Planning"
  };
  return m[area] || "Flex";
}

function setOracleZone(zone){
  const el = document.getElementById('oracle');
  const hint = document.getElementById('oracleZoneHint');
  if (!el) return;
  el.setAttribute('data-zone', zone);
  if (hint) hint.textContent = zone;
}

function updateOracleFromAgenda(){
  const day = window.__CURRENT_DAY;
  if (!day) return;
  const now = new Date();
  const current = findCurrentArea(day.events, now);
  if (current){
    setOracleZone(normalizeZone(current.area));
    return;
  }
  const next = findNextArea(day.events, now);
  setOracleZone(next ? "Flex" : "Flex");
}

document.addEventListener('DOMContentLoaded', ()=>{
  if (document.getElementById('oracle')){
    updateOracleFromAgenda();
  }
});

const __oldUpdateLiveArea = updateLiveArea;
updateLiveArea = function(){
  try{ __oldUpdateLiveArea(); }catch(_){}
  updateOracleFromAgenda();
};
```

## Features

✅ **Real-time Zone Detection**: Automatically detects and displays current FlowOS zone  
✅ **Dynamic Color Auras**: Each zone has its unique color scheme  
✅ **Smooth Animations**: Subtle floating and pulsing effects  
✅ **Accessibility**: Proper ARIA labels and semantic HTML  
✅ **Responsive Design**: Adapts to different screen sizes  

## Zone Color Mapping

- **Rest & Recharge**: Mint green aura
- **Health**: Bright green aura (faster pulse)
- **Creative / Project Work**: Blue aura
- **Review & Planning**: Purple aura
- **Errands & Logistics**: Orange aura
- **Social & Relationships**: Red/pink aura
- **Flex**: Gray aura

## Testing

The sandbox file `sandbox_digital_twin_oracle.html` is ready for testing and demonstrates the full functionality.