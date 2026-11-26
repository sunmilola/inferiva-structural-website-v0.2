#!/usr/bin/env python3
"""
Build the INFERIVA site.

Both reference sites are multi-page. Youverify runs roughly thirty pages across
Solution, Industry, Company, Resources and Legal; MetaMap is similar. A single
page cannot carry that, and more importantly a buyer who wants to read about
transaction monitoring specifically has nowhere to land.

This generates the shell once — nav, footer, styles — and writes each page's
content into it, so the chrome cannot drift between pages.

    python3 build.py
"""

from __future__ import annotations
import os, pathlib, shutil
from html import escape

OUT = pathlib.Path(__file__).parent
ENQUIRY_ENDPOINT = os.environ.get("INFERIVA_ENQUIRY_ENDPOINT", "").strip()

# --------------------------------------------------------------------------
# Information architecture.
#
# Deliberately smaller than Youverify's. Every page here has something real to
# say; a thin page is worse than an absent one, and a nav full of stubs is the
# first thing that reads as a startup pretending to be a company.
# --------------------------------------------------------------------------
NAV = [
    ("Platform", "platform/index.html", []),
    ("Solutions", "solutions.html", [
        ("Integrated platform", "platform/index.html"),
        ("Monitoring &amp; Investigations", "platform/aml.html"),
        ("Fraud Decisioning", "platform/fraud.html"),
        ("Due Diligence &amp; Customer Risk", "platform/customer-risk.html"),
        ("Investigations", "platform/investigations.html"),
        ("Regulatory reporting", "platform/reporting.html"),
        ("Agent &amp; Wallet Networks", "platform/agent-supervision.html"),
    ]),
    ("Institutions", "institutions.html", [
        ("Commercial banks", "sectors/commercial-banks.html"),
        ("Payments and mobile money", "sectors/agent-networks.html"),
        ("Microfinance institutions", "sectors/microfinance.html"),
        ("Digital lenders", "sectors/digital-lenders.html"),
    ]),
    ("Get started", "start/index.html", [
        ("Explore a diagnostic", "start/diagnostic.html"),
        ("Buying and deployment", "start/how-you-buy.html"),
    ]),
    ("Assurance", "assurance/index.html", [
        ("How an assessment runs", "assurance/how-it-works.html"),
        ("What you receive", "assurance/deliverables.html"),
    ]),
    ("Resources", "resources.html", []),
    ("Company", "company/contact.html", [
        ("Partners", "company/partners.html"),
    ]),
]

STYLE = """
:root{--navy:#24282b;--deep:#24282b;--blue:#b3291b;--lift:#b3291b;--paper:#f7f4ef;
--ink:#1c2528;--soft:#514b46;--rule:#ded7ce;--flag:#b42318;--hold:#1f7a4d;--warn:#c98200}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}
body{margin:0;font-family:'DM Sans',system-ui,sans-serif;font-size:17px;line-height:1.6;color:var(--ink);background:#fff;-webkit-font-smoothing:antialiased}
.wrap{max-width:1160px;margin:0 auto;padding:0 28px}
a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}
:focus-visible{outline:3px solid var(--blue);outline-offset:3px}
h1,h2,h3,h4{letter-spacing:-.02em}


/* ---- visual layer ----------------------------------------------------
   The brand asset carries photography, depth and iconography. Austere type
   on white and "unfinished" are hard to tell apart, and next to that asset
   the earlier build read as a draft. This adds weight without inventing
   claims: a real diagram, real icons, and depth in the dark bands. */

.hero, .phead, .band {
  background:
    radial-gradient(1100px 520px at 76% -8%, rgba(83,68,59,.34), transparent 60%),
    radial-gradient(760px 420px at 8% 108%, rgba(62,50,44,.55), transparent 62%),
    linear-gradient(168deg, #24282b 0%, #24282b 54%, #24282b 100%);
  position:relative; overflow:hidden;
}
.hero::after, .phead::after, .band::after{
  content:""; position:absolute; inset:0; pointer-events:none;
  background-image:linear-gradient(rgba(255,255,255,.028) 1px, transparent 1px),
                   linear-gradient(90deg, rgba(255,255,255,.028) 1px, transparent 1px);
  background-size:52px 52px;
  mask-image:radial-gradient(900px 480px at 72% 8%, #000 0%, transparent 72%);
}
.hero>.wrap,.phead>.wrap,.band>.wrap{position:relative;z-index:2}
.rule-accent{width:56px;height:3px;background:#ff6852;margin:0 0 22px;border-radius:2px}

/* the connected-operations diagram */
.opsmap{width:100%;max-width:560px;height:auto;display:block;margin:0 auto}
.opsmap .hub{fill:rgba(255,104,82,.16);stroke:#ff6852;stroke-width:1.5}
.opsmap .node{fill:rgba(255,255,255,.07);stroke:rgba(227,217,204,.55);stroke-width:1.2}
.opsmap .link{stroke:rgba(233,151,131,.5);stroke-width:1.2;fill:none}
.opsmap .dot{fill:#ff6852}
.opsmap text{font-family:'DM Sans',sans-serif;font-size:11.5px;font-weight:600;
  fill:#f4eee6;letter-spacing:.05em}
.opsmap .hubtext{font-size:13px;fill:#fff;letter-spacing:.09em}

/* iconography */
.ico{width:44px;height:44px;border-radius:9px;background:var(--navy);display:flex;
  align-items:center;justify-content:center;flex:0 0 44px}
.ico svg{width:22px;height:22px;stroke:#ff8a76;stroke-width:1.7;fill:none;
  stroke-linecap:round;stroke-linejoin:round}
.ico.light{background:#eee9e1}
.ico.light svg{stroke:var(--blue)}

/* connected operations list, as on the brand asset */
.ops{display:flex;flex-direction:column;gap:2px}
.opitem{display:flex;gap:16px;align-items:center;padding:13px 0;border-bottom:1px solid var(--rule)}
.opitem:last-child{border-bottom:0}
.opitem b{font-size:16px;font-weight:700;letter-spacing:.01em;display:block}
.opitem span{font-size:14.5px;color:var(--soft);display:block;margin-top:1px}
.opitem a{display:flex;gap:16px;align-items:center;width:100%}
.opitem a:hover{text-decoration:none}
.opitem a:hover b{color:var(--blue)}

/* leadership band */
.lead3{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-top:40px;
  border-top:1px solid var(--rule)}
@media(max-width:980px){.lead3{grid-template-columns:1fr}}
.lead3>div{padding:30px 34px 30px 0;border-right:1px solid var(--rule)}
.lead3>div:last-child{border-right:0;padding-right:0}
.lead3>div:not(:first-child){padding-left:34px}
@media(max-width:980px){.lead3>div{border-right:0;border-bottom:1px solid var(--rule);
  padding:26px 0}.lead3>div:not(:first-child){padding-left:0}}
.lead3 h3{font-size:17.5px;font-weight:700;margin:16px 0 7px}
.lead3 p{font-size:15.5px;color:var(--soft);line-height:1.55;margin:0}

/* wedge steps */
.wedge{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:38px}
@media(max-width:800px){.wedge{grid-template-columns:1fr}}
.wedge>div{padding:26px 28px;background:rgba(255,255,255,.055);
  border:1px solid rgba(255,255,255,.14);border-radius:4px}
.wedge b{display:block;font-size:17px;color:#fff;margin:0 0 7px}
.wedge span{font-size:15.5px;color:#e3d9cc;line-height:1.55}

/* strapline */
.strap{background:#24282b;color:#e3d9cc;text-align:center;padding:22px 0;
  font-size:13px;letter-spacing:.34em;font-weight:600}


/* ---- narrative acts ---------------------------------------------------
   Youverify's strongest page element follows two customers through the
   product rather than describing it. Ours follows one agent — and carries on
   past where theirs stops, into the part where somebody external asks
   whether any of it can be evidenced. */
.acts{margin-top:8px}
.act{display:grid;grid-template-columns:132px minmax(0,1fr) minmax(0,.92fr);
  gap:34px;padding:34px 0;border-top:1px solid rgba(255,255,255,.14);align-items:start}
.act:first-child{border-top:0}
@media(max-width:940px){.act{grid-template-columns:104px 1fr;gap:18px}
  .act .actpanel{grid-column:2}}
@media(max-width:560px){.act{grid-template-columns:1fr}.act .actpanel{grid-column:1}}
.act .when{font-family:ui-monospace,monospace;font-size:12px;color:#e3d9cc;
  letter-spacing:.06em;padding-top:4px;line-height:1.5}
.act .when b{display:block;color:#ff6852;font-weight:600;margin-bottom:3px}
.act h3{font-size:20px;font-weight:700;color:#fff;margin:0 0 9px;line-height:1.26}
.act p{font-size:16px;line-height:1.6;color:#e3d9cc;margin:0 0 10px}
.act p:last-child{margin:0}
.act .actpanel{background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.14);
  border-radius:4px;padding:16px 18px}
.act .actpanel .k{display:flex;justify-content:space-between;gap:12px;
  padding:7px 0;font-size:13.5px;color:#e3d9cc;border-bottom:1px solid rgba(255,255,255,.09)}
.act .actpanel .k:last-child{border-bottom:0}
.act .actpanel .k b{color:#fff;font-weight:600}
.act .actpanel .mono{font-family:ui-monospace,monospace;font-size:11.5px;color:#ff8a76}

/* designed-for band */

.desk{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:6px;padding:22px 24px}
.desk-h{margin:0 0 8px;color:#ff6852;font-size:12.5px;letter-spacing:.14em;font-weight:600;text-transform:uppercase}
.desk a{display:flex;justify-content:space-between;gap:12px;padding:12px 0;color:#fff;font-size:16px;border-bottom:1px solid rgba(255,255,255,.12)}
.desk a:last-child{border-bottom:0}
.desk a span{color:#ff8a76}
.desk a:hover{text-decoration:none;color:#ff6852}
.sectors{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:34px}
@media(max-width:1000px){.sectors{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.sectors{grid-template-columns:1fr}}
a.sector{display:block;padding:0;overflow:hidden;background:#fff;border:1px solid var(--rule);border-radius:4px;color:inherit}
a.sector:hover{text-decoration:none;box-shadow:0 10px 26px rgba(8,23,40,.09)}
a.sector img{width:100%;display:block;aspect-ratio:16/10;object-fit:cover}
a.sector>div{padding:18px 20px 20px}
a.sector h3{margin:0 0 6px;font-size:17px}
a.sector p{margin:0;font-size:15px;color:var(--soft);line-height:1.5}
a.sector p.go{margin-top:12px;color:var(--blue);font-weight:600;font-size:14.5px}
.designed{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--rule);
  border:1px solid var(--rule);margin-top:40px}
@media(max-width:900px){.designed{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.designed{grid-template-columns:1fr}}
.designed>div{background:#fff;padding:26px 24px}
.designed .lab{font-family:ui-monospace,monospace;font-size:11.5px;color:var(--blue);
  letter-spacing:.06em;margin:0 0 9px}
.designed h4{margin:0 0 7px;font-size:16.5px;font-weight:700}
.designed p{margin:0;font-size:15px;color:var(--soft);line-height:1.55}


/* ---- inline calls to action ------------------------------------------
   Placed at the moment a reader has just been given a reason, not sprayed
   through the page. Each one asks for the next step that actually follows
   from what they have read. */
.ctaband{background:var(--paper);border:1px solid var(--rule);border-left:4px solid var(--blue);
  padding:30px 34px;margin:46px 0 0;display:grid;grid-template-columns:1fr auto;
  gap:32px;align-items:center}
@media(max-width:820px){.ctaband{grid-template-columns:1fr;gap:20px}}
.ctaband .kick{font-family:ui-monospace,monospace;font-size:11.5px;color:var(--blue);
  letter-spacing:.07em;margin:0 0 8px}
.ctaband h3{font-size:21px;font-weight:700;margin:0 0 8px;line-height:1.28;max-width:30ch}
.ctaband p{font-size:16px;color:var(--soft);line-height:1.55;margin:0;max-width:56ch}
.ctaband .acts{display:flex;gap:11px;flex-wrap:wrap}
.ctaband .btn{padding:13px 22px;font-size:15.5px;background:var(--blue);color:#fff;
  border-color:var(--blue);white-space:nowrap}
.ctaband .btn:hover{background:var(--lift)}
.ctaband .btn.quiet{background:#fff;color:var(--blue);border-color:var(--rule)}
.ctaband .btn.quiet:hover{background:var(--paper)}
.ctaband.dark{background:rgba(255,255,255,.055);border-color:rgba(255,255,255,.16);
  border-left-color:#ff6852}
.ctaband.dark h3{color:#fff}
.ctaband.dark p{color:#e3d9cc}
.ctaband.dark .btn{background:#fff;color:var(--navy);border-color:#fff}
.ctaband.dark .btn.quiet{background:transparent;color:#fff;border-color:rgba(255,255,255,.42)}


/* ---- display type -----------------------------------------------------
   The brand asset sets its headline in a serif. Public Sans carries the
   body; the serif carries the voice. */
h1, h2.head, .journey h2, .cta h2, .phead h1, .ctaband h3{
  font-family:'DM Sans',system-ui,sans-serif;
  letter-spacing:-.012em;
}
.hero h1{font-weight:600;line-height:1.02;letter-spacing:-.018em}
h2.head, .journey h2, .cta h2{font-weight:600}
.phead h1{font-weight:600}

/* eyebrow — positions the offer before the headline reads */
.eyebrow{
  font-family:'DM Sans',sans-serif;
  font-size:12.5px;font-weight:700;letter-spacing:.13em;
  color:#ff6852;margin:0 0 20px;text-transform:uppercase;
}
.phead .eyebrow{color:#ff6852}

/* one bright call to action rather than two of equal weight */
.btn.gold{background:#ff6852;border-color:#ff6852;color:#24282b;font-weight:700}
.btn.gold:hover{background:#ff8a76;border-color:#ff8a76}
.hero .hbtns{align-items:center}
.hero .textlink{color:#e3d9cc;font-size:15.5px;font-weight:600;padding:14px 4px}
.hero .textlink:hover{color:#fff}

/* nav with dropdowns */
nav{position:sticky;top:0;z-index:70;background:rgba(11,31,54,.98);backdrop-filter:blur(8px)}
nav .wrap{display:flex;align-items:center;justify-content:space-between;height:68px}
.logo{font-weight:700;font-size:20px;letter-spacing:.1em;color:#fff}
.logo:hover{text-decoration:none}
.nl{display:flex;gap:4px;align-items:center}
.navitem{position:relative}
.navitem>a{color:#e3d9cc;font-size:15px;padding:10px 14px;display:inline-block;border-radius:3px}
.navitem>a:hover,.navitem:hover>a{color:#fff;text-decoration:none;background:rgba(255,255,255,.07)}
.navitem>a[aria-current]{color:#fff}
.drop{position:absolute;top:100%;left:0;min-width:270px;background:#fff;border:1px solid var(--rule);
  border-radius:4px;box-shadow:0 20px 44px rgba(6,20,38,.26);padding:8px;display:none}
.navitem:hover .drop,.navitem:focus-within .drop{display:block}
.drop a{display:block;padding:10px 13px;font-size:15px;color:var(--ink);border-radius:3px}
.drop a.sub,.mg a.sub{padding-left:26px;font-size:14.5px;color:var(--soft)}
.drop a:hover{background:var(--paper);text-decoration:none;color:var(--blue)}
.nbtn{background:#fff;color:var(--navy)!important;padding:9px 18px;border-radius:3px;font-weight:600;margin-left:10px}
.nbtn:hover{background:#eee9e1;text-decoration:none}
@media(max-width:980px){.navitem:not(.cta){display:none}}
.mnav{display:none}
@media(max-width:980px){.mnav{display:block;margin-left:8px}
.mnav summary{list-style:none;cursor:pointer;color:#fff;font-size:15px;padding:10px 12px;border:1px solid rgba(255,255,255,.25);border-radius:3px}
.mnav summary::-webkit-details-marker{display:none}
.mpanel{position:absolute;left:0;right:0;top:100%;background:#fff;max-height:80vh;overflow:auto;padding:10px 20px 18px;box-shadow:0 18px 40px rgba(8,23,40,.25)}
.mg{padding:10px 0;border-bottom:1px solid var(--rule)}.mg:last-child{border-bottom:0}
.mg a{display:block;padding:7px 0;color:var(--ink);font-size:15.5px}
.mg a.mh{font-weight:700;color:var(--blue);font-size:13px;letter-spacing:.1em;text-transform:uppercase}}
.nbtn{white-space:nowrap}
@media(max-width:420px){.nbtn{padding:9px 11px!important;font-size:14px!important}.logo{font-size:17px!important;letter-spacing:.12em!important}}

/* page head */
.phead{background:var(--deep);color:#fff;padding:72px 0 76px;position:relative;overflow:hidden}
.phead::before{content:"";position:absolute;inset:0;background:radial-gradient(900px 380px at 80% -10%,rgba(119,94,77,.28),transparent 62%)}
.phead .wrap{position:relative}
.crumb{font-size:13.5px;color:#e3d9cc;margin:0 0 14px}
.crumb a{color:#e3d9cc}
.phead h1{font-size:clamp(32px,4.4vw,50px);line-height:1.08;font-weight:700;margin:0 0 18px;max-width:20ch}
.phead p{font-size:19px;color:#e3d9cc;max-width:56ch;margin:0;line-height:1.55}

/* hero (home only) */
.hero{background:var(--deep);color:#fff;padding:92px 0 100px;position:relative;overflow:hidden}
.hero::before{content:"";position:absolute;inset:0;background:radial-gradient(1000px 420px at 78% -5%,rgba(119,94,77,.30),transparent 62%)}
.hero .wrap{position:relative}
.hgrid{display:grid;grid-template-columns:1.12fr .88fr;gap:48px;align-items:center}
@media(max-width:940px){.hgrid{grid-template-columns:1fr;gap:38px}}
.hero h1{font-size:clamp(36px,5.1vw,60px);line-height:1.05;font-weight:700;margin:0 0 22px}
.hero .lede{font-size:clamp(17px,2vw,20px);color:#e3d9cc;margin:0 0 34px;max-width:50ch;line-height:1.55}
.btns{display:flex;gap:12px;flex-wrap:wrap}
.hero .btn{padding:14px 22px;font-size:15.5px}
.btn{display:inline-block;padding:14px 26px;border-radius:3px;font-weight:600;font-size:16px;background:#fff;color:var(--navy);border:1px solid #fff}
.btn:hover{text-decoration:none;background:#eee9e1}
.btn.ghost{background:transparent;color:#fff;border-color:rgba(255,255,255,.42)}
.btn.ghost:hover{background:rgba(255,255,255,.09)}
.btn.solid{background:var(--blue);border-color:var(--blue);color:#fff}
.btn.solid:hover{background:var(--lift)}

#control-walkthrough,#sector-films,#sample-board-pack,#enquiry{scroll-margin-top:92px}
.control-preview,.specimen{padding:clamp(20px,4vw,34px);border:1px solid var(--rule);border-radius:6px}
.control-preview h2,.specimen h3{margin:8px 0 20px;line-height:1.2}
.control-preview dl,.specimen dl{margin:0 0 18px}
.control-preview dt,.specimen dt{font-weight:700;margin-top:14px}
.control-preview dd,.specimen dd{margin:3px 0 0;color:var(--ink);line-height:1.55}
.walkthrough{align-items:start;margin-top:24px}
.walkthrough h3{margin:0 0 8px}
.walkthrough .body{margin-bottom:20px}
.specimen{background:var(--paper);border-top:4px solid var(--navy)}
.specimen-section{margin-top:40px}
.hero .hgrid > div{min-width:0}

/* panels */
.panel{background:#fff;color:var(--ink);border-radius:5px;box-shadow:0 30px 70px rgba(4,15,30,.42);overflow:hidden}
.panel-h{display:flex;justify-content:space-between;align-items:center;padding:14px 20px;border-bottom:1px solid var(--rule);background:#f7f4ef}
.panel-h b{font-size:14px}
.live{font-size:12px;color:var(--hold);font-weight:600;display:flex;align-items:center;gap:6px}
.live::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--hold)}
.row{display:flex;justify-content:space-between;align-items:center;gap:14px;padding:13px 20px;border-bottom:1px solid var(--rule);font-size:14.5px}
.row .who{display:flex;flex-direction:column;gap:2px}
.row .meta{font-family:ui-monospace,monospace;font-size:11.5px;color:var(--soft)}
.pill{font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:20px;white-space:nowrap}
.pill.f{background:#fdeceb;color:var(--flag)}
.pill.a{background:#fff6e6;color:var(--warn)}
.pill.ok{background:#eaf6ef;color:var(--hold)}
.panel-f{padding:12px 20px;background:#f7f4ef;font-size:12.5px;color:var(--soft)}

/* sections */
.sec{padding:86px 0}
.sec.wash{background:var(--paper);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.sec.tight{padding:62px 0}
h2.head{font-size:clamp(26px,3.3vw,38px);line-height:1.15;font-weight:700;margin:0 0 18px;max-width:23ch}
h3.sub{font-size:21px;font-weight:700;margin:38px 0 12px}
p.lead{font-size:18px;line-height:1.62;color:var(--soft);max-width:64ch;margin:0 0 16px}
p.lead strong{color:var(--ink);font-weight:600}
p.body{font-size:17px;line-height:1.62;color:var(--soft);max-width:64ch;margin:0 0 15px}
p.body strong{color:var(--ink);font-weight:600}

.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--rule);border:1px solid var(--rule);margin-top:42px}
@media(max-width:900px){.grid3{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.grid3{grid-template-columns:1fr}}
.cell{background:#fff;padding:28px 26px 30px}
.cell h3{font-size:17.5px;font-weight:700;margin:0 0 8px}
.cell p{font-size:15px;line-height:1.56;color:var(--soft);margin:0}
.cell a{font-size:15px;font-weight:600;display:inline-block;margin-top:12px}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:42px}
@media(max-width:760px){.grid2{grid-template-columns:1fr}}
.card{background:#fff;border:1px solid var(--rule);padding:28px 28px 30px}
.card h3{font-size:19px;font-weight:700;margin:0 0 4px}
.card .cap{font-size:14px;color:var(--blue);font-weight:600;margin:0 0 18px}
.card ul{margin:0;padding:0;list-style:none}
.card li{font-size:15px;color:var(--soft);padding:8px 0;border-top:1px solid var(--rule);line-height:1.45}
.card li:first-child{border-top:0;padding-top:0}

.bridge{background:var(--navy);color:#fff;padding:32px 34px;margin-top:18px}
.bridge h3{font-size:19px;font-weight:700;margin:0 0 3px;color:#fff}
.bridge .cap{font-size:14px;color:#ff8a76;font-weight:600;margin:0 0 18px}
.bridge p{font-size:16.5px;line-height:1.6;color:#e3d9cc;margin:0;max-width:64ch}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 0}
.tags span{font-family:ui-monospace,monospace;font-size:12px;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.17);padding:5px 10px;border-radius:2px;color:#f4eee6}

.split{display:grid;grid-template-columns:1fr 1.02fr;gap:52px;align-items:start;margin-top:42px}
@media(max-width:940px){.split{grid-template-columns:1fr;gap:32px}}
.point{border-top:1px solid var(--rule);padding:20px 0}
.point h4{margin:0 0 5px;font-size:17px;font-weight:700}
.point p{margin:0;font-size:15.5px;color:var(--soft);line-height:1.56}

.report{background:#fff;border:1px solid var(--rule);border-radius:4px;overflow:hidden}
.report-h{padding:18px 22px;border-bottom:1px solid var(--rule)}
.report-h b{font-size:15px}
.report-h div{font-family:ui-monospace,monospace;font-size:12px;color:var(--soft);margin-top:4px}
.finding{padding:18px 22px;border-bottom:1px solid var(--rule)}
.finding:last-child{border-bottom:0}
.finding.bad{border-left:4px solid var(--flag)}
.finding.good{border-left:4px solid var(--hold)}
.finding p{margin:0;font-size:15px;line-height:1.55}
.finding .cite{font-family:ui-monospace,monospace;font-size:11.5px;color:var(--soft);display:block;margin-top:8px}

.steps{counter-reset:s;margin-top:42px;border-top:1px solid var(--rule)}
.stp{display:grid;grid-template-columns:54px minmax(0,.8fr) minmax(0,1.2fr);gap:26px;padding:30px 0;border-bottom:1px solid var(--rule);align-items:start}
@media(max-width:820px){.stp{grid-template-columns:44px 1fr;gap:14px}.stp .sd{grid-column:2}}
.stp .sn{font-family:ui-monospace,monospace;font-size:14px;color:var(--blue);font-weight:500;padding-top:3px}
.stp h3{font-size:19px;font-weight:700;margin:0;line-height:1.3}
.stp p{font-size:16.5px;line-height:1.6;color:var(--soft);margin:0 0 12px}
.stp p:last-child{margin:0}
.stp .aside{font-size:15px;border-left:3px solid var(--rule);padding-left:15px}

.tbl{border:1px solid var(--rule);margin-top:42px;background:#fff}
.trow{display:grid;grid-template-columns:180px 1fr;border-top:1px solid var(--rule)}
.trow:first-child{border-top:0}
.trow div{padding:16px 24px;font-size:15.5px}
.trow div:first-child{font-weight:600;border-right:1px solid var(--rule)}
.trow .ref{font-family:ui-monospace,monospace;font-size:13px;color:var(--soft);display:block;margin-top:3px}
@media(max-width:600px){.trow{grid-template-columns:1fr}.trow div:first-child{border-right:0;padding-bottom:0}}

.quote{border-left:4px solid var(--blue);padding:4px 0 4px 22px;margin:34px 0;max-width:62ch}
.quote p{font-size:19px;line-height:1.5;color:var(--ink);margin:0;font-weight:500}

/* cta band */
section.cta{background:var(--deep);color:#fff;padding:80px 0}
.cta-grid{display:grid;grid-template-columns:1.05fr 1fr;gap:52px;align-items:start}
@media(max-width:900px){.cta-grid{grid-template-columns:1fr;gap:32px}}
.cta h2{font-size:clamp(26px,3.3vw,38px);font-weight:700;margin:0 0 16px;line-height:1.15;max-width:19ch}
.cta p{color:#e3d9cc;font-size:17.5px;line-height:1.6;max-width:44ch;margin:0 0 16px}
.cta h4{color:#fff;font-size:17px;margin:26px 0 8px;font-weight:600}
form{background:#fff;padding:28px 28px 30px;border-radius:4px}
.contact-grid{display:grid;grid-template-columns:1fr 1.15fr;gap:56px;align-items:start}
@media(max-width:900px){.contact-grid{grid-template-columns:1fr;gap:32px}}
.contact-grid form{border:1px solid var(--rule);box-shadow:0 10px 30px rgba(8,23,40,.06)}
.routes{list-style:none;margin:18px 0 8px;padding:0;border-top:1px solid var(--rule)}
.routes li{padding:13px 0;border-bottom:1px solid var(--rule)}
.routes b{font-size:16.5px;color:var(--ink);font-weight:600}
.routes b{display:block;margin-bottom:3px}
.routes span{font-size:15px;color:var(--soft);line-height:1.5;display:block}
.f{margin:0 0 16px}
.f label{display:block;font-size:14px;font-weight:600;margin:0 0 6px;color:var(--ink)}
.f input,.f textarea{width:100%;padding:11px 13px;font:inherit;font-size:16px;border:1px solid var(--rule);border-radius:3px;color:var(--ink)}
.f input:focus,.f textarea:focus{border-color:var(--blue);outline:2px solid rgba(179,41,27,.16)}
.f textarea{min-height:84px;resize:vertical}
.f .hint{font-size:13px;color:var(--soft);margin:6px 0 0}
.opts{display:flex;gap:10px;flex-wrap:wrap}
.opts label{flex:1 1 170px;border:1px solid var(--rule);border-radius:3px;padding:12px 14px;cursor:pointer;font-size:15px;font-weight:500;display:flex;gap:9px;align-items:flex-start;line-height:1.4}
.opts input{width:auto;margin:3px 0 0;accent-color:var(--blue)}
.opts label:has(input:checked){border-color:var(--blue);box-shadow:inset 0 0 0 1px var(--blue)}
.opts small{display:block;font-weight:400;color:var(--soft);font-size:13.5px;margin-top:2px}
button.send{width:100%;padding:14px;font:inherit;font-size:16px;font-weight:600;background:var(--blue);color:#fff;border:0;border-radius:3px;cursor:pointer}
button.send:hover{background:var(--lift)}
.fnote{font-size:13.5px;color:var(--soft);margin:12px 0 0;line-height:1.5}
.cta form p.fnote,.cta form p.hint{font-size:13.5px;color:var(--soft);max-width:none;line-height:1.5}
.cta form p.hint{margin:6px 0 0}
.sent{background:#f3faf6;border-left:4px solid var(--hold);padding:22px 24px;border-radius:3px}
.sent h3{margin:0 0 7px;font-size:18px}
.sent p{margin:0;font-size:15.5px;color:var(--soft);line-height:1.55}

/* next links */
.next{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:40px}
@media(max-width:820px){.next{grid-template-columns:1fr}}
.next a{background:#fff;border:1px solid var(--rule);padding:22px 24px;display:block}
.next a:hover{border-color:var(--blue);text-decoration:none}
.next b{display:block;font-size:16.5px;color:var(--ink);margin:0 0 5px}
.next span{font-size:14.5px;color:var(--soft);line-height:1.5;display:block}

footer{background:#24282b;color:#ded7ce;padding:54px 0 42px;font-size:14.5px}
.fg{display:grid;grid-template-columns:1.4fr repeat(4,1fr);gap:30px}
@media(max-width:940px){.fg{grid-template-columns:1fr 1fr}}
footer h5{color:#fff;font-size:13.5px;font-weight:600;margin:0 0 13px}
footer ul{list-style:none;margin:0;padding:0}
footer li{margin:0 0 9px}
footer a{color:#ded7ce;font-size:14px}
.fbot{border-top:1px solid #24282b;margin-top:38px;padding-top:24px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:13.5px}
/* Customer-facing landing pages */
.skip-link{position:fixed;top:8px;left:8px;z-index:90;transform:translateY(-160%);padding:8px 14px;background:#fff}
.skip-link:focus{transform:none}
nav{background:rgba(255,255,255,.98);border-bottom:1px solid var(--rule)}
nav .logo{color:var(--deep)}
.navitem>a{color:var(--ink)}
.navitem>a:hover,.navitem:hover>a,.navitem>a[aria-current]{color:var(--blue);background:var(--paper)}
nav .nbtn{background:var(--blue);color:white!important;border-radius:6px}
nav .nbtn:hover{background:var(--navy)}
nav .mnav summary{color:var(--ink);border-color:var(--rule)}
.btn.outline{color:var(--blue);border-color:#ded7ce;background:transparent}
.btn.outline:hover{background:#eee9e1}
#journey,#see-it-working,#institutions,#content{scroll-margin-top:86px}
.section-intro{max-width:690px;margin-bottom:32px}
.section-intro h2,.customer-close h2{font-family:'DM Sans',system-ui,sans-serif;font-size:clamp(32px,4.6vw,54px);line-height:1.06;margin:0 0 14px}
.journey-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(24px,5vw,70px);align-items:start}
.journey-grid>*{min-width:0}
.journey-steps{border-top:1px solid var(--rule)}
.journey-steps details{border-bottom:1px solid var(--rule);padding:15px 0}
.journey-steps summary{cursor:pointer;font-size:19px;font-weight:700;color:var(--navy)}
.journey-steps p{margin:10px 0;color:var(--soft)}
.journey-film{margin:0;padding:14px;background:#eee9e1;border-radius:12px}
.journey-film video{aspect-ratio:16/9}
.journey-film .platform-overview-player{display:block;width:100%;max-width:100%;height:auto;object-fit:contain;background:#0a141f;border-radius:6px;margin-bottom:16px}
.journey-film figcaption{color:var(--soft);font-size:14px}
.outcomes{background:#f7f4ef}
.outcome-grid article{border-top:3px solid #ded7ce;padding-top:10px}
.outcome-grid p,.institution-grid p{color:var(--soft)}
.section-link{display:inline-block;margin-top:20px;font-weight:700}
.institution-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.institution-grid>a{display:block;background:white;border:1px solid var(--rule);border-radius:10px;padding:22px;color:var(--ink)}
.institution-grid>a:hover{border-color:var(--blue);text-decoration:none;background:#f7f4ef}
.institution-grid img{display:block;width:100%;aspect-ratio:2.35;object-fit:cover;object-position:center 60%;border-radius:6px;margin-bottom:16px}
.institution-grid h3{margin:0}
.institution-grid a>span{font-size:15px;font-weight:700;color:var(--blue)}
.customer-close{background:var(--deep);color:white}
.customer-close p{color:#ded7ce;max-width:56ch}
.customer-close aside{border:1px solid #514b46;border-radius:10px;padding:24px}
.customer-close aside h3{margin-top:0}
.customer-close aside a{color:#ff8a76}
@media(max-width:850px){
  .journey-grid{grid-template-columns:1fr}
}
@media(max-width:540px){
  nav .wrap{padding-inline:14px}
  .institution-grid{grid-template-columns:1fr}
}
/* Inferiva Structural homepage */
.structural-hero{position:relative;isolation:isolate;display:grid;align-items:center;min-height:clamp(440px,43vw,610px);padding:70px 0;color:white;text-align:center;background:var(--deep)}
.structural-hero img,.structural-hero::after{position:absolute;inset:0;width:100%;height:100%;z-index:-1}
.structural-hero img{object-fit:cover;object-position:center 63%}
.structural-hero::after{content:"";background:linear-gradient(115deg,rgba(24,23,22,.87),rgba(29,27,26,.64))}
.structural-hero h1{font:750 clamp(38px,6.35vw,86px)/.98 'DM Sans',system-ui,sans-serif;letter-spacing:-.05em;margin:0}
.structural-hero p{max-width:45ch;margin:22px auto 30px;color:#f4eee6;font-size:clamp(17px,2vw,23px)}
.splash{min-height:clamp(530px,calc(100svh - 70px),900px)}
.splash img{object-position:center 58%}
.splash::after{background:linear-gradient(110deg,rgba(24,23,22,.9),rgba(24,23,22,.53))}
.splash h1 span{color:#ff8a76}
.splash p{max-width:55ch}
.structural-hero .btns{justify-content:center}
.structural-hero .btn,.partner-band .btn{border-radius:8px}
.buyer-routes{padding:28px 0;background:white}
.buyer-routes .wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.buyer-routes a{padding:17px;text-align:center;color:var(--navy);font-weight:700;border:1px solid var(--rule);border-radius:10px}
.buyer-routes a:hover{background:var(--paper)}
.solution-section .institution-grid{grid-template-columns:repeat(4,minmax(0,1fr))}
@media(max-width:950px){.solution-section .institution-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:540px){.solution-section .institution-grid{grid-template-columns:1fr}}
.offer-section,.resource-section{background:#eee9e1}
.offer-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}
.offer-grid article{background:white;border-radius:14px;border:1px solid var(--rule);overflow:hidden}
.offer-grid img{display:block;width:100%;height:auto;aspect-ratio:2.15;object-fit:cover;object-position:center 60%}
.offer-grid article div{padding:24px 26px 28px}
.offer-grid h3{font-size:24px;line-height:1.2;margin:0}
.offer-grid p,.partner-band p{color:var(--soft)}
.offer-grid a{font-weight:700}
.partner-band{padding:34px 0;background:white}
.partner-band .wrap{display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap}
.partner-band h2,.partner-band p{margin:0}
#home,#solutions,#platform,#assurance,#resources,#partners,#contact{scroll-margin-top:90px}
nav .logo{letter-spacing:0;font-size:19px}
@media(max-width:540px){
  nav .logo{font-size:15px!important;letter-spacing:0!important}
  .structural-hero{padding:52px 0;min-height:420px}
  .buyer-routes .wrap,.offer-grid{grid-template-columns:1fr}
}
"""

STYLE += """
.home-two{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,84px)}
.home-platform h2,.home-film h2,.home-leadership h2,.home-start h2{font:700 clamp(2rem,4vw,3.25rem)/1.1 'DM Sans',system-ui,sans-serif;margin:0 0 23px}
.home-operations-title{font-size:.92rem;letter-spacing:.15em;text-transform:uppercase;color:var(--soft);margin:0 0 16px}
.home-capabilities{padding:0;margin:0;list-style:none}
.home-capabilities li+li{border-top:1px solid var(--rule)}
.home-capabilities a{display:grid;grid-template-columns:54px minmax(0,1fr);align-items:center;gap:20px;padding:22px 0;color:var(--navy)}
.home-capabilities a:hover strong{text-decoration:underline;text-underline-offset:.2em}
.home-capabilities .ico{width:54px;height:54px;margin:0;border-radius:11px;background:#f9e8e1;color:#b3291b;display:grid;place-items:center}
.home-capabilities .ico svg{stroke:currentColor}
.home-capabilities .operation-copy{display:grid;gap:4px}
.home-capabilities .operation-copy>span{color:var(--soft)}
.home-film{scroll-margin-top:85px}
.home-film .journey-film{max-width:1000px;margin:0}
.home-film video{display:block;width:100%;aspect-ratio:16/9;background:var(--deep)}
.home-three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin:30px 0}
.home-three article{padding:24px;border:1px solid var(--rule);border-radius:8px}
.home-three h3{margin:10px 0}
.home-three p{margin:0}
.home-start{background:linear-gradient(120deg,#24282b,#24282b);color:white}
.home-start .lead,.home-start p{color:#f4eee6}
.home-start article{border-color:#ffffff44;background:#ffffff08}
nav a.active-section,nav a[aria-current=page]{text-decoration:underline;text-underline-offset:5px}
@media(max-width:760px){.home-two,.home-three{grid-template-columns:1fr}}
"""

STYLE += """
nav .navitem{display:flex;align-items:center}
nav .navitem>a{padding-inline:9px}
.nav-disclosure summary{display:grid;place-items:center;width:26px;height:34px;cursor:pointer;list-style:none;color:var(--ink)}
.nav-disclosure summary::-webkit-details-marker{display:none}
.nav-disclosure summary::after{content:"";width:7px;height:7px;border-right:2px solid;border-bottom:2px solid;transform:rotate(45deg)}
.nav-submenu{position:absolute;top:100%;left:0;width:max-content;max-width:290px;background:white;border:1px solid var(--rule);padding:8px;border-radius:6px;box-shadow:0 10px 28px #1c252825}
.navitem:nth-last-of-type(-n+2) .nav-submenu{left:auto;right:0}
.nav-submenu a{display:block;padding:8px 12px;color:var(--ink)}
.nav-submenu a:hover,.nav-submenu a[aria-current]{background:var(--paper)}
.mg a:first-child{font-weight:700}
.mg a+a{padding-left:14px}
footer h5 a{color:inherit}
@media(max-width:980px){nav .navitem{display:none}}
"""

SCRIPT = """
document.querySelectorAll('.nav-disclosure').forEach(function (menu) {
  menu.addEventListener('toggle', function () {
    if (menu.open) document.querySelectorAll('.nav-disclosure[open]').forEach(function (other) {
      if (other !== menu) other.open = false;
    });
  });
  menu.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && menu.open) {
      menu.open = false;
      menu.querySelector('summary').focus();
    }
  });
  document.addEventListener('click', function (event) {
    if (!menu.parentElement.contains(event.target)) menu.open = false;
  });
});

document.querySelectorAll('.mnav a[href^="#"]').forEach(function (link) {
  link.addEventListener('click', function () {
    link.closest('details').open = false;
  });
});

(function () {
  var EMAIL = 'enquiries@inferivastructural.com';
  var form = document.getElementById('enquiry');
  if (!form) return;
  var note = form.querySelector('#note');
  function fit() {
    var r = form.querySelector('input[name=interest]:checked');
    if (r && note) note.placeholder = r.getAttribute('data-hint');
  }
  try {
    var t = new URLSearchParams(location.search).get('topic');
    var pick = t && form.querySelector('input[name=interest][value="' + t.replace(/[^a-z]/g, '') + '"]');
    if (pick) pick.checked = true;
  } catch (err) {}
  form.addEventListener('change', fit); fit();
  form.addEventListener('submit', function (e) {
    var endpoint = form.getAttribute('action');
    e.preventDefault();
    if (!endpoint) {
      var d = new FormData(form), lines = [];
      var topic = form.querySelector('input[name=interest]:checked');
      lines.push('Request: ' + (topic ? topic.parentNode.querySelector('span').firstChild.textContent.trim() : ''));
      [['Name','name'],['Email','email'],['Institution','organisation'],['Where we operate','markets'],['Notes','note']]
        .forEach(function (p) { lines.push(p[0] + ': ' + (d.get(p[1]) || '')); });
      location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('Enquiry: ' + lines[0].slice(9)) +
                      '&body=' + encodeURIComponent(lines.join('\\n'));
      return;
    }
    var b = form.querySelector('button.send');
    var previousError = form.querySelector('.err');
    if (previousError) previousError.remove();
    b.disabled = true; b.textContent = 'Sending\\u2026';
    fetch(endpoint, { method: 'POST', body: new FormData(form),
                      headers: { Accept: 'application/json' } })
      .then(function (r) { if (!r.ok) throw new Error(r.status);
        form.insertAdjacentHTML('beforebegin',
          '<div class="sent" role="status"><h3>Sent</h3><p>We will come back ' +
          'inside two working days.</p></div>');
        form.style.display = 'none'; })
      .catch(function () {
        b.disabled = false; b.textContent = 'Send enquiry';
        if (!form.querySelector('.err')) {
          b.insertAdjacentHTML('afterend',
            '<p class="fnote err" role="alert" style="color:#b42318">That did not send. Email us at ' +
            '<a href="mailto:' + EMAIL + '">' + EMAIL + '</a> and we will pick it up.</p>'); } });
  });
})();
"""


# --- icons, drawn once ----------------------------------------------------
ICONS = {
 "aml": '<path d="M3 21h18M5 21V9l7-5 7 5v12M9 21v-6h6v6"/>',
 "fraud": '<path d="M12 3l8 3v6c0 4.5-3.2 7.9-8 9-4.8-1.1-8-4.5-8-9V6z"/><path d="M9.5 12l1.8 1.8L15 10"/>',
 "customer": '<circle cx="12" cy="8" r="3.4"/><path d="M4.5 20a7.5 7.5 0 0 1 15 0"/>',
 "investigations": '<circle cx="10.5" cy="10.5" r="6"/><path d="M15.2 15.2L21 21"/>',
 "reporting": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h6M10 16h6"/>',
 "agents": '<circle cx="6" cy="7" r="2.4"/><circle cx="18" cy="7" r="2.4"/><circle cx="12" cy="17" r="2.4"/><path d="M7.6 8.8l3 6M16.4 8.8l-3 6M8.4 7h7.2"/>',
 "view": '<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z"/><circle cx="12" cy="12" r="2.6"/>',
 "governed": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/>',
 "measure": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
}

def icon(name: str, light: bool = False) -> str:
    return (f'<span class="ico{" light" if light else ""}">'
            f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg></span>')


def opsmap() -> str:
    """The connected-operations diagram.

    Six capabilities around one governed core — which is the argument the
    platform makes, drawn rather than asserted.
    """
    import math
    labels = [("AML", -90), ("FRAUD", -30), ("REGULATORY\nREPORTING", 30),
              ("PSP & AGENTS", 90), ("INVESTIGATIONS", 150), ("CUSTOMER RISK", 210)]
    cx, cy, r = 300, 210, 138
    links, nodes = "", ""
    for text, deg in labels:
        a = math.radians(deg)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        mx, my = cx + (r * .55) * math.cos(a + .28), cy + (r * .55) * math.sin(a + .28)
        links += f'<path class="link" d="M{cx},{cy} Q{mx:.0f},{my:.0f} {x:.0f},{y:.0f}"/>'
        nodes += f'<circle class="node" cx="{x:.0f}" cy="{y:.0f}" r="34"/>'
        nodes += f'<circle class="dot" cx="{x:.0f}" cy="{y:.0f}" r="3.4"/>'
        anchor = "middle"
        ty = y + (-46 if -135 < deg < -45 else 56)
        lines = text.split("\n")
        for i, ln in enumerate(lines):
            nodes += (f'<text x="{x:.0f}" y="{ty + i*14:.0f}" text-anchor="{anchor}">'
                      f'{ln}</text>')
    return f"""<svg class="opsmap" viewBox="0 0 600 430" role="img"
  aria-label="Six financial crime capabilities connected to one governed core">
  {links}
  <circle class="hub" cx="{cx}" cy="{cy}" r="62"/>
  <circle class="hub" cx="{cx}" cy="{cy}" r="46" style="fill:rgba(255,104,82,.24)"/>
  <text class="hubtext" x="{cx}" y="{cy-4}" text-anchor="middle">ONE</text>
  <text class="hubtext" x="{cx}" y="{cy+14}" text-anchor="middle">PLATFORM</text>
  {nodes}
</svg>"""


def cta(base: str, kicker: str, head: str, body: str, actions, dark: bool = False) -> str:
    """An inline call to action.

    Placed where a reader has just been given a reason to take the next step,
    and asking for the step that follows from what they have read — not the
    same generic ask on every page, which is what makes a CTA invisible.
    """
    btns = "".join(
        f'<a class="btn{"" if i == 0 else " quiet"}" href="{base}{href}">{label}</a>'
        for i, (label, href) in enumerate(actions))
    return f"""
<div class="ctaband{' dark' if dark else ''}">
  <div>
    {f'<p class="kick">{kicker}</p>' if kicker else ""}
    <h3>{head}</h3>
    <p>{body}</p>
  </div>
  <div class="acts">{btns}</div>
</div>"""


# What a visitor can ask for. Every "talk to us" link on the site names one of these
# (company/contact.html?topic=<key>), so the form opens on what the reader came for.
TOPICS = [
    ("briefing", "An executive briefing", "For a board, CEO or MLRO",
     "Who will attend, and what they need to decide",
     "An hour with your leadership on what one platform would change, and what it would not."),
    ("demo", "Request a live demo", "Set up for your markets and rules",
     "Your products, your markets and the systems you run today",
     "The platform configured for your jurisdictions, products and thresholds. Usually an hour."),
    ("diagnostic", "A diagnostic on your data", "Scope an extract-based review; no charge",
     "The control or workflow you want to examine",
     "We agree the scope and data transfer arrangements first, then review coverage, findings and priorities with you."),
    ("proof", "A proof-of-value engagement", "Start with a focused workflow",
     "The workflow you want to improve and how you would measure success",
     "Agree a workflow, baseline, success criteria and evidence before deciding whether to expand."),
    ("quote", "A quote", "Priced against your volumes",
     "Monthly transactions, records loaded, users and alerts (estimates are fine)",
     "Priced per module and by usage. Tell us your volumes and we send a quote."),
    ("assessment", "An independent assessment", "What you can evidence today",
     "An examination date, a finding to answer, or the board asking",
     "A scoped engagement, including what it will cost your team in time."),
    ("other", "Something else", "We will route it",
     "A deadline, a finding, a system you are replacing",
     "Partnerships, press, or anything else. It reaches a person."),
]


def form_html(base: str, topics=None, question: str = "What can we help with?",
              default: str = "demo", org_label: str = "Institution") -> str:
    topics = topics or TOPICS
    opts = "".join(
        f'<label><input type="radio" name="interest" value="{k}" data-hint="{hint}"'
        f'{" checked" if k == default else ""}><span>{t}<small>{sub}</small></span></label>'
        for k, t, sub, hint, _ in topics)
    action = f' action="{escape(ENQUIRY_ENDPOINT, quote=True)}"' if ENQUIRY_ENDPOINT else ''
    button = "Send enquiry" if ENQUIRY_ENDPOINT else "Open email draft"
    delivery_note = "" if ENQUIRY_ENDPOINT else "Review and send the draft from your email app."
    return f"""<form id="enquiry"{action} method="POST">
      <noscript><p>To enquire without JavaScript, email <a href="mailto:enquiries@inferivastructural.com">enquiries@inferivastructural.com</a>.</p></noscript>
      <div class="f"><label>{question}</label>
        <div class="opts">{opts}</div></div>
      <div class="f"><label for="name">Your name</label>
        <input id="name" name="name" type="text" autocomplete="name" required></div>
      <div class="f"><label for="email">Work email</label>
        <input id="email" name="email" type="email" autocomplete="email" required></div>
      <div class="f"><label for="org">{org_label}</label>
        <input id="org" name="organisation" type="text" autocomplete="organization" required></div>
      <div class="f"><label for="markets">Where you operate</label>
        <input id="markets" name="markets" type="text" placeholder="The countries you are licensed in">
        <p class="hint">So the right person replies, with the right rules in mind.</p></div>
      <div class="f"><label for="note">Anything we should know</label>
        <textarea id="note" name="note" placeholder="A deadline, a finding, a system you are replacing"></textarea></div>
      <p class="fnote">Please keep customer records and diagnostic extracts out of this form.</p>
      <button class="send" type="submit">{button}</button>
      <p class="fnote">{delivery_note} We use this to reply to your enquiry.
      Or email <a href="mailto:enquiries@inferivastructural.com">enquiries@inferivastructural.com</a>.</p>
    </form>"""


def form_block(base: str, headline: str = "", lede: str = "") -> str:
    headline = headline or "Tell us what you need"
    lede = lede or ("A briefing, a demonstration on your own rules, a diagnostic on your "
                    "own data, a quote or an assessment. Pick one and the reply comes from "
                    "someone who has read it.")
    return f"""
<section class="cta" id="contact">
  <div class="wrap cta-grid">
    <div>
      <h2>{headline}</h2>
      <p>{lede}</p>
      <h4>What happens next</h4>
      <p>One of us reads it, not a queue. We come back inside two working days
      with a time — or a straight answer about whether we are the right fit.</p>
    </div>
    {form_html(base)}
  </div>
</section>"""


def nav_html(base: str, active: str) -> str:
    desktop, mobile = [], []
    for label, href, children in NAV:
        current = ' aria-current="page"' if active == href else ""
        link = f'<a href="{base}{href}"{current}>{label}</a>'
        sublinks = "".join(
            f'<a href="{base}{path}"{" aria-current=page" if active == path else ""}>{name}</a>'
            for name, path in children
        )
        dropdown = (
            f'<details class="nav-disclosure"><summary aria-label="{label} links"></summary>'
            f'<div class="nav-submenu">{sublinks}</div></details>'
            if children else ""
        )
        desktop.append(f'<div class="navitem">{link}{dropdown}</div>')
        mobile.append(f'<div class="mg">{link}{sublinks}</div>')
    return ("".join(desktop) + '<details class="mnav"><summary>Menu</summary>'
            '<div class="mpanel">' + "".join(mobile) + '</div></details>')


def footer_html(base: str) -> str:
    html = ""
    for title, href, links in NAV:
        items = "".join(f'<li><a href="{base}{path}">{name}</a></li>' for name, path in links)
        html += f'<div><h5><a href="{base}{href}">{title}</a></h5><ul>{items}</ul></div>'
    return f"""
<footer>
  <div class="wrap">
    <div class="fg">
      <div><h5>INFERIVA</h5>
        <p style="margin:0;font-size:14px">Financial-crime software built by Inferiva Structural.</p></div>
      {html}
    </div>
    <div class="fbot"><span>&copy; 2026 Inferiva Structural</span></div>
  </div>
</footer>
<div class="strap">ONE FINANCIAL CRIME RISK. MANY MANIFESTATIONS.</div>"""


def page(path: str, title: str, desc: str, body: str, base: str,
         cta_headline: str = "", cta_lede: str = "", closing_form: bool = True) -> None:
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — INFERIVA</title>
<meta name="description" content="{desc}">
<style>
@font-face{{font-family:'DM Sans';src:url('{base}media/fonts/dm-sans-latin.woff2') format('woff2');font-style:normal;font-weight:400 800;font-display:swap}}
{STYLE}</style>
</head>
<body>
<a class="skip-link" href="#content">Skip to content</a>
<nav aria-label="Main navigation"><div class="wrap">
  <a class="logo" href="{base}index.html">Inferiva Structural</a>
  <div class="nl">{nav_html(base, path)}</div>
</div></nav>
<main id="content">
{body}
{form_block(base, cta_headline, cta_lede) if closing_form else ''}
</main>
{footer_html(base)}
<script>{SCRIPT}</script>
</body>
</html>
"""
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html, encoding="utf8")


def head(base: str, crumb: str, h1: str, lede: str, eyebrow: str = "") -> str:
    """Page head.

    The eyebrow states what the page is before the headline has to. Where none
    is given the breadcrumb does that work on its own.
    """
    brow = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    return f"""
<header class="phead"><div class="wrap">
  <p class="crumb">{crumb}</p>
  {brow}
  <h1>{h1}</h1>
  {f"<p>{lede}</p>" if lede else ""}
</div></header>"""


def nextlinks(base: str, items) -> str:
    cells = "".join(
        f'<a href="{base}{h}"><b>{t}</b><span>{d}</span></a>' for t, h, d in items)
    return f'<section class="sec tight wash"><div class="wrap">' \
           f'<h2 class="head" style="font-size:22px;margin-bottom:6px">Next</h2>' \
           f'<div class="next" style="margin-top:22px">{cells}</div></div></section>'


if __name__ == "__main__":
    import pages
    pages.build(page, head, nextlinks, icon, opsmap, cta, form_html, TOPICS)
    # The page was renamed from a Nigerian licence category to the global term. Links already
    # published (LinkedIn posts) point at the old address, so it forwards, keeping any tracking.
    old = OUT / "sectors" / "payment-service-banks.html"
    old.write_text("""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Agent networks and mobile wallets — INFERIVA</title>
<link rel="canonical" href="https://www.inferivastructural.com/sectors/agent-networks.html">
<meta http-equiv="refresh" content="0; url=agent-networks.html">
<script>location.replace('agent-networks.html' + location.search + location.hash);</script>
</head><body><p>This page has moved to <a href="agent-networks.html">Agent networks and mobile wallets</a>.</p></body></html>
""")
    print("  site built")
