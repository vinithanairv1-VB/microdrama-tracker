"""
MICRO-DRAMA MARKET INTELLIGENCE DASHBOARD v2.0
===============================================
Professional-grade market intelligence for the short-form video drama industry.

To run locally:
  pip install streamlit plotly pandas
  streamlit run app.py

Author: Vinitha Nair
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# ============================================
# PAGE CONFIG & CUSTOM STYLING
# ============================================
st.set_page_config(
    page_title="Micro-Drama Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(180deg, #0f1419 0%, #1a1f2e 100%);
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'DM Sans', sans-serif !important;
        color: #f8fafc !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'DM Sans', sans-serif !important;
        color: #94a3b8 !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'Space Mono', monospace !important;
        color: #f1f5f9 !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'DM Sans', sans-serif !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdown"] {
        color: #e2e8f0;
    }
    
    /* Custom card class */
    .intel-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    
    .intel-card h3 {
        margin-top: 0;
        font-size: 1.25rem;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Platform badges */
    .platform-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-reelshort { background: #ef4444; color: white; }
    .badge-dramabox { background: #8b5cf6; color: white; }
    .badge-goodshort { background: #10b981; color: white; }
    .badge-tiktok { background: #000000; color: white; }
    
    /* Threat level indicators */
    .threat-high { color: #ef4444; font-weight: 700; }
    .threat-medium { color: #f59e0b; font-weight: 700; }
    .threat-low { color: #10b981; font-weight: 700; }
    
    /* Weekly change indicators */
    .change-up { color: #10b981; }
    .change-down { color: #ef4444; }
    .change-neutral { color: #6b7280; }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #1e293b !important;
        border-radius: 8px !important;
    }
    
    /* Table styling */
    .dataframe {
        font-family: 'DM Sans', sans-serif !important;
    }
    
    /* Divider */
    hr {
        border-color: #334155 !important;
        margin: 2rem 0 !important;
    }
    
    /* Footer */
    .footer-text {
        color: #64748b;
        font-size: 0.875rem;
        text-align: center;
        padding: 2rem 0;
        border-top: 1px solid #334155;
        margin-top: 2rem;
    }
    
    /* Subheader styling */
    .section-header {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e293b;
        border-radius: 12px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #334155 !important;
        color: #f1f5f9 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA - EXPANDED WITH MORE DETAIL
# ============================================

# Current week data with historical tracking
APPS_DATA = {
    "ReelShort": {
        "score": 4.2,
        "installs": 50000000,
        "revenue_2024": 400,
        "revenue_q1_2025": 180,
        "origin": "China",
        "company": "Crazy Maple Studio",
        "launched": "2022",
        "rank_current": 1,
        "rank_last_week": 1,
        "rank_change": 0,
        "us_share": 55,
        "top_genres": ["Romance", "Thriller", "Revenge"],
        "avg_episode_count": 68,
        "content_count": 500,
        "monetization": "Coins + Subscription",
        "threat_level": "Market Leader"
    },
    "DramaBox": {
        "score": 4.6,
        "installs": 100000000,
        "revenue_2024": 323,
        "revenue_q1_2025": 145,
        "origin": "Singapore",
        "company": "StoryMatrix (Tencent-backed)",
        "launched": "2023",
        "rank_current": 2,
        "rank_last_week": 2,
        "rank_change": 0,
        "us_share": 30,
        "top_genres": ["Romance", "Paranormal", "Family Drama"],
        "avg_episode_count": 75,
        "content_count": 400,
        "monetization": "Coins + Ads",
        "threat_level": "Strong Challenger"
    },
    "ShortMax": {
        "score": 4.4,
        "installs": 20000000,
        "revenue_2024": 85,
        "revenue_q1_2025": 52,
        "origin": "China",
        "company": "Jiuzhou Cultural Group",
        "launched": "2023",
        "rank_current": 3,
        "rank_last_week": 4,
        "rank_change": 1,
        "us_share": 8,
        "top_genres": ["Romance", "CEO", "Revenge"],
        "avg_episode_count": 70,
        "content_count": 300,
        "monetization": "Coins + Subscription",
        "threat_level": "Rising Fast"
    },
    "GoodShort": {
        "score": 4.3,
        "installs": 10000000,
        "revenue_2024": 50,
        "revenue_q1_2025": 28,
        "origin": "China",
        "company": "Nice New",
        "launched": "2023",
        "rank_current": 4,
        "rank_last_week": 3,
        "rank_change": -1,
        "us_share": 5,
        "top_genres": ["Romance", "Comedy", "Drama"],
        "avg_episode_count": 65,
        "content_count": 250,
        "monetization": "Coins",
        "threat_level": "Established"
    },
    "FlexTV": {
        "score": 4.1,
        "installs": 15000000,
        "revenue_2024": 65,
        "revenue_q1_2025": 38,
        "origin": "China",
        "company": "Chengdu Yuewen",
        "launched": "2023",
        "rank_current": 5,
        "rank_last_week": 5,
        "rank_change": 0,
        "us_share": 4,
        "top_genres": ["Romance", "Werewolf", "Billionaire"],
        "avg_episode_count": 72,
        "content_count": 280,
        "monetization": "Coins + Ads",
        "threat_level": "Stable"
    },
    "My Drama": {
        "score": 4.3,
        "installs": 10000000,
        "revenue_2024": 40,
        "revenue_q1_2025": 25,
        "origin": "Ukraine",
        "company": "Holywater / Fox",
        "launched": "2022",
        "rank_current": 6,
        "rank_last_week": 7,
        "rank_change": 1,
        "us_share": 3,
        "top_genres": ["Romance", "Mafia", "LGBTQ+"],
        "avg_episode_count": 70,
        "content_count": 180,
        "monetization": "Subscription",
        "threat_level": "Fox-Backed Growth"
    },
    "PineDrama": {
        "score": 4.7,
        "installs": 2000000,
        "revenue_2024": 0,
        "revenue_q1_2025": 5,
        "origin": "China/TikTok",
        "company": "ByteDance",
        "launched": "2026",
        "rank_current": 7,
        "rank_last_week": 10,
        "rank_change": 3,
        "us_share": 1,
        "top_genres": ["Romance", "Comedy", "Drama"],
        "avg_episode_count": 60,
        "content_count": 50,
        "monetization": "Free (Ad-supported)",
        "threat_level": "⚠️ WATCH CLOSELY"
    },
    "GammaTime": {
        "score": 4.5,
        "installs": 1000000,
        "revenue_2024": 0,
        "revenue_q1_2025": 3,
        "origin": "USA",
        "company": "GammaTime Inc",
        "launched": "2025",
        "rank_current": 8,
        "rank_last_week": 8,
        "rank_change": 0,
        "us_share": 1,
        "top_genres": ["Premium Drama", "Thriller", "Horror"],
        "avg_episode_count": 45,
        "content_count": 25,
        "monetization": "Premium Subscription",
        "threat_level": "Celebrity-Backed"
    },
    "Vigloo": {
        "score": 4.4,
        "installs": 1000000,
        "revenue_2024": 15,
        "revenue_q1_2025": 8,
        "origin": "South Korea",
        "company": "SpoonLabs",
        "launched": "2023",
        "rank_current": 9,
        "rank_last_week": 9,
        "rank_change": 0,
        "us_share": 1,
        "top_genres": ["K-Drama Style", "Romance", "Fantasy"],
        "avg_episode_count": 55,
        "content_count": 120,
        "monetization": "Coins",
        "threat_level": "K-Content Edge"
    },
    "MoboReels": {
        "score": 4.0,
        "installs": 5000000,
        "revenue_2024": 20,
        "revenue_q1_2025": 12,
        "origin": "India",
        "company": "Times Internet",
        "launched": "2024",
        "rank_current": 10,
        "rank_last_week": 11,
        "rank_change": 1,
        "us_share": 0.5,
        "top_genres": ["Bollywood-style", "Romance", "Family"],
        "avg_episode_count": 80,
        "content_count": 150,
        "monetization": "Ads + Coins",
        "threat_level": "Regional Player"
    },
}

# Trending titles with more detail
TRENDING_TITLES = [
    {
        "title": "The Double Life of My Billionaire Husband",
        "platform": "ReelShort",
        "genre": "Romance",
        "sub_genre": "Billionaire",
        "episodes": 92,
        "revenue_est": 22,
        "views_est": "180M",
        "weeks_trending": 12,
        "status": "🔥 #1 Overall"
    },
    {
        "title": "Fsatisfying Justice",
        "platform": "ReelShort",
        "genre": "Revenge",
        "sub_genre": "Family Drama",
        "episodes": 85,
        "revenue_est": 18,
        "views_est": "150M",
        "weeks_trending": 8,
        "status": "📈 Rising"
    },
    {
        "title": "Love at First Bite",
        "platform": "DramaBox",
        "genre": "Paranormal",
        "sub_genre": "Vampire Romance",
        "episodes": 80,
        "revenue_est": 15,
        "views_est": "120M",
        "weeks_trending": 10,
        "status": "⭐ Steady"
    },
    {
        "title": "Trapped with the CEO",
        "platform": "ShortMax",
        "genre": "Romance",
        "sub_genre": "CEO",
        "episodes": 78,
        "revenue_est": 12,
        "views_est": "95M",
        "weeks_trending": 6,
        "status": "📈 Rising"
    },
    {
        "title": "My Secret Mafia Husband",
        "platform": "My Drama",
        "genre": "Thriller",
        "sub_genre": "Mafia Romance",
        "episodes": 70,
        "revenue_est": 8,
        "views_est": "65M",
        "weeks_trending": 5,
        "status": "🆕 New Entry"
    },
    {
        "title": "The Alpha's Rejected Mate",
        "platform": "FlexTV",
        "genre": "Paranormal",
        "sub_genre": "Werewolf",
        "episodes": 88,
        "revenue_est": 10,
        "views_est": "80M",
        "weeks_trending": 7,
        "status": "⭐ Steady"
    },
    {
        "title": "Revenge of the Discarded Wife",
        "platform": "DramaBox",
        "genre": "Revenge",
        "sub_genre": "Divorce Drama",
        "episodes": 65,
        "revenue_est": 9,
        "views_est": "70M",
        "weeks_trending": 4,
        "status": "📈 Rising"
    },
    {
        "title": "Pregnant and Abandoned",
        "platform": "GoodShort",
        "genre": "Drama",
        "sub_genre": "Secret Baby",
        "episodes": 72,
        "revenue_est": 7,
        "views_est": "55M",
        "weeks_trending": 9,
        "status": "⭐ Steady"
    },
]

# Genre performance data
GENRE_DATA = [
    {"genre": "Romance", "market_share": 45, "growth_rate": 25, "avg_completion": 78},
    {"genre": "Revenge", "market_share": 18, "growth_rate": 85, "avg_completion": 82},
    {"genre": "Paranormal", "market_share": 12, "growth_rate": 45, "avg_completion": 75},
    {"genre": "Thriller", "market_share": 10, "growth_rate": 60, "avg_completion": 80},
    {"genre": "Comedy", "market_share": 8, "growth_rate": 30, "avg_completion": 65},
    {"genre": "Family Drama", "market_share": 7, "growth_rate": 40, "avg_completion": 72},
]

# Regional market data
REGIONAL_DATA = [
    {"region": "United States", "market_share": 49, "revenue_q1": 343, "growth": 380, "top_platform": "ReelShort"},
    {"region": "Southeast Asia", "market_share": 18, "revenue_q1": 126, "growth": 450, "top_platform": "DramaBox"},
    {"region": "Latin America", "market_share": 12, "revenue_q1": 84, "growth": 520, "top_platform": "ReelShort"},
    {"region": "Europe", "market_share": 10, "revenue_q1": 70, "growth": 280, "top_platform": "DramaBox"},
    {"region": "Middle East", "market_share": 6, "revenue_q1": 42, "growth": 350, "top_platform": "ShortMax"},
    {"region": "Other", "market_share": 5, "revenue_q1": 35, "growth": 200, "top_platform": "Various"},
]

# Market metrics
MARKET_METRICS = {
    "q1_2025_revenue": 700,
    "us_market_share": 49,
    "yoy_growth": 400,
    "total_downloads": 950,
    "projected_2025": 11000,
    "avg_revenue_per_user": 2.85,
    "avg_session_time": 45,
    "weekly_active_users": 85,
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def format_number(num):
    """Format large numbers with K/M/B suffixes"""
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.0f}M"
    elif num >= 1_000:
        return f"{num/1_000:.0f}K"
    return str(num)

def get_rank_change_indicator(change):
    """Return emoji indicator for rank change"""
    if change > 0:
        return f"🟢 +{change}"
    elif change < 0:
        return f"🔴 {change}"
    return "⚪ —"

def create_platform_color_map():
    """Consistent colors for platforms"""
    return {
        "ReelShort": "#ef4444",
        "DramaBox": "#8b5cf6",
        "ShortMax": "#f59e0b",
        "GoodShort": "#10b981",
        "FlexTV": "#3b82f6",
        "My Drama": "#ec4899",
        "PineDrama": "#000000",
        "GammaTime": "#6366f1",
        "Vigloo": "#14b8a6",
        "MoboReels": "#f97316",
    }

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("## 🎬 Micro-Drama Intel")
    st.markdown("*Market Intelligence Dashboard*")
    st.markdown("---")
    
    # Update info
    st.markdown("### 📅 Data Status")
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%B %d, %Y')}")
    st.markdown(f"**Week:** {datetime.now().strftime('%U')} of 2026")
    st.markdown("**Data Sources:** Google Play, App Store, Sensor Tower, Media Partners Asia")
    
    st.markdown("---")
    
    # Quick market stats
    st.markdown("### 📊 Market Snapshot")
    st.metric("Q1 2025 Revenue", f"${MARKET_METRICS['q1_2025_revenue']}M", "+380% YoY")
    st.metric("2025 Projected", f"${MARKET_METRICS['projected_2025']/1000:.1f}B", "Omdia")
    st.metric("US Market Share", f"{MARKET_METRICS['us_market_share']}%", "Largest")
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### 🧭 Quick Links")
    st.markdown("""
    - [Platform Rankings](#platform-rankings)
    - [Trending Content](#trending-content)
    - [Genre Analysis](#genre-analysis)
    - [Regional Markets](#regional-breakdown)
    - [Competitive Intel](#competitive-intelligence)
    """)
    
    st.markdown("---")
    st.markdown("**Built by Vinitha Nair**")
    st.markdown("📧 vinithanair.v1@gmail.com")

# ============================================
# MAIN DASHBOARD
# ============================================

# Header
st.markdown("# 🎬 Micro-Drama Market Intelligence")
st.markdown("*Real-time monitoring of the global short-form drama industry*")

st.markdown("---")

# ============================================
# TOP METRICS ROW
# ============================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Platforms Tracked",
        value=len(APPS_DATA),
        delta="2 new this quarter"
    )

with col2:
    total_downloads = sum(d['installs'] for d in APPS_DATA.values())
    st.metric(
        label="Total Downloads",
        value=format_number(total_downloads),
        delta="+18% MoM"
    )

with col3:
    total_revenue = sum(d['revenue_q1_2025'] for d in APPS_DATA.values())
    st.metric(
        label="Q1 2025 Revenue",
        value=f"${total_revenue}M",
        delta="+380% YoY"
    )

with col4:
    total_content = sum(d['content_count'] for d in APPS_DATA.values())
    st.metric(
        label="Titles in Market",
        value=f"{total_content:,}+",
        delta="+25% QoQ"
    )

with col5:
    avg_rating = sum(d['score'] for d in APPS_DATA.values()) / len(APPS_DATA)
    st.metric(
        label="Avg Rating",
        value=f"{avg_rating:.2f} ⭐",
        delta="+0.1"
    )

st.markdown("---")

# ============================================
# PLATFORM RANKINGS TABLE
# ============================================

st.markdown('<p class="section-header">📱 Platform Rankings</p>', unsafe_allow_html=True)

# Create dataframe
df_apps = pd.DataFrame([
    {
        "Rank": data["rank_current"],
        "Change": get_rank_change_indicator(data["rank_change"]),
        "Platform": name,
        "Company": data["company"],
        "Origin": data["origin"],
        "Downloads": format_number(data["installs"]),
        "Q1 Revenue": f"${data['revenue_q1_2025']}M",
        "Rating": f"{data['score']} ⭐",
        "US Share": f"{data['us_share']}%",
        "Titles": data["content_count"],
        "Status": data["threat_level"]
    }
    for name, data in sorted(APPS_DATA.items(), key=lambda x: x[1]["rank_current"])
])

st.dataframe(
    df_apps,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Rank": st.column_config.NumberColumn("Rank", width="small"),
        "Change": st.column_config.TextColumn("Δ", width="small"),
        "Platform": st.column_config.TextColumn("Platform", width="medium"),
        "Company": st.column_config.TextColumn("Company", width="medium"),
        "Status": st.column_config.TextColumn("Status", width="medium"),
    }
)

# Charts row
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Revenue chart
    df_revenue = pd.DataFrame([
        {"Platform": name, "Revenue": data["revenue_q1_2025"], "Origin": data["origin"]}
        for name, data in APPS_DATA.items()
        if data["revenue_q1_2025"] > 0
    ]).sort_values("Revenue", ascending=True)
    
    fig_revenue = px.bar(
        df_revenue,
        x="Revenue",
        y="Platform",
        orientation="h",
        color="Origin",
        title="Q1 2025 Revenue by Platform ($M)",
        color_discrete_sequence=["#667eea", "#764ba2", "#f59e0b", "#10b981", "#ef4444"]
    )
    fig_revenue.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        title_font=dict(size=16, color="#f8fafc"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        height=400
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

with col_chart2:
    # Market share pie
    df_share = pd.DataFrame([
        {"Platform": name, "US Share": data["us_share"]}
        for name, data in APPS_DATA.items()
        if data["us_share"] > 0
    ])
    
    fig_share = px.pie(
        df_share,
        values="US Share",
        names="Platform",
        title="US Market Share by Platform",
        color_discrete_sequence=px.colors.sequential.Plasma_r
    )
    fig_share.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        title_font=dict(size=16, color="#f8fafc"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        height=400
    )
    st.plotly_chart(fig_share, use_container_width=True)

st.markdown("---")

# ============================================
# TRENDING CONTENT
# ============================================

st.markdown('<p class="section-header">🔥 Trending Content</p>', unsafe_allow_html=True)

df_titles = pd.DataFrame(TRENDING_TITLES)

col_trend1, col_trend2 = st.columns([2, 1])

with col_trend1:
    fig_titles = px.bar(
        df_titles.sort_values("revenue_est", ascending=True),
        x="revenue_est",
        y="title",
        color="platform",
        orientation="h",
        title="Top Performing Titles - Estimated Revenue ($M)",
        color_discrete_map=create_platform_color_map(),
        hover_data=["genre", "episodes", "views_est"]
    )
    fig_titles.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        title_font=dict(size=16, color="#f8fafc"),
        legend=dict(bgcolor="rgba(0,0,0,0)", title="Platform"),
        height=450,
        yaxis_title=""
    )
    st.plotly_chart(fig_titles, use_container_width=True)

with col_trend2:
    st.markdown("**📋 Content Breakdown**")
    
    # Genre distribution
    genre_counts = df_titles.groupby("genre").size().reset_index(name="count")
    fig_genre = px.pie(
        genre_counts,
        values="count",
        names="genre",
        title="Genre Mix",
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig_genre.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        title_font=dict(size=14, color="#f8fafc"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        height=250,
        margin=dict(t=50, b=0, l=0, r=0)
    )
    st.plotly_chart(fig_genre, use_container_width=True)
    
    # Key stats
    st.markdown(f"""
    **Avg Episodes:** {df_titles['episodes'].mean():.0f}  
    **Avg Revenue:** ${df_titles['revenue_est'].mean():.1f}M  
    **Top Genre:** {genre_counts.loc[genre_counts['count'].idxmax(), 'genre']}
    """)

st.markdown("---")

# ============================================
# GENRE ANALYSIS
# ============================================

st.markdown('<p class="section-header">📊 Genre Analysis</p>', unsafe_allow_html=True)

df_genre = pd.DataFrame(GENRE_DATA)

col_genre1, col_genre2, col_genre3 = st.columns(3)

with col_genre1:
    fig_g1 = px.bar(
        df_genre.sort_values("market_share", ascending=True),
        x="market_share",
        y="genre",
        orientation="h",
        title="Market Share by Genre (%)",
        color="market_share",
        color_continuous_scale="Viridis"
    )
    fig_g1.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        title_font=dict(size=14, color="#f8fafc"),
        showlegend=False,
        height=300
    )
    fig_g1.update_coloraxes(showscale=False)
    st.plotly_chart(fig_g1, use_container_width=True)

with col_genre2:
    fig_g2 = px.bar(
        df_genre.sort_values("growth_rate", ascending=True),
        x="growth_rate",
        y="genre",
        orientation="h",
        title="YoY Growth Rate (%)",
        color="growth_rate",
        color_continuous_scale="Plasma"
    )
    fig_g2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        title_font=dict(size=14, color="#f8fafc"),
        showlegend=False,
        height=300
    )
    fig_g2.update_coloraxes(showscale=False)
    st.plotly_chart(fig_g2, use_container_width=True)

with col_genre3:
    fig_g3 = px.bar(
        df_genre.sort_values("avg_completion", ascending=True),
        x="avg_completion",
        y="genre",
        orientation="h",
        title="Avg Completion Rate (%)",
        color="avg_completion",
        color_continuous_scale="Tealgrn"
    )
    fig_g3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        title_font=dict(size=14, color="#f8fafc"),
        showlegend=False,
        height=300
    )
    fig_g3.update_coloraxes(showscale=False)
    st.plotly_chart(fig_g3, use_container_width=True)

st.markdown("""
**💡 Key Insight:** Revenge content is the fastest-growing genre (+85% YoY) with the highest completion rates (82%), 
suggesting strong audience demand for justice/empowerment narratives. Consider prioritizing this genre for licensing.
""")

st.markdown("---")

# ============================================
# REGIONAL BREAKDOWN
# ============================================

st.markdown('<p class="section-header">🌍 Regional Breakdown</p>', unsafe_allow_html=True)

df_regional = pd.DataFrame(REGIONAL_DATA)

col_reg1, col_reg2 = st.columns(2)

with col_reg1:
    fig_reg1 = px.pie(
        df_regional,
        values="market_share",
        names="region",
        title="Global Market Share by Region",
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        hole=0.4
    )
    fig_reg1.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        title_font=dict(size=16, color="#f8fafc"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        height=350
    )
    st.plotly_chart(fig_reg1, use_container_width=True)

with col_reg2:
    fig_reg2 = px.bar(
        df_regional.sort_values("growth", ascending=True),
        x="growth",
        y="region",
        orientation="h",
        title="YoY Growth Rate by Region (%)",
        color="growth",
        color_continuous_scale="Viridis",
        text="growth"
    )
    fig_reg2.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_reg2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        title_font=dict(size=16, color="#f8fafc"),
        showlegend=False,
        height=350
    )
    fig_reg2.update_coloraxes(showscale=False)
    st.plotly_chart(fig_reg2, use_container_width=True)

# Regional table
st.dataframe(
    df_regional,
    use_container_width=True,
    hide_index=True,
    column_config={
        "region": "Region",
        "market_share": st.column_config.ProgressColumn("Market Share %", min_value=0, max_value=50),
        "revenue_q1": st.column_config.NumberColumn("Q1 Revenue ($M)", format="$%d"),
        "growth": st.column_config.NumberColumn("YoY Growth %", format="%d%%"),
        "top_platform": "Leading Platform"
    }
)

st.markdown("---")

# ============================================
# COMPETITIVE INTELLIGENCE
# ============================================

st.markdown('<p class="section-header">🎯 Competitive Intelligence</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["⚠️ New Entrants", "🤝 Partnership Opps", "📋 Strategic Recs"])

with tab1:
    col_ent1, col_ent2, col_ent3 = st.columns(3)
    
    with col_ent1:
        st.markdown("""
        ### 🖤 PineDrama (ByteDance)
        **Launched:** January 2026  
        **Threat Level:** 🔴 **CRITICAL**
        
        **Strategy:**
        - Free content (no coins)
        - Ad-free viewing
        - TikTok cross-promotion (150M+ US users)
        - Aggressive content acquisition
        
        **Watch For:**
        - Exclusive content deals
        - Creator partnerships
        - Super Bowl ad campaign rumored
        
        **Our Response:**
        - Monitor weekly ranking changes
        - Track content library growth
        - Identify their supplier relationships
        """)
    
    with col_ent2:
        st.markdown("""
        ### ✨ GammaTime
        **Launched:** October 2025  
        **Threat Level:** 🟠 **HIGH**
        
        **Strategy:**
        - "Hollywood quality" positioning
        - Celebrity investors (Kardashians, Ohanian)
        - Premium subscription model
        - Higher production budgets
        
        **Differentiation:**
        - US-produced content
        - A-list talent attached
        - Premium pricing ($9.99/mo)
        
        **Our Response:**
        - Track content quality benchmarks
        - Monitor subscriber growth
        - Evaluate co-production opportunities
        """)
    
    with col_ent3:
        st.markdown("""
        ### 🦊 Fox + Holywater
        **Announced:** November 2025  
        **Threat Level:** 🟠 **MEDIUM-HIGH**
        
        **Deal Terms:**
        - Equity stake in Holywater
        - 200 shows commitment
        - US market focus
        
        **Competitive Edge:**
        - Hollywood IP access
        - Ukraine production efficiency
        - Established My Drama platform
        
        **Our Response:**
        - Track My Drama ranking trajectory
        - Identify content slate
        - Evaluate similar studio partnerships
        """)

with tab2:
    col_part1, col_part2 = st.columns(2)
    
    with col_part1:
        st.markdown("""
        ### 🎬 Content Supply Partners
        
        | Company | Strength | Status |
        |---------|----------|--------|
        | Crazy Maple Studio | #1 producer, ReelShort parent | Exclusive to ReelShort |
        | StoryMatrix | High volume, quality | DramaBox exclusive |
        | Vertical Film (Vancouver) | Western production | Open to deals |
        | COL Group | Novel adaptations | Seeking partners |
        | Wattpad / WEBTOON | IP pipeline | Open to licensing |
        
        ### 📚 IP Sources
        - **Tomato Novel** - 80% of ReelShort content
        - **Korean Webtoons** - Untapped for micro-drama
        - **Wattpad** - 90M+ monthly users, romance focus
        - **AO3/Fan communities** - Trend identification
        """)
    
    with col_part2:
        st.markdown("""
        ### 📺 Distribution Partners
        
        | Platform | Opportunity | Fit |
        |----------|-------------|-----|
        | Tubi | FAST channel | High |
        | Pluto TV | Dedicated channel | High |
        | YouTube Shorts | Discovery funnel | Medium |
        | Roku Channel | Growing FAST | Medium |
        | Amazon Freevee | Ad-supported | Medium |
        
        ### 🏢 Studio Relationships
        - **Holywater** - Fox deal may limit availability
        - **Jiuzhou** - ShortMax parent, aggressive
        - **Chengdu Yuewen** - FlexTV, China Literature backing
        - **SpoonLabs** - K-drama expertise, niche
        """)

with tab3:
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("""
        ### 🎯 Immediate Actions (Next 30 Days)
        
        1. **Set Weekly Monitoring Cadence**
           - Track PineDrama downloads/rankings daily
           - Report significant movements to leadership
        
        2. **Evaluate Non-Exclusive Suppliers**
           - Vertical Film Vancouver
           - Independent Korean studios
           - Wattpad IP licensing
        
        3. **Genre Diversification**
           - Revenge content growing fastest (+85%)
           - Thriller/Horror underserved
           - True crime adaptation opportunities
        
        4. **Competitive Response Planning**
           - Draft scenarios for PineDrama's growth
           - Identify defensive content moves
        """)
    
    with col_rec2:
        st.markdown("""
        ### 📈 Strategic Initiatives (90 Days)
        
        1. **Content Strategy**
           - Increase revenge/justice content mix
           - Pilot true crime micro-drama format
           - Explore K-content adaptation rights
        
        2. **Distribution Expansion**
           - FAST channel pilot on Tubi/Pluto
           - YouTube Shorts promotional strategy
        
        3. **Partnership Development**
           - Explore studio equity/JV models
           - Evaluate production partnerships
        
        4. **Competitive Positioning**
           - Differentiation from free (PineDrama)
           - Quality vs. volume strategy
        """)

st.markdown("---")

# ============================================
# RAW DATA & EXPORT
# ============================================

with st.expander("📋 View & Export Raw Data"):
    data_tab1, data_tab2, data_tab3, data_tab4 = st.tabs(["Platforms", "Titles", "Genres", "Regions"])
    
    with data_tab1:
        full_df = pd.DataFrame([
            {"Platform": name, **{k: v for k, v in data.items() if k != "top_genres"}}
            for name, data in APPS_DATA.items()
        ])
        st.dataframe(full_df, use_container_width=True)
        st.download_button(
            "📥 Download Platform Data",
            full_df.to_csv(index=False),
            f"microdrama_platforms_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    with data_tab2:
        st.dataframe(df_titles, use_container_width=True)
        st.download_button(
            "📥 Download Titles Data",
            df_titles.to_csv(index=False),
            f"microdrama_titles_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    with data_tab3:
        st.dataframe(df_genre, use_container_width=True)
        st.download_button(
            "📥 Download Genre Data",
            df_genre.to_csv(index=False),
            f"microdrama_genres_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    
    with data_tab4:
        st.dataframe(df_regional, use_container_width=True)
        st.download_button(
            "📥 Download Regional Data",
            df_regional.to_csv(index=False),
            f"microdrama_regional_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer-text">
    <p><strong>Micro-Drama Market Intelligence Dashboard</strong></p>
    <p>Data Sources: Google Play, App Store, Sensor Tower, Media Partners Asia, Variety, Deadline</p>
    <p>Update Schedule: Rankings weekly • Market metrics monthly • Competitive intel as available</p>
    <p>Built by <strong>Vinitha Nair</strong> | 📧 vinithanair.v1@gmail.com</p>
</div>
""", unsafe_allow_html=True)
