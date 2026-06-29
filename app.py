"""
==========================================================
            PharmaWatch AI
Global Pharmaceutical Supply Chain Intelligence
==========================================================

Author : Code Force Team
Frontend : Streamlit
Backend : Multi-Agent AI (Groq + Tavily + NewsAPI + GDELT)

"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# ==========================================================
# BACKEND IMPORTS
# ==========================================================

from services.news_service import NewsService
from services.gdelt_service import GDELTService

from agents.event_agent import EventAgent
from agents.research_agent import ResearchAgent
from agents.risk_agent import RiskAgent
from agents.alternatives_agent import AlternativesAgent


# ==========================================================
# PAGE CONFIG
# ==========================================================

LOADING_MESSAGES = [

    "🌍 Searching live global news...",

    "📦 Looking for supply-chain disruptions...",

    "🏭 Checking manufacturing facilities...",

    "🚢 Mapping shipping routes...",

    "🧠 Researching pharmaceutical evidence...",

    "💊 Identifying affected medicines...",

    "⚠️ Calculating shortage risk...",

    "🏥 Building hospital recommendations...",

    "✨ Almost there...",

]

st.set_page_config(
    page_title="PharmaWatch AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# CUSTOM THEME
# ==========================================================

st.markdown("""
<style>

/* ---- layout ---- */
.block-container {
    padding-top: 3rem;
    padding-bottom: 2rem;
}

/* ---- sidebar ---- */
section[data-testid="stSidebar"] {
    background: #0d1117;
}
section[data-testid="stSidebar"] * {
    color: #e6edf3 !important;
}

/* ---- cards ---- */
.pw-card {
    border-radius: 14px;
    padding: 20px 22px;
    border: 1px solid #21262d;
    background: #161b22;
    margin-bottom: 14px;
}
.pw-card h4 {
    margin: 0 0 8px 0;
    font-size: 14px;
    letter-spacing: .05em;
    text-transform: uppercase;
    color: #8b949e;
}
.pw-card p {
    margin: 0;
    font-size: 22px;
    font-weight: 700;
    color: #e6edf3;
}

/* ---- risk badge ---- */
.badge-low    { background:#1a3a2a; color:#3fb950; border-radius:8px; padding:4px 12px; font-weight:700; }
.badge-medium { background:#3a2e10; color:#d29922; border-radius:8px; padding:4px 12px; font-weight:700; }
.badge-high   { background:#3a1a1a; color:#f85149; border-radius:8px; padding:4px 12px; font-weight:700; }
.badge-critical { background:#5a0e1a; color:#ff7b72; border-radius:8px; padding:4px 12px; font-weight:700; }

/* ---- section headers ---- */
.section-label {
    font-size: 11px;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #8b949e;
    margin-bottom: 6px;
}

/* ---- pipeline step ---- */
.pipeline-step {
    display:flex; align-items:center; gap:10px;
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid #21262d;
    background: #161b22;
    margin-bottom: 8px;
}
.pipeline-dot {
    width:10px; height:10px; border-radius:50%;
    background:#3fb950; flex-shrink:0;
}
.pipeline-dot.pending { background:#8b949e; }

/* ---- big title ---- */
.big-title {
    font-size: 32px;
    font-weight: 800;
    color: #e6edf3;
    letter-spacing: -1px;
    white-space: normal;
    word-break: break-word;
}
.sub-title {
    font-size: 16px;
    color: #8b949e;
    margin-top: 4px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# SESSION STATE INIT
# ==========================================================

if "pipeline_run" not in st.session_state:
    st.session_state.pipeline_run = False
if "articles" not in st.session_state:
    st.session_state.articles = []
if "events" not in st.session_state:
    st.session_state.events = []
if "research_reports" not in st.session_state:
    st.session_state.research_reports = []
if "risk_reports" not in st.session_state:
    st.session_state.risk_reports = []
if "alternatives_reports" not in st.session_state:
    st.session_state.alternatives_reports = []
if "run_timestamp" not in st.session_state:
    st.session_state.run_timestamp = None


# ==========================================================
# HELPERS
# ==========================================================

def run_pipeline(progress_bar, status_box, timer_box):

    start_time = time.time()

    def update(progress, message):
        elapsed = int(time.time() - start_time)

        mins = elapsed // 60
        secs = elapsed % 60

        progress_bar.progress(progress)

        status_box.info(message)

        timer_box.caption(
            f"⏱ Elapsed Time : {mins:02d}:{secs:02d}"
        )

    # =====================================================
    # Fetch News
    # =====================================================

    update(
        5,
        "🌍 Connecting to NewsAPI & GDELT..."
    )

    news_service = NewsService()
    gdelt_service = GDELTService()

    news_articles = news_service.fetch_latest_news()
    gdelt_articles = gdelt_service.fetch_latest_events()

    articles = news_articles + gdelt_articles

    update(
        15,
        f"📰 Collected {len(articles)} live news articles."
    )

    # =====================================================
    # Event Detection
    # =====================================================

    update(
        20,
        "🔎 Detecting global supply-chain disruptions..."
    )

    event_agent = EventAgent()

    events = event_agent.process_articles(
        articles
    )

    update(
        35,
        f"✅ Identified {len(events)} relevant global events."
    )

    # =====================================================
    # Research Agent
    # =====================================================

    research_messages = [

        "🧠 Researching pharmaceutical evidence...",

        "🌍 Searching trusted web sources...",

        "🏭 Mapping manufacturers and API suppliers...",

        "🚢 Checking logistics, ports and shipping routes...",

        "📦 Correlating geopolitical events with pharma supply chains...",

        "🔬 Verifying evidence before generating reports...",

    ]

    research_progress = [40, 45, 50, 55, 60, 65]

    for progress, message in zip(
        research_progress,
        research_messages,
    ):

        update(progress, message)

        time.sleep(0.2)

    research_agent = ResearchAgent()

    research_reports = research_agent.process_events(
        events
    )

    update(
        72,
        f"✅ Generated {len(research_reports)} research reports."
    )

    # =====================================================
    # Risk Assessment
    # =====================================================

    risk_messages = [

        "⚠️ Assessing medicine shortage risks...",

        "📈 Estimating disruption severity...",

        "💊 Identifying affected medicines...",

        "🏥 Evaluating hospital impact...",

        "📊 Computing confidence scores...",

        "✨ Almost there..."

    ]

    risk_progress = [75, 80, 84, 88, 92, 96]

    for progress, message in zip(
        risk_progress,
        risk_messages,
    ):

        update(progress, message)

        time.sleep(0.2)

    risk_agent = RiskAgent()

    risk_reports = risk_agent.process_reports(
        research_reports
    )

    # =====================================================
    # Complete
    # =====================================================

    update(
        100,
        "🎉 Analysis completed successfully!"
    )

    return (
        articles,
        events,
        research_reports,
        risk_reports,
    )


def risk_color(level: str) -> str:
    level = level.upper() if level else "UNKNOWN"
    return {"LOW": "green", "MEDIUM": "orange", "HIGH": "red"}.get(level, "darkred")


def risk_badge(level: str) -> str:
    level = (level or "UNKNOWN").upper()
    cls = {"LOW": "badge-low", "MEDIUM": "badge-medium", "HIGH": "badge-high"}.get(
        level, "badge-critical"
    )
    return f'<span class="{cls}">{level}</span>'


def gauge_chart(score: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "", "font": {"size": 34, "color": "#e6edf3"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#8b949e"},
            "bar": {"color": "#f85149"},
            "bgcolor": "#161b22",
            "bordercolor": "#21262d",
            "steps": [
                {"range": [0, 30],  "color": "#1a3a2a"},
                {"range": [30, 60], "color": "#3a2e10"},
                {"range": [60, 100],"color": "#3a1a1a"},
            ],
        },
    ))
    fig.update_layout(
        height=240,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e6edf3",
    )
    return fig


def safe_list(val) -> list:
    """Ensure val is always a list."""
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return [str(val)]


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    st.markdown("### 💊 PharmaWatch AI")
    st.caption("Supply Chain Intelligence")
    st.divider()

    page = st.radio(
        "Navigate",
        [
            "🏠 Dashboard",
            "📰 News Intelligence",
            "🌍 Event Intelligence",
            "🔬 Research Analysis",
            "⚠️ Risk Assessment",
            "🏥 Hospital Simulation",
            "💊 Drug Alternatives",
            "📈 Analytics",
            "ℹ️ About",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("**AI Pipeline Status**")

    steps = [
        ("News API", True),
        ("GDELT", True),
        ("Event Agent", True),
        ("Research Agent", True),
        ("Risk Agent", True),
    ]
    for label, active in steps:
        dot_cls = "pipeline-dot" if active else "pipeline-dot pending"
        st.markdown(
            f'<div class="pipeline-step">'
            f'<div class="{dot_cls}"></div>'
            f'<span style="font-size:13px">{label}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.divider()
    if st.session_state.run_timestamp:
        st.caption(f"Last run: {st.session_state.run_timestamp}")
    st.caption("Confluence Hackathon · Prototype")


# ==========================================================
# TITLE BAR
# ==========================================================

st.markdown('<div class="big-title">💊 PharmaWatch AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Global Pharmaceutical Supply Chain Intelligence Platform</div>',
    unsafe_allow_html=True,
)
st.divider()


# ===========================================================
# PAGE: DASHBOARD
# ===========================================================

if page == "🏠 Dashboard":

    col_btn, col_info = st.columns([2, 5])
    with col_btn:
        run_btn = st.button("🔍 Run Pipeline", use_container_width=True, type="primary")
    with col_info:
        if st.session_state.pipeline_run:
            st.success(
                f"✅ Pipeline complete — "
                f"{len(st.session_state.risk_reports)} risk reports generated."
            )
        else:
            st.info("Click **Run Pipeline** to fetch live news and run all AI agents.")

    if run_btn:
        progress_bar = st.progress(0)
        status_box = st.empty()
        timer_box = st.empty()
        checklist = st.empty()
        (
            st.session_state.articles,
            st.session_state.events,
            st.session_state.research_reports,
            st.session_state.risk_reports,
        ) = run_pipeline(
            progress_bar,
            status_box,
            timer_box,
        )
        checklist.success("✅ News Collection Complete")
        checklist.success("✅ Event Intelligence Complete")
        checklist.success("✅ Research Analysis Complete")
        checklist.success("✅ Risk Assessment Complete")
        st.session_state.pipeline_run = True
        st.session_state.run_timestamp = datetime.now().strftime(
            "%d %b %Y %H:%M")
        time.sleep(1)
        st.rerun()

    if st.session_state.pipeline_run and st.session_state.risk_reports:

        reports = st.session_state.risk_reports

        # ---- KPI row ----
        total      = len(reports)
        high_count = sum(1 for r in reports if getattr(r, "overall_risk", "").upper() == "HIGH")
        avg_score  = sum(getattr(r, "risk_score", 0) for r in reports) / total if total else 0
        avg_conf   = sum(getattr(r, "confidence", 0) for r in reports) / total if total else 0

        k1, k2, k3, k4 = st.columns(4)
        for col, label, val in [
            (k1, "Events Analysed",   str(total)),
            (k2, "High Risk Events",  str(high_count)),
            (k3, "Avg Risk Score",    f"{avg_score:.0f} / 100"),
            (k4, "Avg Confidence",    f"{avg_conf * 100:.0f}%"),
        ]:
            col.markdown(
                f'<div class="pw-card"><h4>{label}</h4><p>{val}</p></div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # ---- Top risk report ----
        top = max(reports, key=lambda r: getattr(r, "risk_score", 0))

        left, right = st.columns([3, 2])

        with left:
            st.markdown("#### 🔴 Highest Risk Event")
            st.markdown(
                f'<div class="pw-card">'
                f'<h4>Headline</h4>'
                f'<p style="font-size:17px">{getattr(top, "headline", "—")}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

            st.markdown("**Risk Level** &nbsp;" + risk_badge(getattr(top, "overall_risk", "")), unsafe_allow_html=True)
            st.markdown(f"**Reason:** {getattr(top, 'reasoning', '—')}")

            actions = safe_list(getattr(top, "recommended_actions", getattr(top, "actions", [])))
            if actions:
                st.markdown("**✅ Recommended Actions**")
                for a in actions:
                    st.success(a)

        with right:
            st.markdown("#### Risk Score Gauge")
            st.plotly_chart(gauge_chart(getattr(top, "risk_score", 0)), use_container_width=True)

            st.markdown("**Affected Medicines**")
            meds = safe_list(getattr(top, "affected_medicines", getattr(top, "medicines", [])))
            for m in meds:
                st.markdown(f"- {m}")

            st.markdown("**Affected Regions**")
            regions = safe_list(getattr(top, "affected_regions", getattr(top, "regions", [])))
            for r in regions:
                st.markdown(f"- {r}")

    elif st.session_state.pipeline_run:
        st.warning("Pipeline ran but returned no risk reports. Check your API keys in config.py.")


# ===========================================================
# PAGE: NEWS INTELLIGENCE
# ===========================================================

elif page == "📰 News Intelligence":
    st.subheader("📰 News Intelligence")

    if not st.session_state.pipeline_run:
        st.info("Run the pipeline from the Dashboard first.")
    else:
        articles = st.session_state.articles
        st.markdown(f"**{len(articles)} articles fetched** (NewsAPI + GDELT)")
        st.divider()

        for i, article in enumerate(articles[:30]):
            title   = getattr(article, "title", str(article)) if not isinstance(article, dict) else article.get("title", "—")
            source  = getattr(article, "source", "") if not isinstance(article, dict) else article.get("source", "")
            url     = getattr(article, "url", "") if not isinstance(article, dict) else article.get("url", "")
            pub_at  = getattr(article, "published_at", "") if not isinstance(article, dict) else article.get("publishedAt", "")

            with st.expander(f"{i+1}. {title[:100]}"):
                st.markdown(f"**Source:** {source}")
                if pub_at:
                    st.markdown(f"**Published:** {pub_at}")
                if url:
                    st.markdown(f"[Read full article →]({url})")


# ===========================================================
# PAGE: EVENT INTELLIGENCE
# ===========================================================

elif page == "🌍 Event Intelligence":
    st.subheader("🌍 Event Intelligence")

    if not st.session_state.pipeline_run:
        st.info("Run the pipeline from the Dashboard first.")
    else:
        events = st.session_state.events
        if not events:
            st.warning("No events extracted.")
        else:
            st.markdown(f"**{len(events)} events extracted by Event Agent**")
            st.divider()

            for i, ev in enumerate(events):
                headline   = getattr(ev, "headline",   f"Event {i+1}")
                event_type = getattr(ev, "event_type", "UNKNOWN")
                location   = getattr(ev, "location",   "—")
                summary    = getattr(ev, "summary",    "—")

                with st.expander(f"{i+1}. [{event_type}] {headline[:90]}"):
                    st.markdown(f"**Location:** {location}")
                    st.markdown(f"**Summary:** {summary}")


# ===========================================================
# PAGE: RESEARCH ANALYSIS
# ===========================================================

elif page == "🔬 Research Analysis":
    st.subheader("🔬 Research Analysis")

    if not st.session_state.pipeline_run:
        st.info("Run the pipeline from the Dashboard first.")
    else:
        reports = st.session_state.research_reports
        if not reports:
            st.warning("No research reports available.")
        else:
            st.markdown(f"**{len(reports)} research reports generated**")
            st.divider()

            for i, rr in enumerate(reports):
                headline = getattr(rr, "headline", f"Report {i+1}")

                with st.expander(f"{i+1}. {headline[:90]}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**Research Summary**")
                        st.write(getattr(rr, "research_summary", "—"))

                        st.markdown("**Affected Regions**")
                        for r in safe_list(getattr(rr, "affected_regions", [])):
                            st.markdown(f"- {r}")

                        st.markdown("**Affected Countries**")
                        for c in safe_list(getattr(rr, "affected_countries", [])):
                            st.markdown(f"- {c}")

                    with col2:
                        st.markdown("**Affected API Suppliers**")
                        for s in safe_list(getattr(rr, "affected_api_suppliers", [])):
                            st.markdown(f"- {s}")

                        st.markdown("**Affected Raw Materials**")
                        for m in safe_list(getattr(rr, "affected_raw_materials", [])):
                            st.markdown(f"- {m}")

                        conf = getattr(rr, "confidence", None)
                        if conf is not None:
                            st.markdown(f"**Confidence:** {conf * 100:.0f}%")

                    web_sources = safe_list(getattr(rr, "web_sources", []))
                    if web_sources:
                        st.markdown("**Web Sources**")
                        for s in web_sources:
                            st.markdown(f"- {s}")


# ===========================================================
# PAGE: RISK ASSESSMENT
# ===========================================================

elif page == "⚠️ Risk Assessment":
    st.subheader("⚠️ Risk Assessment")

    if not st.session_state.pipeline_run:
        st.info("Run the pipeline from the Dashboard first.")
    else:
        reports = st.session_state.risk_reports
        if not reports:
            st.warning("No risk reports available.")
        else:
            st.markdown(f"**{len(reports)} risk reports generated**")
            st.divider()

            for i, rr in enumerate(reports):
                headline    = getattr(rr, "headline", f"Report {i+1}")
                overall_risk  = getattr(rr, "overall_risk", "UNKNOWN")
                risk_score  = getattr(rr, "risk_score", 0)
                confidence  = getattr(rr, "confidence", 0)
                estimated_shortage_time = getattr(rr, "estimated_shortage_time", getattr(rr, "shortage", "Unknown"))

                with st.expander(
                    f"{i+1}. {headline[:80]} — {overall_risk}",
                    expanded=(i == 0),
                ):
                    st.markdown(risk_badge(overall_risk), unsafe_allow_html=True)

                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Risk Level",   overall_risk)
                    c2.metric("Risk Score",   f"{risk_score}/100")
                    c3.metric("Confidence",   f"{confidence * 100:.0f}%")
                    c4.metric("Shortage ETA", str(estimated_shortage_time))

                    st.markdown("**Reasoning**")
                    st.write(getattr(rr, "reasoning", "—"))

                    actions = safe_list(getattr(rr, "recommended_actions", getattr(rr, "actions", [])))
                    if actions:
                        st.markdown("**Recommended Actions**")
                        for a in actions:
                            st.success(a)

                    alt_suppliers = safe_list(getattr(rr, "alternative_suppliers", getattr(rr, "suppliers", [])))
                    if alt_suppliers:
                        st.markdown("**Alternative Suppliers**")
                        for s in alt_suppliers:
                            st.markdown(f"- {s}")


# ===========================================================
# PAGE: HOSPITAL SIMULATION
# ===========================================================

elif page == "🏥 Hospital Simulation":
    st.subheader("🏥 Hospital Simulation")
    st.caption(
        "Simulate the impact of a supply chain disruption on hospital operations. "
        "Pulls real disruption context from the Risk Agent when available."
    )
    st.divider()

    # ------------------------------------------------------
    # Helpers
    # ------------------------------------------------------

    def parse_shortage_duration(estimate: str) -> int:
        """
        Convert a RiskReport.estimated_shortage_time string
        (e.g. '1-2 Weeks', '2-4 Weeks', '1-3 Months', 'Unknown',
        'No expected shortage') into a usable simulation
        duration in days.

        Always returns a value within the simulation's allowed
        slider range (7-180) so it can safely seed the widget.
        """
        if not estimate:
            return 30

        text = estimate.strip().lower()

        if "no expected shortage" in text:
            return 14

        import re
        numbers = [int(n) for n in re.findall(r"\d+", text)]

        if not numbers:
            return 30  # "Unknown" or unparseable -> reasonable default

        # Use the upper end of the range for a conservative estimate
        upper = max(numbers)

        if "month" in text:
            days = upper * 30
        else:  # weeks, or no unit given
            days = upper * 7

        return max(7, min(180, days))

    def risk_score_to_usage_multiplier(score: int) -> float:
        """
        Higher risk scores imply more panic-buying / hoarding /
        rationing behavior at the hospital level, modeled as a
        modest bump to baseline daily usage.
        """
        if score >= 80:
            return 1.4
        if score >= 50:
            return 1.2
        return 1.0

    # ------------------------------------------------------
    # Source selection: real risk report vs manual entry
    # ------------------------------------------------------

    has_risk_data = bool(
        st.session_state.pipeline_run and st.session_state.risk_reports
    )

    selected_report = None

    if has_risk_data:
        source_mode = st.radio(
            "Simulation Source",
            ["📡 Use a Risk Report", "✍️ Manual Entry"],
            horizontal=True,
        )
    else:
        source_mode = "✍️ Manual Entry"
        st.info(
            "No pipeline run yet — simulating with manually entered values. "
            "Run the pipeline from the Dashboard to simulate against real "
            "detected disruptions."
        )

    if source_mode == "📡 Use a Risk Report":
        # Flatten (report, medicine) pairs so the dropdown is
        # per-medicine, not per-report.
        med_options = []
        for r in st.session_state.risk_reports:
            meds = safe_list(getattr(r, "affected_medicines", []))
            if not meds:
                continue
            for m in meds:
                med_options.append((f"{m} — {r.headline[:60]} ({r.overall_risk})", m, r))

        if not med_options:
            st.warning(
                "The latest pipeline run didn't flag specific medicines. "
                "Switch to Manual Entry below."
            )
            source_mode = "✍️ Manual Entry"
        else:
            labels = [opt[0] for opt in med_options]
            choice = st.selectbox("Select an at-risk medicine", labels)
            idx = labels.index(choice)
            default_medicine, selected_report = med_options[idx][1], med_options[idx][2]

            st.markdown(
                f"**Risk Level:** {risk_badge(selected_report.overall_risk)} &nbsp;&nbsp;"
                f"**Risk Score:** {selected_report.risk_score}/100 &nbsp;&nbsp;"
                f"**Estimated Shortage:** {selected_report.estimated_shortage_time}",
                unsafe_allow_html=True,
            )
            st.caption(f"Triggering event: {selected_report.headline}")

    if source_mode == "✍️ Manual Entry":
        default_medicine = ""

    st.divider()

    # ------------------------------------------------------
    # Simulation inputs
    # ------------------------------------------------------

    default_duration = (
        parse_shortage_duration(selected_report.estimated_shortage_time)
        if selected_report else 30
    )
    default_scenario_map = {
        "Shipping Disruption": "Port Closure",
        "Manufacturing Disruption": "Factory Shutdown",
        "Trade Restriction": "Export Ban",
        "Geopolitical Conflict": "Sanctions",
        "Natural Disaster": "Natural Disaster",
    }
    default_scenario = (
        default_scenario_map.get(selected_report.event_type, "Factory Shutdown")
        if selected_report else "Factory Shutdown"
    )
    scenario_options = ["Factory Shutdown", "Port Closure", "Export Ban", "Natural Disaster", "Sanctions"]

    col1, col2 = st.columns(2)
    with col1:
        scenario = st.selectbox(
            "Disruption Scenario",
            scenario_options,
            index=scenario_options.index(default_scenario),
        )
        medicine = st.text_input("Medicine / API", value=default_medicine, placeholder="e.g. Paracetamol")
        hospital_beds = st.number_input("Hospital Bed Count", min_value=50, max_value=5000, value=500, step=50)
    with col2:
        duration_days = st.slider("Disruption Duration (days)", 7, 180, default_duration)
        current_stock = st.slider("Current Stock (days of supply)", 1, 90, 14)
        daily_usage   = st.number_input("Baseline Daily Units Used", min_value=10, max_value=10000, value=200, step=10)

    if selected_report:
        st.caption(
            f"💡 Duration pre-filled from the Risk Agent's estimate "
            f"(\"{selected_report.estimated_shortage_time}\"). Adjust as needed."
        )

    if st.button("▶ Run Simulation", type="primary"):
        usage_multiplier = (
            risk_score_to_usage_multiplier(selected_report.risk_score)
            if selected_report else 1.0
        )
        effective_daily_usage = daily_usage * usage_multiplier

        shortage_day = max(0, current_stock)
        deficit_days = max(0, duration_days - current_stock)
        total_deficit = deficit_days * effective_daily_usage

        st.divider()
        st.markdown("#### Simulation Results")

        if selected_report and usage_multiplier > 1.0:
            st.caption(
                f"⚠️ Daily usage adjusted ×{usage_multiplier:.1f} to reflect "
                f"{selected_report.overall_risk} risk level (hoarding / rationing effects)."
            )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Shortage Onset", f"Day {shortage_day}")
        m2.metric("Days Without Stock", str(deficit_days))
        m3.metric("Total Unit Deficit", f"{total_deficit:,.0f}")
        m4.metric("Beds Affected (est.)", f"{hospital_beds:,}" if deficit_days > 0 else "0")

        # Timeline chart
        days = list(range(duration_days + 1))
        stock_levels = [max(0, current_stock - d) * effective_daily_usage for d in days]
        df_sim = pd.DataFrame({"Day": days, "Stock Units": stock_levels})

        fig = px.area(
            df_sim, x="Day", y="Stock Units",
            title=f"Projected Stock Level — {medicine or 'Medicine'} ({scenario})",
            color_discrete_sequence=["#3fb950"],
        )
        fig.add_vline(
            x=shortage_day,
            line_dash="dash",
            line_color="#f85149",
            annotation_text="Stock depleted",
            annotation_position="top",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e6edf3",
        )
        st.plotly_chart(fig, use_container_width=True)

        if deficit_days > 0:
            st.error(
                f"⚠️ Stock will run out on **Day {shortage_day}**. "
                f"Procure at least **{total_deficit:,.0f} units** to cover the disruption."
            )
            if medicine.strip():
                st.info(
                    f"💊 Need a backup plan? Check the **Drug Alternatives** page "
                    f"for therapeutic substitutes for **{medicine.strip()}**."
                )
        else:
            st.success("✅ Current stock is sufficient to cover the full disruption window.")


# ===========================================================
# PAGE: DRUG ALTERNATIVES
# ===========================================================

elif page == "💊 Drug Alternatives":
    st.subheader("💊 Drug Alternatives")
    st.caption(
        "Find therapeutic alternatives when a medicine faces a shortage. "
        "Results are grounded in live web evidence, not pre-loaded data."
    )
    st.divider()

    tab_manual, tab_auto = st.tabs(["🔍 Manual Search", "⚡ Auto-Suggest from Risk Reports"])

    # ------------------------------------------------------
    # Render helper for a single AlternativesReport
    # ------------------------------------------------------

    def render_alternatives_report(report):
        if not report.recognized:
            st.warning(
                f"**{report.queried_medicine}** could not be confirmed as a "
                "recognized medicine from available web evidence. "
                "Check the spelling, or try the generic name."
            )
            return

        if report.shortage_context:
            st.markdown(f"**Shortage Context:** {report.shortage_context}")

        if report.therapeutic_class:
            st.markdown(f"**Therapeutic Class:** {report.therapeutic_class}")

        st.markdown(f"**Confidence:** {report.confidence * 100:.0f}%")

        if not report.alternatives:
            st.info(
                "No reliable web evidence was found supporting a specific "
                "alternative for this medicine."
            )
        else:
            st.markdown(f"#### Alternatives for **{report.queried_medicine.title()}**")
            cols = st.columns(min(len(report.alternatives), 4))
            for col, alt in zip(cols, report.alternatives):
                caution_html = (
                    f'<p style="font-size:11px;color:#f85149;margin-top:6px;">⚠ {alt.caution}</p>'
                    if alt.caution else ""
                )
                col.markdown(
                    f'<div class="pw-card" style="text-align:center">'
                    f'<h4>Alternative</h4>'
                    f'<p style="font-size:16px">{alt.name}</p>'
                    f'<p style="font-size:11px;color:#8b949e;font-weight:400;">{alt.drug_class or ""}</p>'
                    f'{caution_html}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            with st.expander("Why these alternatives?"):
                for alt in report.alternatives:
                    st.markdown(f"**{alt.name}** — {alt.similarity_notes}")
                    if alt.caution:
                        st.caption(f"⚠ {alt.caution}")

        if report.web_sources:
            with st.expander(f"Web Sources ({len(report.web_sources)})"):
                for src in report.web_sources:
                    st.markdown(f"- [{src}]({src})")

        st.caption(report.disclaimer)

    # ------------------------------------------------------
    # TAB 1 — Manual Search
    # ------------------------------------------------------

    with tab_manual:
        query = st.text_input("Enter medicine name", placeholder="e.g. Amoxicillin")

        if st.button("🔍 Find Alternatives", type="primary"):
            if not query.strip():
                st.warning("Please enter a medicine name.")
            else:
                with st.spinner(f"Searching the web and analyzing alternatives for {query}…"):
                    agent = AlternativesAgent()
                    report = agent.lookup(query)
                st.divider()
                render_alternatives_report(report)

    # ------------------------------------------------------
    # TAB 2 — Auto-Suggest from Risk Reports
    # ------------------------------------------------------

    with tab_auto:
        if not st.session_state.pipeline_run or not st.session_state.risk_reports:
            st.info(
                "Run the pipeline from the Dashboard first — this tab suggests "
                "alternatives for medicines your Risk Agent has already flagged "
                "as at-risk."
            )
        else:
            all_meds = sorted({
                med
                for r in st.session_state.risk_reports
                for med in safe_list(getattr(r, "affected_medicines", []))
            })

            if not all_meds:
                st.info("The latest pipeline run did not flag any specific medicines.")
            else:
                st.markdown(f"**{len(all_meds)} at-risk medicine(s)** found in the latest pipeline run.")

                if st.button("⚡ Suggest Alternatives for All", type="primary"):
                    with st.spinner("Researching alternatives for at-risk medicines…"):
                        agent = AlternativesAgent()
                        st.session_state.alternatives_reports = agent.suggest_for_risk_reports(
                            st.session_state.risk_reports,
                            max_medicines=10,
                        )

                if st.session_state.alternatives_reports:
                    st.divider()
                    for i, report in enumerate(st.session_state.alternatives_reports):
                        with st.expander(
                            f"{i+1}. {report.queried_medicine}",
                            expanded=(i == 0),
                        ):
                            render_alternatives_report(report)

    st.divider()
    st.caption(
        "⚠️ This tool is for supply-chain planning only. "
        "All therapeutic substitutions must be approved by a licensed clinician."
    )


# ===========================================================
# PAGE: ANALYTICS
# ===========================================================

elif page == "📈 Analytics":
    st.subheader("📈 Analytics")

    if not st.session_state.pipeline_run or not st.session_state.risk_reports:
        st.info("Run the pipeline from the Dashboard to see analytics.")
    else:
        reports = st.session_state.risk_reports

        # ---- Risk level distribution ----
        risk_counts = {}
        for r in reports:
            lvl = getattr(r, "overall_risk", "UNKNOWN").upper()
            risk_counts[lvl] = risk_counts.get(lvl, 0) + 1

        df_risk = pd.DataFrame(
            {"Risk Level": list(risk_counts.keys()), "Count": list(risk_counts.values())}
        )

        col1, col2 = st.columns(2)

        with col1:
            fig_pie = px.pie(
                df_risk, names="Risk Level", values="Count",
                title="Risk Level Distribution",
                color="Risk Level",
                color_discrete_map={
                    "LOW": "#3fb950", "MEDIUM": "#d29922",
                    "HIGH": "#f85149", "CRITICAL": "#ff7b72",
                },
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", font_color="#e6edf3"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            scores = [getattr(r, "risk_score", 0) for r in reports]
            headlines = [
                getattr(r, "headline", f"Event {i}")[:40] + "…"
                for i, r in enumerate(reports)
            ]
            df_scores = pd.DataFrame({"Event": headlines, "Risk Score": scores})
            df_scores = df_scores.sort_values("Risk Score", ascending=True)

            fig_bar = px.bar(
                df_scores, x="Risk Score", y="Event", orientation="h",
                title="Risk Scores by Event",
                color="Risk Score",
                color_continuous_scale=["#3fb950", "#d29922", "#f85149"],
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e6edf3",
                showlegend=False,
                yaxis_title="",
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # ---- Region frequency ----
        region_freq = {}
        for r in reports:
            for reg in safe_list(getattr(r, "affected_regions", [])):
                region_freq[reg] = region_freq.get(reg, 0) + 1

        if region_freq:
            df_reg = pd.DataFrame(
                {"Region": list(region_freq.keys()), "Events": list(region_freq.values())}
            ).sort_values("Events", ascending=False)

            fig_reg = px.bar(
                df_reg, x="Region", y="Events",
                title="Most Affected Regions",
                color="Events",
                color_continuous_scale=["#1a3a2a", "#f85149"],
            )
            fig_reg.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e6edf3",
                showlegend=False,
            )
            st.plotly_chart(fig_reg, use_container_width=True)


# ===========================================================
# PAGE: ABOUT
# ===========================================================

elif page == "ℹ️ About":
    st.subheader("ℹ️ About PharmaWatch AI")
    st.divider()

    st.markdown("""
**PharmaWatch AI** is a real-time pharmaceutical supply chain intelligence platform
built for the **Confluence Hackathon** by **Code Force**.

#### What it does
- Monitors global news and geopolitical events (NewsAPI + GDELT)
- Extracts supply-chain disruption events using an AI **Event Agent**
- Conducts deep research on each event using a **Research Agent** (Tavily + Groq)
- Produces structured risk assessments via a **Risk Agent**
- Presents actionable intelligence through this Streamlit dashboard

#### Technology Stack

| Layer | Technology |
|---|---|
| LLM | Groq (Llama 3.1 8B / 70B) |
| Web Research | Tavily Search API |
| News Feed | NewsAPI |
| Geopolitical Events | GDELT Project |
| Orchestration | LangChain + LangGraph |
| Frontend | Streamlit + Plotly |
| Data Models | Pydantic v2 |

#### Pipeline Architecture
```
NewsAPI + GDELT
      ↓
  Event Agent   (classify & extract events)
      ↓
Research Agent  (Tavily web search + LLM synthesis)
      ↓
  Risk Agent    (risk scoring + recommendations)
      ↓
  Dashboard     (this UI)
```

#### Team
Built with ❤️ by **Code Force Team** · Confluence Hackathon
    """)


# ===========================================================
# FOOTER
# ===========================================================

st.divider()
st.caption(
    "PharmaWatch AI · Prototype · "
    + (f"Last updated: {st.session_state.run_timestamp}" if st.session_state.run_timestamp else "Not yet run")
)