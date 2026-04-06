import streamlit as st
import time

st.set_page_config(
    page_title="StockSense · Fundamental Analyzer",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

:root {
    --bg:      #04090f;
    --surface: rgba(10,22,38,0.82);
    --border:  #152840;
    --accent:  #00d4ff;
    --green:   #00ff88;
    --yellow:  #ffd60a;
    --red:     #ff4560;
    --text:    #c8dff0;
    --muted:   #3d6080;
    --glow:    0 0 24px rgba(0,212,255,0.22);
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}
.stApp { background-color: var(--bg) !important; }

#bg-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    pointer-events: none;
}

.ticker-bar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 32px;
    background: rgba(4,9,15,0.95);
    border-bottom: 1px solid var(--border);
    overflow: hidden;
    z-index: 999;
    display: flex;
    align-items: center;
}
.ticker-track {
    display: flex;
    white-space: nowrap;
    animation: scroll-left 42s linear infinite;
}
@keyframes scroll-left {
    from { transform: translateX(0); }
    to   { transform: translateX(-50%); }
}
.ticker-item {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.06em;
    padding: 0 20px;
    border-right: 1px solid #0e2035;
    line-height: 32px;
    display: inline-flex;
    align-items: center;
    gap: 7px;
}
.ticker-item .sym { color: #fff; font-weight: 700; }
.ticker-item .val { color: var(--muted); }
.ticker-item .up  { color: var(--green); }
.ticker-item .dn  { color: var(--red); }

.block-container {
    position: relative;
    z-index: 1;
    padding-top: 3.5rem !important;
    max-width: 780px !important;
}

.header-wrap { text-align: center; padding: 2rem 0 1.2rem; }
.header-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid rgba(0,212,255,0.45);
    padding: 3px 14px;
    border-radius: 2px;
    margin-bottom: 0.9rem;
    box-shadow: var(--glow);
}
.header-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.03em;
    margin: 0;
    line-height: 1.1;
}
.header-title span { color: var(--accent); }
.header-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    margin-top: 0.55rem;
    letter-spacing: 0.1em;
}

.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.26em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.8rem 0 0.7rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after { content:''; flex:1; height:1px; background:var(--border); }

.stNumberInput > div > div > input {
    background: rgba(5,14,26,0.9) !important;
    border: 1px solid var(--border) !important;
    color: var(--accent) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 1.05rem !important;
    border-radius: 6px !important;
    padding: 0.5rem 0.8rem !important;
}
.stNumberInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: var(--glow) !important;
}
.stNumberInput label {
    color: var(--text) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
}

.stButton > button {
    width: 100% !important;
    background: transparent !important;
    border: 1.5px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 2rem !important;
    border-radius: 6px !important;
    margin-top: 0.8rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: rgba(0,212,255,0.07) !important;
    box-shadow: var(--glow) !important;
    transform: translateY(-1px) !important;
}

.result-box {
    border-radius: 10px;
    padding: 1.8rem 2rem;
    margin: 1.4rem 0 1rem;
    text-align: center;
    animation: fadeSlide 0.45s cubic-bezier(.22,.68,0,1.2);
    backdrop-filter: blur(6px);
}
@keyframes fadeSlide {
    from { opacity:0; transform:translateY(14px) scale(.97); }
    to   { opacity:1; transform:translateY(0) scale(1); }
}
.result-box.green  { border:1.5px solid var(--green);  background:rgba(0,255,136,0.06); }
.result-box.yellow { border:1.5px solid var(--yellow); background:rgba(255,214,10,0.06); }
.result-box.red    { border:1.5px solid var(--red);    background:rgba(255,69,96,0.06); }
.result-box.grey   { border:1.5px solid var(--muted);  background:rgba(61,96,128,0.06); }
.result-label { font-family:'Space Mono',monospace; font-size:0.6rem; letter-spacing:0.24em; text-transform:uppercase; margin-bottom:0.4rem; color:var(--muted); }
.result-verdict { font-size:2.2rem; font-weight:800; letter-spacing:-0.01em; line-height:1.2; }
.result-box.green  .result-verdict { color:var(--green); }
.result-box.yellow .result-verdict { color:var(--yellow); }
.result-box.red    .result-verdict { color:var(--red); }
.result-box.grey   .result-verdict { color:var(--muted); }
.result-note { font-size:0.75rem; color:#7a9ab8; margin-top:0.5rem; font-family:'Space Mono',monospace; }

.metrics-row { display:grid; grid-template-columns:repeat(4,1fr); gap:0.65rem; margin:1.1rem 0; }
.m-tile { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:0.9rem 0.5rem; text-align:center; backdrop-filter:blur(8px); }
.m-tile-label { font-family:'Space Mono',monospace; font-size:0.52rem; letter-spacing:0.14em; text-transform:uppercase; color:var(--muted); margin-bottom:0.35rem; }
.m-tile-value { font-family:'Space Mono',monospace; font-size:1.05rem; font-weight:700; color:var(--accent); }

.score-wrap { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:1.2rem 1.4rem; margin:0.7rem 0; backdrop-filter:blur(8px); }
.score-title { font-family:'Space Mono',monospace; font-size:0.58rem; letter-spacing:0.2em; text-transform:uppercase; color:var(--muted); margin-bottom:0.9rem; }
.bar-row { margin-bottom:0.75rem; }
.bar-label { display:flex; justify-content:space-between; font-family:'Space Mono',monospace; font-size:0.62rem; color:var(--text); margin-bottom:0.28rem; }
.bar-track { height:3px; background:var(--border); border-radius:2px; overflow:hidden; }
.bar-fill  { height:100%; border-radius:2px; transition:width 0.8s cubic-bezier(.22,.68,0,1); }

.footer { font-family:'Space Mono',monospace; font-size:0.58rem; color:var(--muted); text-align:center; padding:2rem 0 1rem; letter-spacing:0.07em; }

#MainMenu, footer, header { visibility:hidden; }
.stDeployButton { display:none; }
div[data-testid="stDecoration"] { display:none; }
hr { border-color:var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  ANIMATED CANVAS BACKGROUND + SCROLLING TICKER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="ticker-bar">
  <div class="ticker-track" id="ticker-track"></div>
</div>

<canvas id="bg-canvas"></canvas>

<script>
// ── Ticker ───────────────────────────────────────────────────────────────────
const TICKERS = [
  {sym:"RELIANCE",  price:"2947.30", chg:"+1.24%", up:true},
  {sym:"TCS",       price:"3812.55", chg:"+0.87%", up:true},
  {sym:"INFY",      price:"1423.10", chg:"-0.41%", up:false},
  {sym:"HDFCBANK",  price:"1688.75", chg:"+0.63%", up:true},
  {sym:"ICICIBANK", price:"1122.40", chg:"+1.05%", up:true},
  {sym:"WIPRO",     price:"458.90",  chg:"-0.28%", up:false},
  {sym:"BAJFINANCE",price:"6934.20", chg:"+2.11%", up:true},
  {sym:"SBIN",      price:"782.55",  chg:"-0.55%", up:false},
  {sym:"MARUTI",    price:"12340.00",chg:"+0.74%", up:true},
  {sym:"TATAMOTORS",price:"942.30",  chg:"+1.88%", up:true},
  {sym:"NIFTY50",   price:"23541.85",chg:"+0.96%", up:true},
  {sym:"SENSEX",    price:"77489.20",chg:"+0.82%", up:true},
  {sym:"ADANIENT",  price:"2455.60", chg:"-1.32%", up:false},
  {sym:"LTIM",      price:"5612.00", chg:"+0.50%", up:true},
  {sym:"SUNPHARMA", price:"1680.40", chg:"+0.33%", up:true},
  {sym:"HINDUNILVR",price:"2234.80", chg:"-0.18%", up:false},
  {sym:"ONGC",      price:"267.45",  chg:"+0.92%", up:true},
  {sym:"COALINDIA", price:"412.60",  chg:"-0.44%", up:false},
  {sym:"POWERGRID", price:"322.15",  chg:"+0.67%", up:true},
  {sym:"NTPC",      price:"358.90",  chg:"+1.14%", up:true},
];

const track = document.getElementById('ticker-track');
const makeItems = () => TICKERS.map(t =>
  `<span class="ticker-item">
     <span class="sym">${t.sym}</span>
     <span class="val">${t.price}</span>
     <span class="${t.up?'up':'dn'}">${t.chg}</span>
   </span>`).join('');
track.innerHTML = makeItems() + makeItems();

// ── Canvas ───────────────────────────────────────────────────────────────────
const canvas = document.getElementById('bg-canvas');
const ctx    = canvas.getContext('2d');

function resize() {
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', () => { resize(); render(); });

// ── Grid ─────────────────────────────────────────────────────────────────────
function drawGrid() {
  const sz = 52;
  ctx.strokeStyle = 'rgba(21,40,64,0.5)';
  ctx.lineWidth   = 0.5;
  for (let x=0; x<canvas.width; x+=sz) {
    ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,canvas.height); ctx.stroke();
  }
  for (let y=32; y<canvas.height; y+=sz) {
    ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke();
  }
}

// ── Large ghost stock names ───────────────────────────────────────────────────
const FLOATERS = [
  {text:'RELIANCE',    x:0.06, y:0.22, op:0.042, sz:40},
  {text:'NIFTY 50',   x:0.52, y:0.16, op:0.055, sz:44},
  {text:'TCS',         x:0.80, y:0.40, op:0.048, sz:50},
  {text:'INFY',        x:0.10, y:0.50, op:0.038, sz:38},
  {text:'SENSEX',      x:0.38, y:0.70, op:0.052, sz:46},
  {text:'BAJFINANCE',  x:0.55, y:0.88, op:0.036, sz:36},
  {text:'HDFCBANK',    x:0.18, y:0.87, op:0.038, sz:36},
  {text:'WIPRO',       x:0.68, y:0.62, op:0.038, sz:38},
  {text:'SBIN',        x:0.32, y:0.42, op:0.034, sz:34},
  {text:'TATAMOTORS',  x:0.48, y:0.52, op:0.032, sz:32},
  {text:'MARUTI',      x:0.72, y:0.92, op:0.034, sz:34},
  {text:'NTPC',        x:0.05, y:0.93, op:0.034, sz:34},
];

function drawFloaters() {
  FLOATERS.forEach(f => {
    ctx.save();
    ctx.globalAlpha = f.op;
    ctx.fillStyle   = '#00d4ff';
    ctx.font        = `bold ${f.sz}px Syne, sans-serif`;
    ctx.fillText(f.text, f.x * canvas.width, f.y * canvas.height);
    ctx.restore();
  });
}

// ── Mini sparkline stock cards ────────────────────────────────────────────────
const CARDS = [
  {name:'RELIANCE', chg:'+1.24%', up:true,  pts:[120,118,125,130,128,135,142,139,145,150,148,155], col:'#00ff88', x:0.02,  y:0.10},
  {name:'TCS',      chg:'+0.87%', up:true,  pts:[200,195,202,208,205,212,210,218,215,222,220,228], col:'#00d4ff', x:0.72,  y:0.07},
  {name:'INFY',     chg:'-0.41%', up:false, pts:[180,182,178,175,172,170,168,165,167,163,160,158], col:'#ff4560', x:0.755, y:0.52},
  {name:'HDFCBANK', chg:'+0.63%', up:true,  pts:[100,102,105,104,108,112,110,115,118,116,121,124], col:'#00ff88', x:0.02,  y:0.60},
  {name:'BAJFIN',   chg:'+2.11%', up:true,  pts:[300,298,310,320,315,325,335,330,342,348,352,362], col:'#ffd60a', x:0.715, y:0.28},
  {name:'SBIN',     chg:'-0.55%', up:false, pts:[90,88,85,87,84,82,80,83,78,76,74,72],             col:'#ff4560', x:0.02,  y:0.34},
  {name:'MARUTI',   chg:'+0.74%', up:true,  pts:[150,155,158,154,162,165,162,170,172,170,176,180], col:'#00d4ff', x:0.72,  y:0.76},
  {name:'NTPC',     chg:'+1.14%', up:true,  pts:[60,62,61,65,67,66,70,72,71,76,74,79],             col:'#00ff88', x:0.02,  y:0.80},
];

function drawCard(card) {
  const W=148, H=76, pad=10;
  const cx = Math.floor(card.x * canvas.width);
  const cy = Math.floor(card.y * canvas.height);

  // card bg
  ctx.fillStyle   = 'rgba(6,15,28,0.78)';
  ctx.strokeStyle = 'rgba(21,40,64,0.95)';
  ctx.lineWidth   = 1;
  ctx.beginPath(); ctx.roundRect(cx,cy,W,H,6); ctx.fill(); ctx.stroke();

  // accent top bar
  ctx.fillStyle = card.col + '33';
  ctx.fillRect(cx, cy, W, 3);
  ctx.fillStyle = card.col;
  ctx.fillRect(cx, cy, W*0.55, 3);

  // name
  ctx.fillStyle = 'rgba(200,223,240,0.65)';
  ctx.font = 'bold 8.5px Space Mono, monospace';
  ctx.fillText(card.name, cx+pad, cy+18);

  // change
  ctx.fillStyle = card.up ? '#00ff88' : '#ff4560';
  ctx.font = '7.5px Space Mono, monospace';
  ctx.fillText(card.chg, cx+W-pad-30, cy+18);

  // sparkline
  const pts=card.pts, min=Math.min(...pts), max=Math.max(...pts), range=max-min||1;
  const sw=W-pad*2, sh=H-34, sx=cx+pad, sy=cy+26;

  const grad = ctx.createLinearGradient(0, sy, 0, sy+sh);
  const hex2 = card.col + '30';
  grad.addColorStop(0, hex2); grad.addColorStop(1,'transparent');
  ctx.beginPath();
  pts.forEach((v,i)=>{
    const px=sx+(i/(pts.length-1))*sw;
    const py=sy+sh-((v-min)/range)*sh;
    i===0 ? ctx.moveTo(px,py) : ctx.lineTo(px,py);
  });
  ctx.lineTo(sx+sw, sy+sh); ctx.lineTo(sx, sy+sh); ctx.closePath();
  ctx.fillStyle=grad; ctx.fill();

  ctx.beginPath();
  pts.forEach((v,i)=>{
    const px=sx+(i/(pts.length-1))*sw;
    const py=sy+sh-((v-min)/range)*sh;
    i===0 ? ctx.moveTo(px,py) : ctx.lineTo(px,py);
  });
  ctx.strokeStyle=card.col; ctx.lineWidth=1.8; ctx.stroke();

  // dot at end
  const lx=sx+sw, ly=sy+sh-((pts[pts.length-1]-min)/range)*sh;
  ctx.beginPath(); ctx.arc(lx,ly,3,0,Math.PI*2);
  ctx.fillStyle=card.col; ctx.fill();
}

// ── Main candlestick chart ────────────────────────────────────────────────────
const CANDLES = [
  {o:400,h:420,l:390,c:415},{o:415,h:430,l:408,c:425},{o:425,h:440,l:418,c:420},
  {o:420,h:435,l:412,c:432},{o:432,h:450,l:425,c:446},{o:446,h:462,l:438,c:457},
  {o:457,h:468,l:445,c:450},{o:450,h:465,l:442,c:462},{o:462,h:478,l:456,c:474},
  {o:474,h:488,l:465,c:482},{o:482,h:494,l:470,c:478},{o:478,h:496,l:472,c:490},
  {o:490,h:508,l:484,c:503},{o:503,h:514,l:490,c:498},{o:498,h:518,l:492,c:514},
  {o:514,h:528,l:507,c:522},{o:522,h:534,l:510,c:518},{o:518,h:532,l:512,c:528},
  {o:528,h:545,l:520,c:538},{o:538,h:552,l:530,c:546},{o:546,h:562,l:538,c:556},
  {o:556,h:568,l:545,c:550},{o:550,h:564,l:542,c:560},{o:560,h:576,l:552,c:570},
  {o:570,h:585,l:562,c:578},
];

function drawCandles() {
  const sx=0.12*canvas.width, ex=0.88*canvas.width;
  const sy=0.18*canvas.height, ey=0.84*canvas.height;
  const all=CANDLES.flatMap(c=>[c.h,c.l]);
  const minV=Math.min(...all), maxV=Math.max(...all), range=maxV-minV;
  const total=CANDLES.length;
  const cw=(ex-sx)/total, bw=cw*0.52;

  const toY = v => sy + (1-(v-minV)/range)*(ey-sy);

  // Reference dashed lines + price labels
  [0.25,0.50,0.75].forEach(frac => {
    const y = sy + frac*(ey-sy);
    const price = (minV+(1-frac)*range).toFixed(0);
    ctx.strokeStyle='rgba(21,40,64,0.7)'; ctx.lineWidth=0.8;
    ctx.setLineDash([5,9]);
    ctx.beginPath(); ctx.moveTo(sx,y); ctx.lineTo(ex,y); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle='rgba(61,96,128,0.55)'; ctx.font='8px Space Mono,monospace';
    ctx.fillText(price, sx-2, y+3);
  });

  // Volume bars
  CANDLES.forEach((c,i) => {
    const cx2 = sx + i*cw + cw/2;
    const volH = (18 + i*0.6 + Math.sin(i*0.7)*8) * 0.4;
    ctx.fillStyle = c.c>=c.o ? 'rgba(0,255,136,0.10)' : 'rgba(255,69,96,0.09)';
    ctx.fillRect(cx2-bw/2, ey+5, bw, volH);
  });

  // Candle bodies + wicks
  CANDLES.forEach((c,i) => {
    const cx2=sx+i*cw+cw/2;
    const bull=c.c>=c.o;
    ctx.strokeStyle = bull ? 'rgba(0,255,136,0.28)' : 'rgba(255,69,96,0.26)';
    ctx.fillStyle   = bull ? 'rgba(0,255,136,0.20)' : 'rgba(255,69,96,0.18)';
    ctx.lineWidth   = 1;
    ctx.beginPath(); ctx.moveTo(cx2,toY(c.h)); ctx.lineTo(cx2,toY(c.l)); ctx.stroke();
    const top=toY(Math.max(c.o,c.c)), bot=toY(Math.min(c.o,c.c));
    const h=Math.max(bot-top,1.5);
    ctx.fillRect(cx2-bw/2,top,bw,h);
    ctx.strokeRect(cx2-bw/2,top,bw,h);
  });

  // MA line
  const ma=CANDLES.map(c=>(c.h+c.l+c.c)/3);
  ctx.beginPath();
  ma.forEach((v,i)=>{
    const px=sx+i*cw+cw/2, py=toY(v);
    i===0?ctx.moveTo(px,py):ctx.lineTo(px,py);
  });
  const maGrad=ctx.createLinearGradient(sx,0,ex,0);
  maGrad.addColorStop(0,'rgba(0,212,255,0)');
  maGrad.addColorStop(0.25,'rgba(0,212,255,0.55)');
  maGrad.addColorStop(1,'rgba(0,255,136,0.38)');
  ctx.strokeStyle=maGrad; ctx.lineWidth=1.6; ctx.stroke();

  // Chart label
  ctx.fillStyle='rgba(0,212,255,0.22)';
  ctx.font='bold 9px Space Mono,monospace';
  ctx.fillText('NIFTY50  1D', sx, sy-8);
}

// ── Scattered data labels ─────────────────────────────────────────────────────
const LABELS = [
  {t:'P/E: 18.4',       x:0.06,  y:0.47},
  {t:'ROE: 22.3%',      x:0.60,  y:0.93},
  {t:'EPS: +16.7%',     x:0.30,  y:0.96},
  {t:'D/E: 0.42',       x:0.80,  y:0.93},
  {t:'EBITDA: 32%',     x:0.15,  y:0.97},
  {t:'Mkt Cap: 18L Cr', x:0.44,  y:0.10},
  {t:'52W H: 3124',     x:0.60,  y:0.04},
  {t:'52W L: 2234',     x:0.76,  y:0.04},
  {t:'Beta: 1.12',      x:0.08,  y:0.06},
  {t:'Vol: 4.2M',       x:0.24,  y:0.06},
  {t:'RSI: 61.4',       x:0.36,  y:0.04},
  {t:'MACD: +12.3',     x:0.06,  y:0.97},
];
function drawLabels() {
  ctx.fillStyle='rgba(0,212,255,0.14)';
  ctx.font='8.5px Space Mono,monospace';
  LABELS.forEach(d=>ctx.fillText(d.t, d.x*canvas.width, d.y*canvas.height));
}

// ── Corner brackets ───────────────────────────────────────────────────────────
function drawCorners() {
  const sz=28;
  [[8,40,1,1],[canvas.width-8,40,-1,1],[8,canvas.height-8,1,-1],[canvas.width-8,canvas.height-8,-1,-1]]
    .forEach(([x,y,dx,dy])=>{
      ctx.strokeStyle='rgba(0,212,255,0.28)'; ctx.lineWidth=1.5;
      ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x+dx*sz,y); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x,y+dy*sz); ctx.stroke();
    });
}

// ── Render ────────────────────────────────────────────────────────────────────
function render() {
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.fillStyle='#04090f'; ctx.fillRect(0,0,canvas.width,canvas.height);
  drawGrid();
  drawFloaters();
  drawCandles();
  CARDS.forEach(drawCard);
  drawLabels();
  drawCorners();
}

render();
</script>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  APP UI
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="header-wrap">
    <div class="header-badge">Fundamental Analysis Engine v2.0</div>
    <h1 class="header-title">Stock<span>Sense</span></h1>
    <p class="header-sub">Enter metrics &nbsp;·&nbsp; Get an instant signal &nbsp;·&nbsp; Indian equities</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Financial Inputs</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    eps = st.number_input("📈  EPS Growth (%)",        min_value=0.0, max_value=200.0, step=0.1,  help="Earnings Per Share growth YoY")
    roe = st.number_input("💰  Return on Equity (%)",  min_value=0.0, max_value=100.0, step=0.1,  help="Net income / Shareholders equity")
with col2:
    de  = st.number_input("⚖️  Debt / Equity Ratio",   min_value=0.0, max_value=20.0,  step=0.01, help="Total debt / Total equity")
    pe  = st.number_input("💸  P/E Ratio",              min_value=0.0, max_value=500.0, step=0.1,  help="Market price / Earnings per share")

st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
analyze = st.button("▶  RUN ANALYSIS", use_container_width=True)

if analyze:
    with st.spinner(""):
        time.sleep(0.55)

    if eps >= 15 and roe >= 18 and de <= 1:
        if pe <= 20:
            verdict, emoji, css_cls = "STRONG BUY",      "🟢", "green"
            logic = "Excellent fundamentals at a fair valuation. High conviction entry."
        else:
            verdict, emoji, css_cls = "BUY · EXPENSIVE", "🟡", "yellow"
            logic = "Great business quality, but valuation is stretched."
    elif eps >= 10 and roe >= 15 and de <= 1.5:
        verdict, emoji, css_cls = "BUY",               "🟡", "yellow"
        logic = "Solid metrics. Acceptable fundamentals for accumulation."
    elif de > 2:
        verdict, emoji, css_cls = "AVOID · HIGH DEBT", "🔴", "red"
        logic = "High leverage is a significant risk factor. Capital at risk."
    else:
        verdict, emoji, css_cls = "HOLD",              "⚪", "grey"
        logic = "Mixed signals. Monitor for improving catalysts."

    st.markdown(f"""
    <div class="result-box {css_cls}">
        <div class="result-label">Signal</div>
        <div class="result-verdict">{emoji} {verdict}</div>
        <div class="result-note">{logic}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metrics-row">
        <div class="m-tile"><div class="m-tile-label">EPS Growth</div><div class="m-tile-value">{eps:.1f}%</div></div>
        <div class="m-tile"><div class="m-tile-label">ROE</div><div class="m-tile-value">{roe:.1f}%</div></div>
        <div class="m-tile"><div class="m-tile-label">Debt/Equity</div><div class="m-tile-value">{de:.2f}</div></div>
        <div class="m-tile"><div class="m-tile-label">P/E Ratio</div><div class="m-tile-value">{pe:.1f}</div></div>
    </div>
    """, unsafe_allow_html=True)

    def pct(val, lo, hi): return min(100, max(0, int((val-lo)/(hi-lo)*100)))
    def bar_color(p): return "var(--green)" if p>=65 else ("var(--yellow)" if p>=35 else "var(--red)")

    ep=pct(eps,0,30); rp=pct(roe,0,30); dp=pct(3-de,0,3); pp=pct(50-pe,0,50)

    st.markdown(f"""
    <div class="score-wrap">
        <div class="score-title">Metric Scorecard</div>
        <div class="bar-row">
            <div class="bar-label"><span>EPS Growth</span><span>{eps:.1f}%</span></div>
            <div class="bar-track"><div class="bar-fill" style="width:{ep}%;background:{bar_color(ep)};"></div></div>
        </div>
        <div class="bar-row">
            <div class="bar-label"><span>Return on Equity</span><span>{roe:.1f}%</span></div>
            <div class="bar-track"><div class="bar-fill" style="width:{rp}%;background:{bar_color(rp)};"></div></div>
        </div>
        <div class="bar-row">
            <div class="bar-label"><span>Debt/Equity (lower = better)</span><span>{de:.2f}</span></div>
            <div class="bar-track"><div class="bar-fill" style="width:{dp}%;background:{bar_color(dp)};"></div></div>
        </div>
        <div class="bar-row">
            <div class="bar-label"><span>P/E Ratio (lower = cheaper)</span><span>{pe:.1f}</span></div>
            <div class="bar-track"><div class="bar-fill" style="width:{pp}%;background:{bar_color(pp)};"></div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    StockSense &nbsp;·&nbsp; Built with Streamlit &nbsp;·&nbsp; Educational use only &nbsp;·&nbsp; Not financial advice
</div>
""", unsafe_allow_html=True)
