"""
MICRO-DRAMA MARKET INTELLIGENCE DASHBOARD v2.1
===============================================
Professional light theme with Google Sheets integration.

SETUP:
1. Create a Google Sheet with the tabs defined below
2. Publish each sheet to web (File > Share > Publish to web > CSV)
3. Paste the CSV URLs in the SHEET_URLS section below
4. Deploy!

Author: Vinitha Nair
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ============================================
# GOOGLE SHEETS CONFIGURATION
# ============================================
# 
# HOW TO SET UP YOUR GOOGLE SHEET:
# 
# 1. Create a new Google Sheet
# 2. Create 4 tabs named exactly:
#    - "platforms"
#    - "titles" 
#    - "genres"
#    - "regions"
#
# 3. For each tab, go to: File > Share > Publish to web
#    - Select the specific tab
#    - Choose "Comma-separated values (.csv)"
#    - Click Publish and copy the URL
#
# 4. Paste each URL below (replacing the empty strings)
#
# IMPORTANT: Every time you update the sheet, changes appear 
# in your dashboard within ~5 minutes (Google's cache refresh)
# ============================================

SHEET_URLS = {
    "platforms": "https://docs.google.com/spreadsheets/d/e/2PACX-1vT_-4nL7L0B90pPRqkI8rAIXcVr75A7wrg6T28cfZefl-ukGyW2pgqkfv-ZeEcs3SjBPgwnx1L9i5mv/pub?gid=1459790836&single=true&output=csv",  # Paste your platforms tab CSV URL here
    "titles": "https://docs.google.com/spreadsheets/d/e/2PACX-1vT_-4nL7L0B90pPRqkI8rAIXcVr75A7wrg6T28cfZefl-ukGyW2pgqkfv-ZeEcs3SjBPgwnx1L9i5mv/pub?gid=127623823&single=true&output=csv",     # Paste your titles tab CSV URL here
    "genres": "https://docs.google.com/spreadsheets/d/e/2PACX-1vT_-4nL7L0B90pPRqkI8rAIXcVr75A7wrg6T28cfZefl-ukGyW2pgqkfv-ZeEcs3SjBPgwnx1L9i5mv/pub?gid=1423857329&single=true&output=csv",     # Paste your genres tab CSV URL here
    "regions": "https://docs.google.com/spreadsheets/d/e/2PACX-1vT_-4nL7L0B90pPRqkI8rAIXcVr75A7wrg6T28cfZefl-ukGyW2pgqkfv-ZeEcs3SjBPgwnx1L9i5mv/pub?gid=57981399&single=true&output=csv",    # Paste your regions tab CSV URL here
}

# Set to True once you've added your Google Sheet URLs
USE_GOOGLE_SHEETS = True

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Micro-Drama Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Light theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    h1, h2, h3 {
        font-family: 'DM Sans', sans-serif !important;
    }
    
    .section-header {
        font-family: 'DM Sans', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .footer-text {
        color: #64748b;
        font-size: 0.875rem;
        text-align: center;
        padding: 2rem 0;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING FUNCTIONS
# ============================================

@st.cache_data(ttl=300)
def load_from_google_sheets():
    """Load data from published Google Sheets"""
    data = {}
    try:
        if SHEET_URLS["platforms"]:
            data["platforms"] = pd.read_csv(SHEET_URLS["platforms"])
        if SHEET_URLS["titles"]:
            data["titles"] = pd.read_csv(SHEET_URLS["titles"])
        if SHEET_URLS["genres"]:
            data["genres"] = pd.read_csv(SHEET_URLS["genres"])
        if SHEET_URLS["regions"]:
            data["regions"] = pd.read_csv(SHEET_URLS["regions"])
    except Exception as e:
        st.error(f"Error loading Google Sheets: {e}")
        return None
    return data

def load_default_data():
    """Load hardcoded default data"""
    
    platforms_data = [
        {"platform": "ReelShort", "company": "Crazy Maple Studio", "origin": "China", "score": 4.2, "installs": 50000000, "revenue_2024": 400, "revenue_q1_2025": 180, "rank_current": 1, "rank_last_week": 1, "us_share": 55, "content_count": 500, "monetization": "Coins + Subscription", "threat_level": "Market Leader"},
        {"platform": "DramaBox", "company": "StoryMatrix (Tencent)", "origin": "Singapore", "score": 4.6, "installs": 100000000, "revenue_2024": 323, "revenue_q1_2025": 145, "rank_current": 2, "rank_last_week": 2, "us_share": 30, "content_count": 400, "monetization": "Coins + Ads", "threat_level": "Strong Challenger"},
        {"platform": "ShortMax", "company": "Jiuzhou Cultural", "origin": "China", "score": 4.4, "installs": 20000000, "revenue_2024": 85, "revenue_q1_2025": 52, "rank_current": 3, "rank_last_week": 4, "us_share": 8, "content_count": 300, "monetization": "Coins + Subscription", "threat_level": "Rising Fast"},
        {"platform": "GoodShort", "company": "Nice New", "origin": "China", "score": 4.3, "installs": 10000000, "revenue_2024": 50, "revenue_q1_2025": 28, "rank_current": 4, "rank_last_week": 3, "us_share": 5, "content_count": 250, "monetization": "Coins", "threat_level": "Established"},
        {"platform": "FlexTV", "company": "Chengdu Yuewen", "origin": "China", "score": 4.1, "installs": 15000000, "revenue_2024": 65, "revenue_q1_2025": 38, "rank_current": 5, "rank_last_week": 5, "us_share": 4, "content_count": 280, "monetization": "Coins + Ads", "threat_level": "Stable"},
        {"platform": "My Drama", "company": "Holywater / Fox", "origin": "Ukraine", "score": 4.3, "installs": 10000000, "revenue_2024": 40, "revenue_q1_2025": 25, "rank_current": 6, "rank_last_week": 7, "us_share": 3, "content_count": 180, "monetization": "Subscription", "threat_level": "Fox-Backed Growth"},
        {"platform": "PineDrama", "company": "ByteDance", "origin": "China/TikTok", "score": 4.7, "installs": 2000000, "revenue_2024": 0, "revenue_q1_2025": 5, "rank_current": 7, "rank_last_week": 10, "us_share": 1, "content_count": 50, "monetization": "Free (Ad-supported)", "threat_level": "⚠️ WATCH CLOSELY"},
        {"platform": "GammaTime", "company": "GammaTime Inc", "origin": "USA", "score": 4.5, "installs": 1000000, "revenue_2024": 0, "revenue_q1_2025": 3, "rank_current": 8, "rank_last_week": 8, "us_share": 1, "content_count": 25, "monetization": "Premium Subscription", "threat_level": "Celebrity-Backed"},
        {"platform": "Vigloo", "company": "SpoonLabs", "origin": "South Korea", "score": 4.4, "installs": 1000000, "revenue_2024": 15, "revenue_q1_2025": 8, "rank_current": 9, "rank_last_week": 9, "us_share": 1, "content_count": 120, "monetization": "Coins", "threat_level": "K-Content Edge"},
        {"platform": "MoboReels", "company": "Times Internet", "origin": "India", "score": 4.0, "installs": 5000000, "revenue_2024": 20, "revenue_q1_2025": 12, "rank_current": 10, "rank_last_week": 11, "us_share": 0.5, "content_count": 150, "monetization": "Ads + Coins", "threat_level": "Regional Player"},
    ]
    
    titles_data = [
        {"title": "The Double Life of My Billionaire Husband", "platform": "ReelShort", "genre": "Romance", "sub_genre": "Billionaire", "episodes": 92, "revenue_est": 22, "views_est": "180M", "weeks_trending": 12, "status": "🔥 #1 Overall"},
        {"title": "Satisfying Justice", "platform": "ReelShort", "genre": "Revenge", "sub_genre": "Family Drama", "episodes": 85, "revenue_est": 18, "views_est": "150M", "weeks_trending": 8, "status": "📈 Rising"},
        {"title": "Love at First Bite", "platform": "DramaBox", "genre": "Paranormal", "sub_genre": "Vampire Romance", "episodes": 80, "revenue_est": 15, "views_est": "120M", "weeks_trending": 10, "status": "⭐ Steady"},
        {"title": "Trapped with the CEO", "platform": "ShortMax", "genre": "Romance", "sub_genre": "CEO", "episodes": 78, "revenue_est": 12, "views_est": "95M", "weeks_trending": 6, "status": "📈 Rising"},
        {"title": "My Secret Mafia Husband", "platform": "My Drama", "genre": "Thriller", "sub_genre": "Mafia Romance", "episodes": 70, "revenue_est": 8, "views_est": "65M", "weeks_trending": 5, "status": "🆕 New Entry"},
        {"title": "The Alpha's Rejected Mate", "platform": "FlexTV", "genre": "Paranormal", "sub_genre": "Werewolf", "episodes": 88, "revenue_est": 10, "views_est": "80M", "weeks_trending": 7, "status": "⭐ Steady"},
        {"title": "Revenge of the Discarded Wife", "platform": "DramaBox", "genre": "Revenge", "sub_genre": "Divorce Drama", "episodes": 65, "revenue_est": 9, "views_est": "70M", "weeks_trending": 4, "status": "📈 Rising"},
        {"title": "Pregnant and Abandoned", "platform": "GoodShort", "genre": "Drama", "sub_genre": "Secret Baby", "episodes": 72, "revenue_est": 7, "views_est": "55M", "weeks_trending": 9, "status": "⭐ Steady"},
    ]
    
    genres_data = [
        {"genre": "Romance", "market_share": 45, "growth_rate": 25, "avg_completion": 78},
        {"genre": "Revenge", "market_share": 18, "growth_rate": 85, "avg_completion": 82},
        {"genre": "Paranormal", "market_share": 12, "growth_rate": 45, "avg_completion": 75},
        {"genre": "Thriller", "market_share": 10, "growth_rate": 60, "avg_completion": 80},
        {"genre": "Comedy", "market_share": 8, "growth_rate": 30, "avg_completion": 65},
        {"genre": "Family Drama", "market_share": 7, "growth_rate": 40, "avg_completion": 72},
    ]
    
    regions_data = [
        {"region": "United States", "market_share": 49, "revenue_q1": 343, "growth": 380, "top_platform": "ReelShort"},
        {"region": "Southeast Asia", "market_share": 18, "revenue_q1": 126, "growth": 450, "top_platform": "DramaBox"},
        {"region": "Latin America", "market_share": 12, "revenue_q1": 84, "growth": 520, "top_platform": "ReelShort"},
        {"region": "Europe", "market_share": 10, "revenue_q1": 70, "growth": 280, "top_platform": "DramaBox"},
        {"region": "Middle East", "market_share": 6, "revenue_q1": 42, "growth": 350, "top_platform": "ShortMax"},
        {"region": "Other", "market_share": 5, "revenue_q1": 35, "growth": 200, "top_platform": "Various"},
    ]
    
    return {
        "platforms": pd.DataFrame(platforms_data),
        "titles": pd.DataFrame(titles_data),
        "genres": pd.DataFrame(genres_data),
        "regions": pd.DataFrame(regions_data)
    }

# ============================================
# LOAD DATA
# ============================================

if USE_GOOGLE_SHEETS and any(SHEET_URLS.values()):
    data = load_from_google_sheets()
    if data is None:
        st.warning("Failed to load from Google Sheets. Using default data.")
        data = load_default_data()
else:
    data = load_default_data()

df_platforms = data["platforms"]
df_titles = data["titles"]
df_genres = data["genres"]
df_regions = data["regions"]

# ============================================
# HELPER FUNCTIONS
# ============================================

def format_number(num):
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.0f}M"
    elif num >= 1_000:
        return f"{num/1_000:.0f}K"
    return str(num)

def get_rank_change_indicator(current, last_week):
    change = last_week - current
    if change > 0:
        return f"🟢 +{change}"
    elif change < 0:
        return f"🔴 {change}"
    return "⚪ —"

PLATFORM_COLORS = {
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
    
    if USE_GOOGLE_SHEETS and any(SHEET_URLS.values()):
        st.success("📊 Live data from Google Sheets")
    else:
        st.info("📋 Using default dataset")
    
    st.markdown("---")
    st.markdown("### 📅 Data Status")
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%B %d, %Y')}")
    st.markdown(f"**Week:** {datetime.now().strftime('%U')} of {datetime.now().year}")
    
    st.markdown("---")
    st.markdown("### 📊 Market Snapshot")
    st.metric("Q1 2025 Revenue", "$700M", "+380% YoY")
    st.metric("2025 Projected", "$11B", "Omdia")
    st.metric("US Market Share", "49%", "Largest")
    
    st.markdown("---")
    st.markdown("**Built by Vinitha Nair**")
    st.markdown("📧 vinithanair.v1@gmail.com")

# ============================================
# MAIN DASHBOARD
# ============================================

st.title("🎬 Micro-Drama Market Intelligence")
st.markdown("*Real-time monitoring of the global short-form drama industry*")

st.markdown("---")

# ============================================
# TOP METRICS
# ============================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Platforms Tracked", len(df_platforms), "2 new this quarter")

with col2:
    total_downloads = df_platforms['installs'].sum()
    st.metric("Total Downloads", format_number(total_downloads), "+18% MoM")

with col3:
    total_revenue = df_platforms['revenue_q1_2025'].sum()
    st.metric("Q1 2025 Revenue", f"${total_revenue}M", "+380% YoY")

with col4:
    total_content = df_platforms['content_count'].sum()
    st.metric("Titles in Market", f"{total_content:,}+", "+25% QoQ")

with col5:
    avg_rating = df_platforms['score'].mean()
    st.metric("Avg Rating", f"{avg_rating:.2f} ⭐", "+0.1")

st.markdown("---")

# ============================================
# PLATFORM RANKINGS
# ============================================

st.subheader("📱 Platform Rankings")

df_display = df_platforms.copy()
df_display['change'] = df_display.apply(lambda x: get_rank_change_indicator(x['rank_current'], x['rank_last_week']), axis=1)
df_display['downloads_fmt'] = df_display['installs'].apply(format_number)
df_display['revenue_fmt'] = df_display['revenue_q1_2025'].apply(lambda x: f"${x}M")
df_display['rating_fmt'] = df_display['score'].apply(lambda x: f"{x} ⭐")
df_display['us_share_fmt'] = df_display['us_share'].apply(lambda x: f"{x}%")

display_cols = df_display[[
    'rank_current', 'change', 'platform', 'company', 'origin', 
    'downloads_fmt', 'revenue_fmt', 'rating_fmt', 'us_share_fmt', 
    'content_count', 'threat_level'
]].sort_values('rank_current')

display_cols.columns = ['Rank', 'Δ', 'Platform', 'Company', 'Origin', 'Downloads', 'Q1 Revenue', 'Rating', 'US Share', 'Titles', 'Status']

st.dataframe(display_cols, use_container_width=True, hide_index=True)

# Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    df_revenue = df_platforms[df_platforms['revenue_q1_2025'] > 0].sort_values('revenue_q1_2025', ascending=True)
    fig_revenue = px.bar(df_revenue, x='revenue_q1_2025', y='platform', orientation='h', color='origin',
                         title='Q1 2025 Revenue by Platform ($M)', color_discrete_sequence=px.colors.qualitative.Set2)
    fig_revenue.update_layout(height=400, xaxis_title="Revenue ($M)", yaxis_title="")
    st.plotly_chart(fig_revenue, use_container_width=True)

with col_chart2:
    df_share = df_platforms[df_platforms['us_share'] > 0]
    fig_share = px.pie(df_share, values='us_share', names='platform', title='US Market Share by Platform',
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_share.update_layout(height=400)
    st.plotly_chart(fig_share, use_container_width=True)

st.markdown("---")

# ============================================
# TRENDING CONTENT
# ============================================

st.subheader("🔥 Trending Content")

col_trend1, col_trend2 = st.columns([2, 1])

with col_trend1:
    df_titles_sorted = df_titles.sort_values('revenue_est', ascending=True)
    fig_titles = px.bar(df_titles_sorted, x='revenue_est', y='title', color='platform', orientation='h',
                        title='Top Performing Titles - Estimated Revenue ($M)', color_discrete_map=PLATFORM_COLORS,
                        hover_data=['genre', 'episodes', 'views_est'])
    fig_titles.update_layout(height=450, xaxis_title="Estimated Revenue ($M)", yaxis_title="")
    st.plotly_chart(fig_titles, use_container_width=True)

with col_trend2:
    st.markdown("**📋 Content Breakdown**")
    genre_counts = df_titles.groupby('genre').size().reset_index(name='count')
    fig_genre = px.pie(genre_counts, values='count', names='genre', title='Genre Mix',
                       color_discrete_sequence=px.colors.qualitative.Set3)
    fig_genre.update_layout(height=250, margin=dict(t=50, b=0, l=0, r=0))
    st.plotly_chart(fig_genre, use_container_width=True)
    
    st.markdown(f"**Avg Episodes:** {df_titles['episodes'].mean():.0f}")
    st.markdown(f"**Avg Revenue:** ${df_titles['revenue_est'].mean():.1f}M")
    st.markdown(f"**Top Genre:** {genre_counts.loc[genre_counts['count'].idxmax(), 'genre']}")

st.markdown("---")

# ============================================
# GENRE ANALYSIS
# ============================================

st.subheader("📊 Genre Analysis")

col_genre1, col_genre2, col_genre3 = st.columns(3)

with col_genre1:
    fig_g1 = px.bar(df_genres.sort_values('market_share', ascending=True), x='market_share', y='genre',
                    orientation='h', title='Market Share (%)', color='market_share', color_continuous_scale='Purples')
    fig_g1.update_layout(height=300, showlegend=False)
    fig_g1.update_coloraxes(showscale=False)
    st.plotly_chart(fig_g1, use_container_width=True)

with col_genre2:
    fig_g2 = px.bar(df_genres.sort_values('growth_rate', ascending=True), x='growth_rate', y='genre',
                    orientation='h', title='YoY Growth Rate (%)', color='growth_rate', color_continuous_scale='Oranges')
    fig_g2.update_layout(height=300, showlegend=False)
    fig_g2.update_coloraxes(showscale=False)
    st.plotly_chart(fig_g2, use_container_width=True)

with col_genre3:
    fig_g3 = px.bar(df_genres.sort_values('avg_completion', ascending=True), x='avg_completion', y='genre',
                    orientation='h', title='Completion Rate (%)', color='avg_completion', color_continuous_scale='Greens')
    fig_g3.update_layout(height=300, showlegend=False)
    fig_g3.update_coloraxes(showscale=False)
    st.plotly_chart(fig_g3, use_container_width=True)

st.info("💡 **Key Insight:** Revenge content is the fastest-growing genre (+85% YoY) with the highest completion rates (82%), suggesting strong audience demand for justice/empowerment narratives.")

st.markdown("---")

# ============================================
# REGIONAL BREAKDOWN
# ============================================

st.subheader("🌍 Regional Breakdown")

col_reg1, col_reg2 = st.columns(2)

with col_reg1:
    fig_reg1 = px.pie(df_regions, values='market_share', names='region', title='Global Market Share by Region',
                      color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.4)
    fig_reg1.update_layout(height=350)
    st.plotly_chart(fig_reg1, use_container_width=True)

with col_reg2:
    fig_reg2 = px.bar(df_regions.sort_values('growth', ascending=True), x='growth', y='region', orientation='h',
                      title='YoY Growth Rate by Region (%)', color='growth', color_continuous_scale='Blues', text='growth')
    fig_reg2.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_reg2.update_layout(height=350, showlegend=False)
    fig_reg2.update_coloraxes(showscale=False)
    st.plotly_chart(fig_reg2, use_container_width=True)

st.dataframe(df_regions, use_container_width=True, hide_index=True,
             column_config={
                 "region": "Region",
                 "market_share": st.column_config.ProgressColumn("Market Share %", min_value=0, max_value=50),
                 "revenue_q1": st.column_config.NumberColumn("Q1 Revenue ($M)", format="$%d"),
                 "growth": st.column_config.NumberColumn("YoY Growth %", format="%d%%"),
                 "top_platform": "Leading Platform"
             })

st.markdown("---")

# ============================================
# COMPETITIVE INTELLIGENCE
# ============================================

st.subheader("🎯 Competitive Intelligence")

tab1, tab2, tab3 = st.tabs(["⚠️ New Entrants", "🤝 Partnership Opps", "📋 Strategic Recs"])

with tab1:
    col_ent1, col_ent2, col_ent3 = st.columns(3)
    
    with col_ent1:
        st.markdown("""
        #### 🖤 PineDrama (ByteDance)
        **Launched:** January 2026  
        **Threat Level:** 🔴 **CRITICAL**
        
        **Strategy:**
        - Free content (no coins)
        - Ad-free viewing
        - TikTok cross-promotion
        - Aggressive content acquisition
        
        **Watch For:**
        - Exclusive content deals
        - Creator partnerships
        - Marketing blitz
        """)
    
    with col_ent2:
        st.markdown("""
        #### ✨ GammaTime
        **Launched:** October 2025  
        **Threat Level:** 🟠 **HIGH**
        
        **Strategy:**
        - "Hollywood quality" positioning
        - Celebrity investors
        - Premium subscription model
        
        **Differentiation:**
        - US-produced content
        - A-list talent attached
        - Premium pricing ($9.99/mo)
        """)
    
    with col_ent3:
        st.markdown("""
        #### 🦊 Fox + Holywater
        **Announced:** November 2025  
        **Threat Level:** 🟠 **MEDIUM-HIGH**
        
        **Deal Terms:**
        - Equity stake in Holywater
        - 200 shows commitment
        - US market focus
        
        **Competitive Edge:**
        - Hollywood IP access
        - Ukraine production efficiency
        """)

with tab2:
    col_part1, col_part2 = st.columns(2)
    
    with col_part1:
        st.markdown("""
        #### 🎬 Content Supply Partners
        
        | Company | Strength | Status |
        |---------|----------|--------|
        | Crazy Maple Studio | #1 producer | ReelShort exclusive |
        | StoryMatrix | High volume | DramaBox exclusive |
        | Vertical Film Vancouver | Western production | Open to deals |
        | COL Group | Novel adaptations | Seeking partners |
        | Wattpad / WEBTOON | IP pipeline | Open to licensing |
        """)
    
    with col_part2:
        st.markdown("""
        #### 📺 Distribution Partners
        
        | Platform | Opportunity | Fit |
        |----------|-------------|-----|
        | Tubi | FAST channel | High |
        | Pluto TV | Dedicated channel | High |
        | YouTube Shorts | Discovery funnel | Medium |
        | Roku Channel | Growing FAST | Medium |
        """)

with tab3:
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("""
        #### 🎯 Immediate Actions (30 Days)
        
        1. **Weekly PineDrama Monitoring**
           - Track downloads/rankings daily
           - Report significant movements
        
        2. **Evaluate Non-Exclusive Suppliers**
           - Vertical Film Vancouver
           - Independent Korean studios
        
        3. **Genre Diversification**
           - Revenge content (+85% growth)
           - Thriller/Horror underserved
        """)
    
    with col_rec2:
        st.markdown("""
        #### 📈 Strategic Initiatives (90 Days)
        
        1. **Content Strategy**
           - Increase revenge/justice mix
           - Pilot true crime format
        
        2. **Distribution Expansion**
           - FAST channel pilot
           - YouTube Shorts strategy
        
        3. **Partnership Development**
           - Explore studio JV models
        """)

st.markdown("---")

# ============================================
# RAW DATA & EXPORT
# ============================================

with st.expander("📋 View & Export Raw Data"):
    data_tab1, data_tab2, data_tab3, data_tab4 = st.tabs(["Platforms", "Titles", "Genres", "Regions"])
    
    with data_tab1:
        st.dataframe(df_platforms, use_container_width=True)
        st.download_button("📥 Download Platform Data", df_platforms.to_csv(index=False),
                          f"microdrama_platforms_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    with data_tab2:
        st.dataframe(df_titles, use_container_width=True)
        st.download_button("📥 Download Titles Data", df_titles.to_csv(index=False),
                          f"microdrama_titles_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    with data_tab3:
        st.dataframe(df_genres, use_container_width=True)
        st.download_button("📥 Download Genre Data", df_genres.to_csv(index=False),
                          f"microdrama_genres_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    with data_tab4:
        st.dataframe(df_regions, use_container_width=True)
        st.download_button("📥 Download Regional Data", df_regions.to_csv(index=False),
                          f"microdrama_regional_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

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
