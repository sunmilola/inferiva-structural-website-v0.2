"""Page content. One function per page, so copy lives apart from the shell."""


def build(page, head, nextlinks, icon, opsmap, cta, form_html, TOPICS):
    FILMS = {
        "agent-networks": ("agent-oversight", "Agent oversight",
            "Nine linked agents take thirty-six small deposits, none reportable on its own. Monitoring finds the network."),
        "development-finance": ("partner-bank", "Partner-bank assessment",
            "Three partner banks assessed in one pass: who owns them, who runs them, and what each file actually proves."),
        "commercial-banks": ("alert-quality", "Alert quality review",
            "A bank's alert extract, run rule by rule: where analysts' time goes, and a roadmap to fix it."),
    }
    # Sector pages only (not the home page's three recorded runs): a story film with platform screens.
    SECTOR_FILMS = dict(FILMS, microfinance=("microfinance", "One person, three job titles",
            "One compliance officer, three job titles, and an examiner's simplest question."))
    FILM_NOTE = {"microfinance": "Halima and her bank are illustrative; the screens are the platform's own."}

    def video(prefix, f):
        return (f'<video controls preload="none" playsinline poster="{prefix}media/films/{f}-poster.jpg" '
                f'style="width:100%;display:block;border-radius:6px;background:#0a141f;margin-bottom:16px">'
                f'<source src="{prefix}media/films/{f}.mp4" type="video/mp4">'
                f'<track kind="captions" srclang="en" label="English" src="{prefix}media/films/{f}.vtt" default></video>')

    def film_block(slug):
        if slug not in SECTOR_FILMS:
            return ""
        f, t, d = SECTOR_FILMS[slug]
        note = FILM_NOTE.get(slug, "A recorded run of the platform, on illustrative data.")
        return f"""
  <h3 class="sub">See it working</h3>
  <p class="body" style="max-width:64ch">{d} {note}</p>
  <div style="max-width:880px;margin-top:18px">{video("../", f)}</div>
"""

    # Sector diagnostics, listed on the diagnostic page.
    SECTORS = "".join(
        f'<a class="cell sector" href="sectors/{s}.html">'
        f'<img src="media/films/{f}-poster.jpg" alt="" loading="lazy">'
        f'<div><h3>{t}</h3><p>{l}</p><p class="go">See the diagnostic &rarr;</p></div></a>'
        for s, f, t, l in [
            ("agent-networks", "agent-oversight", "Agent networks and mobile wallets", "Oversee thousands of agents, and see the one that changed."),
            ("microfinance", "microfinance", "Microfinance banks", "Monitoring sized for a compliance team of one or two."),
            ("commercial-banks", "alert-quality", "Commercial banks", "Fewer wasted alerts, and evidence a correspondent will accept."),
            ("development-finance", "partner-bank", "Development finance", "Know what your partner banks' files actually prove."),
        ])
    specimen = """
<article class="specimen" aria-labelledby="specimen-title">
  <p class="cap">Illustrative board-pack extract · Synthetic data</p>
  <h3 id="specimen-title">Cash deposit monitoring needs a targeted review</h3>
  <dl>
    <dt>Scope</dt><dd>One bank, one cash-deposit scenario, 1–30 September 2026. Reviewed the alert extract, case dispositions and rule configuration history.</dd>
    <dt>Finding</dt><dd>Of 240 alerts, 180 were closed, including 12 escalated for further investigation. The remaining 60 were open at period end. Of the 180 closed alerts, 18 lacked a recorded decision rationale.</dd>
    <dt>Evidence limit</dt><dd>The extract supports an assessment of recorded outcomes and rationale. It cannot establish whether unalerted transactions should have triggered the rule. Open alerts were excluded from the closed-alert denominator.</dd>
    <dt>Decision requested</dt><dd>Assign the Head of Financial Crime Operations to review the 18 decisions and agree a targeted retest using source transactions before approving any threshold change.</dd>
  </dl>
</article>
"""

    institutions = (
        ("Commercial banks", "Connect risk decisions across onboarding, monitoring, fraud, investigations and reporting.", "commercial-banks", "london-financial-district"),
        ("Payments and mobile money", "See risk across customers, payments and agents so teams can act on the same information.", "agent-networks", "contactless-payment"),
        ("Digital lenders", "Review identity, ownership and application risk before deciding which applicants need a closer look.", "digital-lenders", "partner-review"),
        ("Microfinance institutions", "Give lean teams one place to manage alerts, decisions and deadlines across distributed operations.", "microfinance", "small-business-workspace"),
        ("Development finance", "Build a clearer picture of partner institutions, ownership and the evidence behind due diligence.", "development-finance", "partner-review"),
    )
    sector_outcomes = {slug: outcome for _, outcome, slug, _ in institutions}
    institution_cards = "".join(
        f'<a href="sectors/{slug}.html"><img src="media/brand/{photo}.webp" alt="" loading="lazy" decoding="async"><h3>{name}</h3><p>{outcome}</p><span>Explore {name.lower()} <span aria-hidden="true">→</span></span></a>'
        for name, outcome, slug, photo in institutions if slug != "development-finance"
    )

    page("index.html", "One financial crime risk. Many manifestations. | Inferiva Structural",
         "INFERIVA connects due diligence, AML, fraud, investigations, regulatory reporting and agent supervision.",
         f"""
<header class="structural-hero splash" id="home">
  <img src="media/brand/singapore-waterfront.webp" width="900" height="497" alt="" fetchpriority="high">
  <div class="wrap">
    <h1>One financial crime risk.<br><span>Many manifestations.</span></h1>
    <p>What looks like separate activity across customers, payments and networks can be part of the same pattern. INFERIVA connects the evidence so your teams can see it and act.</p>
    <div class="btns">
      <a class="btn solid" href="platform/index.html#see-it-working">See it working</a>
      <a class="btn ghost" href="start/diagnostic.html">Start with a diagnostic</a>
    </div>
  </div>
</header>

<section class="sec home-platform" aria-labelledby="home-platform-title"><div class="wrap home-two">
  <div>
    <h2 id="home-platform-title">A unified financial-crime operating platform</h2>
    <p class="lead">INFERIVA connects your financial-crime operations in one governed environment, from detection and customer risk through investigation, decision, reporting, evidence and improvement.</p>
    <p class="lead"><strong>One record, one decision trail, one account of what the institution actually did.</strong></p>
  </div>
  <div>
    <h3 class="home-operations-title">Connected operations</h3>
    <ul class="home-capabilities">
      <li><a href="platform/aml.html">{icon("aml")}<span class="operation-copy"><strong>AML</strong><span>Detection, scenarios and thresholds you can defend</span></span></a></li>
      <li><a href="platform/fraud.html">{icon("fraud")}<span class="operation-copy"><strong>Fraud</strong><span>Assess risk before funds move</span></span></a></li>
      <li><a href="platform/customer-risk.html">{icon("customer")}<span class="operation-copy"><strong>Customer risk</strong><span>Know who your customers are and how their risk changes</span></span></a></li>
      <li><a href="platform/investigations.html">{icon("investigations")}<span class="operation-copy"><strong>Investigations</strong><span>Bring transactions, evidence and decisions into one case</span></span></a></li>
      <li><a href="platform/reporting.html">{icon("reporting")}<span class="operation-copy"><strong>Regulatory reporting</strong><span>Prepare reports and retain evidence of the filing decision</span></span></a></li>
      <li><a href="platform/agent-supervision.html">{icon("agents")}<span class="operation-copy"><strong>PSP and agent supervision</strong><span>See patterns across agents, wallets and locations</span></span></a></li>
    </ul>
  </div>
</div></section>

<section class="sec wash home-leadership"><div class="wrap">
  <h2>What changes for leadership</h2>
  <div class="home-three">
    <article>{icon("view")}<h3>One connected view</h3><p>See customers, transactions, alerts, cases and risk in context.</p></article>
    <article>{icon("governed")}<h3>Governed decisions</h3><p>See who decided, when they acted and what evidence supported the decision.</p></article>
    <article>{icon("measure")}<h3>Measurable improvement</h3><p>Compare control outcomes with a recorded baseline and decide where to intervene.</p></article>
  </div>
  <a href="assurance/index.html">Explore assurance</a>
</div></section>

<section class="sec home-start"><div class="wrap">
  <h2>Start where the need is greatest</h2>
  <p class="lead">Deploy the INFERIVA capability you need first, alongside the systems you already use.</p>
  <div class="home-three">
    <article><h3>Deploy a focused capability</h3><p>Choose one workflow and agree the data, controls and outcomes in scope.</p></article>
    <article><h3>Demonstrate value</h3><p>Use your own data and measure the result against your starting point.</p></article>
    <article><h3>Expand on the same foundation</h3><p>Add workflows and carry forward the customer context, decisions and evidence.</p></article>
  </div>
  <div class="hbtns"><a class="btn gold" href="start/index.html">Explore ways to start</a><a class="textlink" href="institutions.html">Find your institution</a></div>
</div></section>
""", "", closing_form=False)

    page("solutions.html", "Financial crime solutions", "Connect the evidence across due diligence, monitoring, agent networks and fraud.",
         head("", '<a href="index.html">Home</a> · Financial crime solutions', "Financial crime solutions", "Connect the evidence across due diligence, monitoring, agent networks and fraud.") + """
<section class="sec solution-section" id="solutions"><div class="wrap">
  <div class="section-intro"><h2>Follow the risk wherever it appears</h2></div>
  <div class="institution-grid">
    <a href="platform/customer-risk.html"><h3>Due Diligence &amp; Customer Risk</h3><p>Know who you’re dealing with. Verify people and businesses, trace beneficial ownership and carry the evidence into ongoing risk reviews.</p><span>Explore customer risk</span></a>
    <a href="platform/aml.html"><h3>Monitoring &amp; Investigations</h3><p>Find suspicious activity in context. Give investigators the linked transactions, customer history and alert rationale in one case.</p><span>Explore monitoring</span></a>
    <a href="platform/agent-supervision.html"><h3>Agent &amp; Wallet Networks</h3><p>Detect patterns that emerge across agents, wallets and locations, including activity that looks ordinary in isolation.</p><span>Explore agent oversight</span></a>
    <a href="platform/fraud.html"><h3>Fraud Decisioning</h3><p>Use identity, device and payment signals to decide which applications and transactions to approve, refer or stop.</p><span>Explore fraud decisioning</span></a>
  </div>
</div></section>


<section class="sec tight wash"><div class="wrap"><h2>Run your financial crime operation on one platform</h2>
<p class="lead">Carry the evidence from the first signal through investigation, reporting and review.</p>
<a class="btn solid" href="platform/index.html">Explore the integrated platform</a></div></section>
""", "", closing_form=False)

    page("institutions.html", "Institutions", "See how financial crime controls apply across banking, payments, digital lending and microfinance.",
         head("", '<a href="index.html">Home</a> · Institutions', "Institutions", "See how financial crime controls apply across banking, payments, digital lending and microfinance.") + """
<section class="sec institution-section" id="institutions"><div class="wrap">
  <div class="section-intro">
    <h2>The same exposure takes different forms</h2>
    <p class="lead">A bank investigates an unusual wire. A payments firm traces activity across agents and wallets. A digital lender assesses an application before releasing funds. See the controls and evidence each team needs.</p>
  </div>
  <div class="institution-grid">""" + institution_cards + """</div>
</div></section>

""", "", closing_form=False)

    page("walkthrough.html", "See how INFERIVA works",
         "A commercial banking walkthrough from unusual payment activity to an accountable decision.",
         head("", '<a href="index.html">Home</a> · Walkthrough',
              "From an unusual payment to a decision you can explain",
              "See how a bank connects customer activity, monitoring alerts and fraud signals, then carries the evidence from investigation into reporting.") + f"""
<section class="sec tight"><div class="wrap">
  <figure class="journey-film" style="max-width:960px;margin:0 auto">
    {video("", "overview-commercial-banks")}
    <figcaption>Commercial banking walkthrough · Illustrative data</figcaption>
  </figure>
</div></section>
<section class="sec tight wash"><div class="wrap">
  <h2>What would this look like in your institution?</h2>
  <a class="btn solid" href="company/contact.html?topic=demo#enquiry">Request a demo</a>
  <a class="btn outline" href="solutions.html">Explore solutions</a>
</div></section>
""", "", closing_form=False)

    page("resources.html", "Evidence and resources", "See INFERIVA in operation and explore how to assess the evidence behind financial crime controls.",
         head("", '<a href="index.html">Home</a> · Evidence and resources', "Evidence and resources", "See INFERIVA in operation and explore how to assess the evidence behind financial crime controls.") + """
<section class="sec resource-section" id="resources"><div class="wrap">
  <div class="section-intro"><h2>See what you can learn about your controls</h2><p><a href="platform/index.html#see-it-working">Watch the INFERIVA platform overview</a></p></div>
  <div class="offer-grid">
    <article><div><h3>Assess your current operation</h3><p>See what a focused diagnostic can tell you about alert outcomes and decision quality using an agreed extract.</p><a href="start/diagnostic.html">Read the diagnostic guide →</a></div></article>
    <article><div><h3>Review a specimen board-pack finding</h3><p>See how a finding sets out the evidence, its limitations and the decision requested of leadership.</p><a href="assurance/deliverables.html#sample-board-pack">View the board-pack specimen →</a></div></article>
  </div>
</div></section>

""", "", closing_form=False)

    # ======================================================================
    # START HERE — the commercial path
    # ======================================================================
    def way(title, suits, does, label, href):
        return (f'<div class="cell"><h3>{title}</h3><p class="cap" style="margin:4px 0 10px">{suits}</p>'
                f'<p>{does}</p><p style="margin-top:14px"><a href="../{href}">{label} &rarr;</a></p></div>')
    page("start/index.html", "Start here",
         "Four ways to start working with INFERIVA: a briefing, a demonstration, a diagnostic or a proof of value.",
         head("../", '<a href="../index.html">Home</a> · Start here',
              "Ways to get started",
              "Four ways to start working with INFERIVA. Choose the one that matches "
              "where your institution is today.") + """
<section class="sec"><div class="wrap">
  <div class="grid2" style="margin-top:0;gap:1px;background:var(--rule);border:1px solid var(--rule)">""" + "".join([
      way("An executive briefing", "For a board, chief executive or MLRO weighing the options",
          "An hour with your leadership on what one platform would change for your institution, and what it would not.",
          "Arrange a briefing", "company/contact.html?topic=briefing"),
      way("A demonstration", "For teams comparing systems",
          "The platform configured for your jurisdictions, products and thresholds, rather than a generic walkthrough.",
          "Request a demonstration", "company/contact.html?topic=demo"),
      way("A diagnostic", "For an institution that wants to know how its current system performs",
          "Send an extract from the system you run today. We tell you what the data covers, then where it is "
          "underperforming. No integration and no charge.",
          "How a diagnostic works", "start/diagnostic.html"),
      way("A proof of value", "For teams that want to test a focused workflow",
          "Agree the operational problem, baseline, measurable success criteria and evidence for a decision about wider deployment.",
          "Discuss proof of value", "company/contact.html?topic=proof#enquiry"),
  ]) + """</div>
</div></section>
""" + nextlinks("../", [
    ("The platform", "platform/index.html", "What each module does."),
    ("Request a free diagnostic", "start/diagnostic.html", "For your kind of institution."),
    ("Talk to us", "company/contact.html", "Ask us anything."),
]), "../")

    page("start/diagnostic.html", "Request a diagnostic",
         "Send an extract from whatever you run today and get a measured account of how it is performing.",
         head("../", '<a href="../index.html">Home</a> · <a href="index.html">Start here</a> · Diagnostic',
              "Find out what your current system is actually doing",
              "Get a measured view of a workflow or control using an agreed extract from your existing systems.") + """
<section class="sec"><div class="wrap">
  <h2 class="head">What happens after you request a diagnostic</h2>
  <div class="steps">
    <div class="stp"><span class="sn">01</span><h3>Agree what to examine</h3><div class="sd">
      <p>Tell us which control or workflow you want to examine. We agree the period, fields and secure transfer arrangements with you before any data is shared.</p></div></div>
    <div class="stp"><span class="sn">02</span><h3>Provide an agreed extract</h3><div class="sd">
      <p>Depending on scope, this could include alerts, rule identifiers, cases, decisions and timestamps from your existing system. The diagnostic uses an extract and requires no production connection.</p></div></div>
    <div class="stp"><span class="sn">03</span><h3>Review the findings</h3><div class="sd">
      <p>Receive a summary of coverage and limitations, findings such as alert escalation and decision documentation, and priorities for follow-up.</p></div></div>
  </div>
  <p><a class="btn solid" href="../company/contact.html?topic=diagnostic#enquiry">Request a diagnostic</a></p>

  <h3 class="sub">Diagnostics by institution</h3>
  <p class="body">What the diagnostic looks for depends on the kind of institution you
  are. Each has a short film of a diagnostic run on the platform, on illustrative data.</p>
  <div class="sectors">""" + SECTORS.replace('href="sectors/', 'href="../sectors/').replace('src="media/', 'src="../media/') + """</div>

  <h3 class="sub">Then, if it is worth repeating</h3>
  <p class="body">A single diagnostic tells you where you stand. <strong>Two tell you
  whether anything you did worked</strong> — and that is the difference between a
  consulting engagement and something that keeps paying.</p>
  <div class="quote"><p>It is also the claim a professional services firm structurally
  cannot match, because they leave. An MLRO defending a tuning decision at examination
  needs evidence the change worked, and evidence is a comparison against a recorded
  baseline rather than an assertion.</p></div>
</div></section>
""" + cta("../", "", "Discuss a diagnostic",
          "Tell us which control you want to examine. We will agree the scope and data transfer arrangements with you.",
          [("Request a diagnostic", "company/contact.html?topic=diagnostic"), ("How you buy", "start/how-you-buy.html")]) + """
""" + nextlinks("../", [
    ("How you buy", "start/how-you-buy.html", "If the diagnostic finds something."),
    ("Independent assurance", "assurance/index.html", "The deeper version, for a board or an examiner."),
    ("Talk to us", "company/contact.html?topic=diagnostic", "Agree the scope and any data needed."),
]), "../")

    page("start/how-you-buy.html", "How you buy",
         "Per module, metered per dimension, with plan changes prorated properly.",
         head("../", '<a href="../index.html">Home</a> · <a href="index.html">Start here</a> · How you buy',
              "Take what you need, pay for what you use",
              "We would rather have a small contract that works than a large one "
              "that stalls in procurement for a year.") + """
<section class="sec"><div class="wrap">
  <h2 class="head">Scope, capacity and deployment</h2>
  <p class="lead">Choose the workflows you need, agree the capacity required, and select a deployment model that fits your operating environment.</p>
  <div class="tbl">
    <div class="trow"><div>Scope</div><div>Due diligence and customer risk, monitoring and investigations, agent and wallet risk, fraud decisioning or an integrated platform.</div></div>
    <div class="trow"><div>Capacity</div><div>Agree the included transactions, screenings, evaluations, users or other units relevant to the offer.</div></div>
    <div class="trow"><div>Deployment</div><div>Shared cloud, dedicated cloud, hybrid or on-premises, with responsibilities for hosting, resilience and support agreed in the quote.</div></div>
  </div>
  <h3 class="sub">Terms for your markets</h3>
  <p class="body">The quote sets out invoicing currency, third-party data and verification costs, and the implementation work for your workflows and jurisdictions. For institutional deployments, compare first-year and ongoing annual costs.</p>
</div></section>
""" + cta("../", "PRICING", "A quote for your institution",
          "Pricing is set per module and by usage. Tell us your volumes and the modules you are considering, and we will send you a quote.",
          [("Get a quote", "company/contact.html?topic=quote"), ("Request a diagnostic first", "start/diagnostic.html")]) + """
""" + nextlinks("../", [
    ("The platform", "platform/index.html", "What each module does."),
    ("Request a free diagnostic", "start/diagnostic.html", "Find the gap before you buy."),
    ("Talk to us", "company/contact.html?topic=quote", "Get a quote against your volumes."),
]), "../")

    # ======================================================================
    # PLATFORM
    # ======================================================================
    page("platform/index.html", "The INFERIVA platform",
         "See how INFERIVA connects customer risk, monitoring, investigations and reporting across the financial-crime operation.",
         head("../", '<a href="../index.html">Home</a> · Platform',
              "One record, from onboarding to filing",
              "Give every team the context to act as risk moves through your institution.") +
         """
<section class="sec journey" id="see-it-working"><div class="wrap">
  <div class="section-intro">
    <h2>Follow one signal from detection to decision</h2>
    <p class="lead">Follow an illustrative business customer from the first signal through investigation and review.</p>
  </div>
  <div class="journey-grid">
    <div class="journey-steps">
      <details open name="customer-journey"><summary>See the whole picture</summary>
        <p>A business customer’s transfers change. The analyst reviews the alerts alongside the customer’s expected activity and screening history on the same record.</p>
        <a href="../platform/aml.html">Explore monitoring</a>
      </details>
      <details name="customer-journey"><summary>Carry the evidence into investigation</summary>
        <p>The analyst escalates the activity. The investigator picks up the case with the linked transactions and the analyst’s rationale already in view.</p>
        <a href="../platform/investigations.html">Explore investigations</a>
      </details>
      <details name="customer-journey"><summary>Explain the decision and review what changed</summary>
        <p>The reviewer uses the case evidence to decide whether reporting is required. Leadership can look back at the decisions and examine whether the rule is producing useful leads.</p>
        <a href="../platform/reporting.html">Explore reporting</a>
      </details>
    </div>
    <figure class="journey-film">
      <video class="platform-overview-player" width="1920" height="1080" controls playsinline preload="none" poster="../media/films/platform-overview-poster.jpg" aria-label="INFERIVA platform overview">
        <source src="../media/films/platform-overview.mp4" type="video/mp4">
        <a href="../media/films/platform-overview.mp4">Open the platform overview video</a>
      </video>
      <figcaption>INFERIVA platform overview</figcaption>
    </figure>
  </div>
</div></section>
<section class="sec outcomes"><div class="wrap">
  <div class="section-intro">
    <h2>Start with the workflow your team needs to improve</h2>
    <p class="lead">Configure the platform around your products, risk appetite, approval paths and jurisdictions. Add workflows as the operation grows.</p>
  </div>
  <div class="institution-grid">
    <a href="customer-risk.html"><h3>Know who you’re doing business with</h3><p>Carry customer and ownership evidence forward into ongoing monitoring.</p><span>Customer risk →</span></a>
    <a href="aml.html"><h3>Prioritise activity worth investigating</h3><p>Give analysts the customer context and alert rationale they need to decide what merits review.</p><span>AML operations →</span></a>
    <a href="fraud.html"><h3>Connect fraud and AML decisions</h3><p>Bring both teams’ signals together when they point to the same customer or activity.</p><span>Fraud operations →</span></a>
    <a href="investigations.html"><h3>Keep investigations moving</h3><p>Pass evidence, decisions and approvals through the case as ownership changes.</p><span>Investigations →</span></a>
    <a href="reporting.html"><h3>Carry the case into reporting</h3><p>Use the case record to support review, approval and filing.</p><span>Regulatory reporting →</span></a>
    <a href="agent-supervision.html"><h3>See risk across your agent network</h3><p>Connect agent behaviour with the customer activity and transactions behind it.</p><span>Payments and agents →</span></a>
  </div>
</div></section>
""", "../")

    page("platform/customer-risk.html", "Customer risk",
         "Identity, documents, liveness and ownership resolved to a risk tier on evidence the analyst can see later.",
         head("../", '<a href="../index.html">Home</a> · <a href="index.html">Platform</a> · Customer risk',
              "The decision you make on day one still matters on day four hundred",
              "Most onboarding produces a yes or a no and throws away the reasoning. "
              "That reasoning is exactly what an examiner asks for later.") + """
<section class="sec"><div class="wrap">
  <h2 class="head">What happens during the check</h2>
  <div class="steps">
    <div class="stp"><span class="sn">01</span><h3>Identity</h3><div class="sd">
      <p>Documents, biometrics and liveness, resolved against government sources where
      they are available in that market.</p></div></div>
    <div class="stp"><span class="sn">02</span><h3>The business behind it</h3><div class="sd">
      <p>For a company, resolve it against the registry and unwrap ownership past the
      holding structure to the people actually behind it.</p>
      <p class="aside">Where ownership cannot be resolved, that is recorded as a fact
      about the customer rather than quietly passed.</p></div></div>
    <div class="stp"><span class="sn">03</span><h3>Screening</h3><div class="sd">
      <p>Sanctions, PEP and watchlist checks — with the list version recorded, so a
      decision can be judged against what was actually knowable that day.</p></div></div>
    <div class="stp"><span class="sn">04</span><h3>The risk tier</h3><div class="sd">
      <p>Personal, geographic, product and behavioural factors resolve to a tier that
      drives enhanced due diligence now and monitoring thresholds afterwards.</p>
      <p class="aside">This is the part that usually gets lost. A tier that does not
      reach the monitoring engine is a form somebody filled in.</p></div></div>
  </div>
  <div class="quote"><p>Onboarding evidence is not filed away. It is the first thing
  attached to the case if that customer is ever investigated.</p></div>
</div></section>
<section class="sec tight"><div class="wrap"><h2>Due diligence for development finance</h2><p>Explore borrower, investee and supplier screening and ownership review.</p><a href="../sectors/development-finance.html">Explore development finance due diligence</a></div></section>
""" + nextlinks("../", [
    ("AML", "platform/aml.html", "Where the risk tier ends up."),
    ("Investigations", "platform/investigations.html", "What the analyst sees."),
    ("Assurance", "assurance/index.html", "Testing whether the evidence exists."),
]), "../")

    page("platform/aml.html", "AML",
         "Laundering and fraud on the same flows, with thresholds derived rather than chosen.",
         head("../", '<a href="../index.html">Home</a> · <a href="index.html">Platform</a> · AML',
              "Detection you can justify, not just run",
              "Any engine will fire alerts. The question an examiner asks is why it "
              "fires where it does, and what you did about the ones it raised.") + """
<section class="sec"><div class="wrap">
  <h2 class="head">Where did this number come from?</h2>
  <p class="lead">Somebody picked a round number once and it has not moved since. We
  work it out instead — <strong>never above what the regulator requires you to
  report</strong>, and never above what your analysts can actually get through,
  because a queue nobody clears is not a stricter control. It is a backlog with your
  name on it.</p>
  <div class="quote"><p>Then we sample what falls just underneath, to see what you are
  missing. Until somebody has done that, a threshold is a guess wearing a suit.</p></div>

  <h3 class="sub">Set the method once, not the number</h3>
  <p class="body">Thresholds are expressed as a relationship to the local regulatory
  figure rather than as an amount. Tell the system to alert beneath the cash reporting
  threshold and it resolves what that means in each market you operate in —
  <strong>from the same line of configuration</strong>.</p>

  <h3 class="sub">Laundering and fraud on the same flows</h3>
  <div class="grid2">
    <div class="card"><h3>Money laundering</h3><p class="cap">Patterns over time</p>
      <ul><li>Structuring, layering and rapid movement</li>
      <li>Dormancy and reactivation</li><li>High-risk jurisdiction exposure</li>
      <li>Velocity against the customer's own baseline</li>
      <li>Cash intensity against the declared business</li></ul></div>
    <div class="card"><h3>Fraud</h3><p class="cap">Signals in the moment</p>
      <ul><li>Device and browser fingerprint</li><li>Remote access tools and emulators</li>
      <li>Behavioural anomaly inside the session</li><li>Network and shared-attribute links</li>
      <li>Holds and interdiction before settlement</li></ul></div>
  </div>

  <h3 class="sub">And why you closed it</h3>
  <p class="body">Rule versions, threshold sets and configuration are retained. Two
  years on, when the analyst has left and the rules have changed four times, you can
  still show what the system was set to that week, what it flagged, and who signed it
  off. <strong>This is the question institutions fail most often in our
  assessments.</strong></p>
</div></section>
""" + cta("../", "IF THIS IS THE GAP", "What are your thresholds set to, and when were they last looked at?",
          "Most institutions can answer the first. A diagnostic answers the second, using an extract rather than an integration.",
          [("Request a diagnostic", "start/diagnostic.html"), ("How you buy", "start/how-you-buy.html")]) + """
""" + nextlinks("../", [
    ("PSP and agent supervision", "platform/agent-supervision.html", "Scenarios built for these markets."),
    ("Investigations", "platform/investigations.html", "What happens after an alert."),
    ("Investigations", "platform/investigations.html", "Where an alert goes next."),
]), "../")

    page("platform/investigations.html", "Investigations",
         "Everything the reviewer needs already attached, and a decision trail that survives the analyst leaving.",
         head("../", '<a href="../index.html">Home</a> · <a href="index.html">Platform</a> · Investigations',
              "The case opens with the context already in it",
              "An analyst who has to go and find the onboarding record, the complaint "
              "history and the linked accounts spends their day assembling rather than "
              "deciding.") + """
<section class="sec"><div class="wrap">
  <div class="grid3">
    <div class="cell"><h3>Attached on open</h3><p>Onboarding evidence, screening
      results, prior alerts, complaints and linked entities — already there.</p></div>
    <div class="cell"><h3>The entity graph</h3><p>Shared devices, addresses,
      beneficiaries and counterparties, so a single case shows the network.</p></div>
    <div class="cell"><h3>Maker-checker</h3><p>Enforced per record, so the person who
      raised it is not the person who cleared it.</p></div>
    <div class="cell"><h3>Service levels</h3><p>Ageing and queue position tracked,
      because an alert nobody reached is a finding of its own.</p></div>
    <div class="cell"><h3>Reasoning retained</h3><p>Why, in the analyst's words,
      stored beside the decision rather than in a comment field nobody exports.</p></div>
    <div class="cell"><h3>Straight to filing</h3><p>Where it escalates, the report
      drafts from the case rather than being rekeyed.</p>
      <a href="reporting.html">How filing works</a></div>
  </div>
  <div class="quote"><p>A decision trail is only worth having if somebody who was not
  there can follow it.</p></div>
</div></section>
""" + cta("../", "TAKE THIS ONE MODULE", "Case management can be taken on its own",
          "Keep your existing detection and filing. Modules are entitled and metered separately, so the first contract is the size of the problem rather than the size of the estate.",
          [("How you buy", "start/how-you-buy.html"), ("See the platform", "platform/index.html")]) + """
""" + nextlinks("../", [
    ("Regulatory reporting", "platform/reporting.html", "From case to filed report."),
    ("AML", "platform/aml.html", "Where the alerts come from."),
    ("Assurance", "assurance/index.html", "Testing whether the trail holds up."),
]), "../")

    page("platform/reporting.html", "Regulatory reporting",
         "Reports drafted from the case, formatted per regulator, filed with the acknowledgement retained.",
         head("../", '<a href="../index.html">Home</a> · <a href="index.html">Platform</a> · Reporting',
              "Filed, acknowledged, and still explainable in two years",
              "Filing is where a compliance function is most visible to its regulator, "
              "and where rekeying causes the most damage.") + """
<section class="sec"><div class="wrap">
  <h2 class="head">Drafted from the case, not from scratch</h2>
  <p class="lead">The suspicious transaction report assembles from the case file that
  produced it — the transactions, the entities, the analyst's reasoning and the
  evidence — in the format that regulator expects.</p>

  <div class="tbl">
    <div class="trow"><div>Nigeria</div><div>Filed to the NFIU through goAML
      <span class="ref">CBN AML/CFT/CPF · in production</span></div></div>
    <div class="trow"><div>Ghana</div><div>Financial Intelligence Centre
      <span class="ref">AML Act 1044</span></div></div>
    <div class="trow"><div>Kenya</div><div>Financial Reporting Centre
      <span class="ref">POCAMLA s.44 · s.44(6)</span></div></div>
    <div class="trow"><div>South Africa</div><div>Financial Intelligence Centre
      <span class="ref">FIC Act s.29 · s.28</span></div></div>
    <div class="trow"><div>United Kingdom</div><div>National Crime Agency
      <span class="ref">POCA 2002 · MLR 2017</span></div></div>
  </div>

  <h3 class="sub">The acknowledgement is part of the record</h3>
  <p class="body">A report you cannot prove you filed is a report you did not file, as
  far as an examiner is concerned. <strong>Acknowledgements are stored against the
  case</strong>, with the timestamp, so the question "when did you tell us" has an
  answer that is not somebody's recollection.</p>

  <h3 class="sub">Timeliness is assessed separately</h3>
  <p class="body">Late filing is a breach in itself, distinct from whether the report
  was correct. The platform tracks the gap between the trigger and the filing, because
  that is the number a supervisor will compute if you do not.</p>
</div></section>
""" + nextlinks("../", [
    ("Investigations", "platform/investigations.html", "Where a report starts."),
    ("Investigations", "platform/investigations.html", "Where the report comes from."),
    ("Assurance", "assurance/how-it-works.html", "How filing is tested."),
]), "../")

    page("platform/agent-supervision.html", "PSP and agent supervision",
         "Scenarios built for agent networks and wallets, where laundering and fraud turn out to be the same agent.",
         head("../", '<a href="../index.html">Home</a> · <a href="index.html">Platform</a> · PSP and agent supervision',
              "The agent laundering money on Tuesday takes scam deposits on Thursday",
              "A platform designed for correspondent banking has never seen either, "
              "and cannot treat them as one problem if it sells AML and fraud "
              "separately.") + """
<section class="sec"><div class="wrap">
  <h2 class="head">What a generic engine misses</h2>
  <div class="grid2">
    <div class="card"><h3>Same-agent round trip</h3><p class="cap">SAME_AGENT_ROUND_TRIP</p>
      <ul><li>Funds leave and return through one agent inside a short window</li>
      <li>Each leg beneath the reporting threshold</li>
      <li>Invisible to any rule looking at single transactions</li></ul></div>
    <div class="card"><h3>Cross-agent structuring</h3><p class="cap">CROSS_AGENT_GEO_STRUCTURING</p>
      <ul><li>Structuring spread across agents and locations</li>
      <li>No single agent trips a threshold</li>
      <li>Only visible when the network is treated as one</li></ul></div>
    <div class="card"><h3>Complaint clustering</h3><p class="cap">AGENT_COMPLAINT_SPIKE</p>
      <ul><li>Cash-not-credited complaints concentrating on one agent</li>
      <li>Frequently the first signal an agent has gone bad</li>
      <li>Lives in the complaints system at most institutions, unread</li></ul></div>
    <div class="card"><h3>Wallet behaviour</h3><p class="cap">DORMANT_WALLET_REACTIVATION · NIGHT_TIME_VELOCITY</p>
      <ul><li>Long-dormant wallets moving quickly on reactivation</li>
      <li>Activity outside the customer's established pattern</li>
      <li>Velocity before a behavioural baseline exists</li></ul></div>
  </div>

  <h3 class="sub">Thresholds that fit the network</h3>
  <p class="body">Agent volumes differ by an order of magnitude between a city network
  and a rural cooperative. <strong>A micro-structuring rule tuned for one alerts on
  every ordinary customer of the other</strong>, so thresholds are configured per
  tenant rather than shipped as constants.</p>

  <div class="quote"><p>An agent suspended for laundering and an agent held for scam
  exposure are the same agent.</p></div>
</div></section>
""" + nextlinks("../", [
    ("Agent networks and mobile wallets", "sectors/agent-networks.html", "Who this was built for."),
    ("AML", "platform/aml.html", "How the thresholds are set."),
    ("Request a demo", "company/contact.html?topic=demo", "See it with your own network."),
]), "../")


    page("platform/fraud.html", "Fraud",
         "Interdiction before the money leaves, on the same record as the AML estate.",
         head("../", '<a href="../index.html">Home</a> · <a href="index.html">Platform</a> · Fraud',
              "Stop it before the money goes",
              "Money laundering is a pattern you find afterwards. Fraud is a decision "
              "you have seconds to make, and the two share a customer.") + """
<section class="sec"><div class="wrap">
  <h2 class="head">Signals in the moment, not patterns over weeks</h2>
  <div class="grid2" style="margin-top:0">
    <div class="card"><h3>What the session tells you</h3><p class="cap">Before the transfer</p>
      <ul><li>Device and browser fingerprint</li>
      <li>Remote access tools and emulators</li>
      <li>Behaviour that does not match the account holder</li>
      <li>Velocity against this customer's own baseline</li></ul></div>
    <div class="card"><h3>What you can do about it</h3><p class="cap">While it still matters</p>
      <ul><li>Hold the payment before it settles</li>
      <li>Block an agent or a device automatically</li>
      <li>Reach the customer before they send it</li>
      <li>Open a case with the session evidence attached</li></ul></div>
  </div>

  <h3 class="sub">Scam intervention</h3>
  <p class="body">A customer being socially engineered is not committing fraud, they are
  losing money to it. <strong>Reaching them before the transfer completes is a
  different capability from scoring the transaction</strong>, and most AML platforms
  do not have it because it was never their problem.</p>

  <h3 class="sub">Including your own people</h3>
  <p class="body">Insider events and network links are tracked on the same graph as
  customer relationships. An employee sharing attributes with a customer account is a
  pattern worth surfacing, and it does not appear in either system alone.</p>

  <h3 class="sub">And scoring you can explain</h3>
  <p class="body">Model scores are versioned. When somebody asks why a payment was
  held in March, the answer is which model, at what version, scoring what — not a
  number with no provenance.</p>

  <div class="quote"><p>The agent laundering money on Tuesday is the agent taking scam
  deposits on Thursday. Two vendors cannot see that.</p></div>
</div></section>
""" + nextlinks("../", [
    ("AML", "platform/aml.html", "The other half of the same estate."),
    ("PSP and agent supervision", "platform/agent-supervision.html", "Where the two meet."),
    ("Investigations", "platform/investigations.html", "What happens after either fires."),
]), "../")

    # ======================================================================
    # ASSURANCE
    # ======================================================================
    page("assurance/index.html", "Independent assurance",
         "A separate system that tests whether your controls can actually be evidenced.",
         head("../", '<a href="../index.html">Home</a> · Assurance',
              "Find out what you can evidence before a supervisor asks",
              "An independent assessment that asks your team the questions a supervisor "
              "would, and records what actually comes back.") + """
<section class="sec"><div class="wrap">
  <p class="lead">The assessment is a separate system, with no shared identifiers
  with the platform. <strong>It runs against institutions on any platform,
  including ours</strong> — we pointed it at our own first, and it found something.</p>

  <h3 class="sub">Two halves, and the second tests the first</h3>
  <div class="grid2">
    <div class="card"><h3>The control assessment</h3><p class="cap">What you have</p>
      <ul><li>Every control scored on whether evidence exists</li>
      <li>Whether it is adequate, current and governed</li>
      <li>And whether it is proportionate to your size</li>
      <li>Cited to the instruments that bind you locally</li></ul></div>
    <div class="card"><h3>The evidence exercise</h3><p class="cap">What you can produce</p>
      <ul><li>Supervisory information requests, issued in writing</li>
      <li>Answered by your team, unaided</li>
      <li>Recorded by source — system of record, spreadsheet, or recollection</li>
      <li>And by what it cost in hours</li></ul></div>
  </div>

  <div class="quote"><p>Where a control is assessed as in place and the request testing
  it cannot be answered, the report says so — and names the obligations you cannot
  currently evidence.</p></div>

  <p class="body">That finding is what no questionnaire reaches. A supervisor treats a
  control that cannot be evidenced as a control that is not there, and most
  institutions do not discover which of theirs fall into that category until somebody
  external asks.</p>

</div></section>
""" + cta("../", "BEFORE YOU COMMIT TO AN ENGAGEMENT", "Start with a diagnostic instead",
          "A diagnostic costs an extract, and it usually tells you whether the deeper exercise is worth it.",
          [("Request a diagnostic", "start/diagnostic.html"), ("What an assessment involves", "assurance/how-it-works.html")]) + """
""" + nextlinks("../", [
    ("How an assessment runs", "assurance/how-it-works.html", "What actually happens, week by week."),
    ("What you receive", "assurance/deliverables.html#sample-board-pack", "The documents and who they are for."),
    ("The platform", "platform/index.html", "What the assessment is separate from."),
]), "../")

    page("assurance/how-it-works.html", "How an assessment runs",
         "What actually happens during a control assurance engagement, and what it asks of your team.",
         head("../", '<a href="../index.html">Home</a> · <a href="index.html">Assurance</a> · How it runs',
              "What actually happens",
              "") + """
<section class="sec"><div class="wrap">
  <div class="steps">
    <div class="stp"><span class="sn">01</span><h3>Scope and period</h3><div class="sd">
      <p>We agree which legal entity is being assessed, in which jurisdiction, and over
      what period. The period is then locked.</p>
      <p class="aside">Without a recorded period, no reader can tell which obligations
      applied or whether the evidence was current.</p></div></div>
    <div class="stp"><span class="sn">02</span><h3>The evidence request</h3><div class="sd">
      <p>You receive the full list of what will be asked for, ahead of the session. No
      surprises — the exercise is not a trap, it is a rehearsal.</p></div></div>
    <div class="stp"><span class="sn">03</span><h3>The control assessment</h3><div class="sd">
      <p>Working through each control with the people who operate it, recording what
      exists, how mature it is, and whether the evidence was actually produced.</p>
      <p class="aside">Assessed against what an institution your size is expected to
      hold, not against a tier one bank's budget.</p></div></div>
    <div class="stp"><span class="sn">04</span><h3>The evidence exercise</h3><div class="sd">
      <p>Supervisory information requests issued in writing and answered by your team
      without our help. We record what came back, from where, and how long it took.</p>
      <p class="aside">This is the part that costs real time. It is also the only part
      that tells you what an examination would actually find.</p></div></div>
    <div class="stp"><span class="sn">05</span><h3>Findings and report</h3><div class="sd">
      <p>Controls rated well whose evidence could not be produced are named, with the
      obligations they put at risk. Strengths are recorded too.</p></div></div>
    <div class="stp"><span class="sn">06</span><h3>Re-measurement</h3><div class="sd">
      <p>The assessment becomes a baseline. Next year measures against it, so progress
      is a number rather than an assertion.</p></div></div>
  </div>

</div></section>
""" + nextlinks("../", [
    ("What you receive", "assurance/deliverables.html#sample-board-pack", "The documents and their audiences."),
    ("Request a diagnostic first", "start/diagnostic.html", "Free, on an extract."),
    ("Talk to us", "company/contact.html?topic=assessment", "Discuss scope for your institution."),
]), "../")

    page("assurance/deliverables.html", "What you receive",
         "The documents produced by an assessment, and who each is written for.",
         head("../", '<a href="../index.html">Home</a> · <a href="index.html">Assurance</a> · What you receive',
              "Four documents, four audiences",
              "A single report written for everybody gets read properly by nobody.") + """
<section class="sec"><div class="wrap">
  <div class="grid2">
    <div class="card"><h3>Board pack</h3><p class="cap">For the audit committee</p>
      <ul><li>Opens with the decisions required, not the findings</li>
      <li>What you are being asked to accept, and what it would cost to close</li>
      <li>Owner and date columns left blank, deliberately</li>
      <li>Short enough to be read before the meeting</li></ul></div>
    <div class="card"><h3>Assurance report</h3><p class="cap">For the MLRO and internal audit</p>
      <ul><li>Every control, every dimension, with the evidence recorded</li>
      <li>Controls assessed as in place that could not be evidenced</li>
      <li>Obligations cited to the instruments in force locally</li>
      <li>Scope and limitations stated on the face of it</li></ul></div>
    <div class="card"><h3>Progress report</h3><p class="cap">For whoever owns remediation</p>
      <ul><li>Movement against the recorded baseline</li>
      <li>What improved, and what regressed</li>
      <li>Whether the trajectory reaches the target</li>
      <li>Blunt about it when it does not</li></ul></div>
    <div class="card"><h3>Submission pack</h3><p class="cap">Where a regulator expects one</p>
      <ul><li>In the structure that regulator asks for</li>
      <li>Assembled from the same assessed record</li>
      <li>Currently Nigeria; other markets receive the neutral report</li></ul></div>
  </div>

  <div class="specimen-section" id="sample-board-pack">""" + specimen + """</div>

  <h3 class="sub">A note on the group case</h3>
  <p class="body">Where an institution holds several regulated entities, the assessment
  produces a group view and an entity comparison — and <strong>deliberately does not
  produce a group score</strong>. A figure assembled from entities that define a
  measure differently is arithmetically valid and analytically meaningless.</p>
  <div class="quote"><p>Better to report per entity with no total than a total nobody
  can defend.</p></div>
</div></section>
""" + nextlinks("../", [
    ("How an assessment runs", "assurance/how-it-works.html", "The engagement, step by step."),
    ("Request a diagnostic first", "start/diagnostic.html", "Free, for your kind of institution."),
    ("Talk to us", "company/contact.html?topic=assessment", "Scope an assessment."),
]), "../")

    # ======================================================================
    # SECTORS
    # ======================================================================
    sectors = [
        ("agent-networks", "Agent networks and mobile wallets",
         "Where the platform was built first.",
         "This is what we built for first",
         "Agent networks and mobile wallets carry the volume in many markets, and the "
         "typologies that come with them are not in a system designed for correspondent banking.",
         [("Agent-specific detection", "Round trips, cross-agent structuring, complaint clustering and suspension — treated as one problem across laundering and fraud."),
          ("Thresholds that fit your network", "A city network and a rural cooperative differ by an order of magnitude. Configured per tenant, not shipped as a constant."),
          ("Intervention options", "Where INFERIVA is integrated into the live decision path, agree when the payment system should refer or hold an instruction.")]),
        ("microfinance", "Microfinance banks and small OFIs",
         "Held to your own standard, not to one written for a bank fifty times your size.",
         "A careful manual process is the right answer here",
         "Most compliance assessments apply one absolute standard and hand a small "
         "institution a list of things it was never meant to buy.",
         [("Proportionate assessment", "Controls judged against what an institution your size is expected to hold. A documented, consistently applied arrangement is a pass, not a finding."),
          ("No crisis manufactured", "A well-run small institution should be told it is well run."),
          ("Room to grow into", "The same platform serves larger institutions, so growing does not mean replacing."),
          ("Honest about cost", "We will tell you if an assessment is more than you need right now.")]),
        ("commercial-banks", "Commercial banks",
         "The full estate, with the evidence discipline an examiner expects.",
         "Bring financial-crime decisions and evidence together across the bank",
         "Tier 2 and tier 3 institutions get the same platform as everybody else — "
         "configured around the bank’s products, data, approval paths and jurisdictions.",
         [("Converged AML and fraud", "One estate rather than two products and two reporting lines that hear about each other late."),
          ("Decision reconstruction", "Two years on, show what the rules were set to that week and who approved the close."),
          ("Multi-market", "Several regulators, one platform, one picture for the board."),
          ("Straight about scale", "Tell us your volumes and we will tell you honestly whether we are ready for them.")]),
        ("development-finance", "Due diligence for development finance",
         "Borrower, investee and counterparty due diligence for development finance.",
         "Establish who is behind a borrower, investee or supplier",
         "Start with entity verification, ownership and screening. Project-linked disbursement controls need facility, milestone and approval evidence from your portfolio systems.",
         [("Entity due diligence", "Review borrower, investee and supplier records with their ownership evidence."),
          ("Screening and review", "Record screening outcomes and unresolved parties for investigation."),
          ("Project-linked controls", "Scope facility and milestone data, release rules and any pre-payment integration separately.")]),
    ]
    for slug, title, desc, h1, lede, points in sectors:
        cells = "".join(f'<article><h3>{t}</h3><p>{d}</p></article>' for t, d in points)
        film_slug = "microfinance-banks" if slug == "microfinance" else slug
        page(f"sectors/{slug}.html", title, desc,
             head("../", f'<a href="../index.html">Home</a> · <a href="../institutions.html">Institutions</a> · {title}',
                  title, h1) + f"""
<section class="sec"><div class="wrap">
  <div class="journey-grid">
    <div>
      <h2>See INFERIVA in your operation</h2>
      <p class="lead">{sector_outcomes[slug]}</p>
      <div class="btns">
        <a class="btn solid" href="../company/contact.html?topic=demo#enquiry">Request a demo</a>
        <a class="btn outline" href="../start/diagnostic.html">Explore a diagnostic</a>
      </div>
    </div>
    <figure class="journey-film">
      {video("../", "overview-" + film_slug)}
      <figcaption>Platform walkthrough · Illustrative data</figcaption>
    </figure>
  </div>
</div></section>
<section class="sec outcomes"><div class="wrap">
  <h2>Where teams can start</h2>
  <div class="grid2 outcome-grid">{cells}</div>
</div></section>
<section class="sec"><div class="wrap">{film_block(slug)}</div></section>
""", "../")

    page("sectors/digital-lenders.html", "Digital lenders",
         "Customer due diligence and application fraud decisioning for digital lenders.",
         head("../", '<a href="../index.html">Home</a> · <a href="../institutions.html">Institutions</a> · Digital lenders',
              "Review application risk before funds are released",
              "Give onboarding and fraud teams a shared view of the applicant, verification evidence and reasons for referral.") + """
<section class="sec outcomes"><div class="wrap">
  <h2>How a referral works</h2>
  <p class="lead">In an illustrative application, identity information is inconsistent and the device has been associated with other applications. The reviewer sees the underlying signals, the diligence results and the reason the application was referred.</p>
  <div class="grid2 outcome-grid">
    <article><h3>Due diligence</h3><p>Record identity and screening evidence. For business borrowers, link the entity and its beneficial owners.</p><a href="../platform/customer-risk.html">Explore customer risk</a></article>
    <article><h3>Fraud decisioning</h3><p>Agree which application signals are available and where a referral fits in the lender’s approval flow.</p><a href="../platform/fraud.html">Explore fraud decisioning</a></article>
  </div>
</div></section>
""", "../", cta_headline="Discuss a proof of value",
         cta_lede="Bring one application workflow and agree the data, decision criteria and evidence your team needs.")

    PARTNER_TYPES = [
        ("implementation", "Implementation partner", "Systems integrators and consultancies",
         "Your firm, the institutions you serve, and the deployments you have delivered", ""),
        ("reseller", "Reseller", "Sell INFERIVA in your markets",
         "The markets you cover and the institutions you sell to", ""),
        ("technology", "Technology partner", "Integrate with the platform",
         "Your product, and where it would connect: core banking, identity, payments, data", ""),
        ("referral", "Referral partner", "Introduce institutions to us",
         "Who you would introduce, and how you know them", ""),
    ]
    page("company/partners.html", "Partners",
         "Partner with INFERIVA as an implementation partner, reseller, technology partner or referral partner.",
         head("../", '<a href="../index.html">Home</a> · Company · Partners',
              "Partner with INFERIVA",
              "Help regulated institutions run financial crime controls they can evidence, "
              "and build a practice around a platform designed to be deployed by partners.") + """
<section class="sec"><div class="wrap">
  <h2 class="head" style="margin-top:0">Ways to partner</h2>
  <p class="lead">Each partnership is built around what your firm already does well.
  Choose the one that fits, or tell us about a combination.</p>
  <div class="grid2" style="margin-top:22px;gap:1px;background:var(--rule);border:1px solid var(--rule)">
    <div class="cell"><h3>Implementation partner</h3><p>Deploy the platform for
      institutions in your markets. Your consultants are trained and certified in our
      implementation method, from contract signature through to business as usual.</p></div>
    <div class="cell"><h3>Reseller</h3><p>Offer INFERIVA to the institutions you already
      serve, with our support on demonstrations, proposals and technical questions.</p></div>
    <div class="cell"><h3>Technology partner</h3><p>Connect your product to the platform:
      core banking, identity verification, payments or data. Joint customers get one
      joined-up flow rather than two systems to reconcile.</p></div>
    <div class="cell"><h3>Referral partner</h3><p>Introduce institutions that need to
      strengthen their financial crime controls, and be rewarded when an introduction
      becomes a customer.</p></div>
  </div>

  <h3 class="sub">What partners get</h3>
  <div class="grid3" style="margin-top:18px">
    <div class="cell"><h3>Training and certification</h3><p>Structured training for
      sales and technical staff, with certification for the consultants who deploy
      the platform.</p></div>
    <div class="cell"><h3>A demonstration environment</h3><p>The platform with
      illustrative data, so you can show it working before a client has shared
      anything.</p></div>
    <div class="cell"><h3>Selling together</h3><p>Our support on qualifying, presenting
      and closing, and a clear understanding of who owns which opportunity.</p></div>
  </div>

  <h3 class="sub">How it works</h3>
  <div class="steps">
    <div class="stp"><span class="sn">01</span><h3>Apply</h3><div class="sd"><p>Tell us
      about your firm and the partnership you have in mind.</p></div></div>
    <div class="stp"><span class="sn">02</span><h3>Talk it through</h3><div class="sd"><p>We
      agree the markets, the institutions and the terms that fit.</p></div></div>
    <div class="stp"><span class="sn">03</span><h3>Get enabled</h3><div class="sd"><p>Training,
      certification and access to the demonstration environment, then your first
      opportunity together.</p></div></div>
  </div>
</div></section>
<section class="cta" id="contact">
  <div class="wrap cta-grid">
    <div>
      <h2>Ready to become a partner?</h2>
      <p>Tell us about your firm and the partnership you have in mind. One of us reads
      it and replies within two working days.</p>
    </div>
    """ + form_html("../", PARTNER_TYPES, "What kind of partnership?", "implementation", "Firm").replace(
        "The countries you are licensed in", "The countries you work in") + """
  </div>
</section>
""", "../", closing_form=False)

    routes = "".join(f'<li><b>{t}</b><span>{what}</span></li>' for k, t, sub, hint, what in TOPICS)
    page("company/contact.html", "Contact",
         "Ask for a briefing, a demonstration, a diagnostic on your own data, a quote or an independent assessment.",
         head("../", '<a href="../index.html">Home</a> · Company · Contact',
              "Talk to us",
              "Tell us what you need. One of us reads it, and we reply inside two working "
              "days with a time, or a straight answer about whether we are the right fit.") + f"""
<section class="sec tight"><div class="wrap">
  <div class="contact-grid">
    <div>
      <h2 class="head" style="font-size:24px;margin-top:0">What each request involves</h2>
      <ul class="routes">{routes}</ul>
      <h3 class="sub">What happens next</h3>
      <p class="body">We read it, reply with a time, and come to the call having looked
      at what you told us: your markets, your rules or the control you want to examine. If we are
      not the right fit for your volumes or your risk profile, we will say so on that
      first call rather than three months into a procurement.</p>
      <h3 class="sub">Or email us</h3>
      <p class="body"><a href="mailto:enquiries@inferivastructural.com">enquiries@inferivastructural.com</a></p>
    </div>
    {form_html("../")}
  </div>
</div></section>
""", "../", closing_form=False)
