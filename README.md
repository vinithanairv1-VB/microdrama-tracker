# 🎬 Micro-Drama Market Intelligence Dashboard

A professional-grade market intelligence tool for monitoring the global short-form drama industry (ReelShort, DramaBox, ShortMax, etc.).

![Dashboard Preview](preview.png)

## Features

- **Platform Rankings** — Track 10+ micro-drama apps with weekly rank changes
- **Trending Content** — Monitor top-performing titles by revenue and viewership
- **Genre Analysis** — Market share, growth rates, and completion metrics by genre
- **Regional Breakdown** — Global market data across US, SEA, LATAM, Europe, MENA
- **Competitive Intelligence** — New entrant tracking (PineDrama, GammaTime, Fox/Holywater)
- **Strategic Recommendations** — Partnership opportunities and action items
- **Data Export** — Download CSV files for all datasets

## Live Demo

🔗 **[View Live Dashboard](https://your-app-url.onrender.com)**

## Quick Start

### Run Locally

```bash
# Clone the repo
git clone https://github.com/vinithanairv1-VB/microdrama-tracker.git
cd microdrama-tracker

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

### Deploy to Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) and connect your GitHub
3. Create a new **Web Service**
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Deploy (free tier available)

## Data Sources

- Google Play Store rankings
- App Store rankings  
- Sensor Tower estimates
- Media Partners Asia reports
- Variety, Deadline, The Hollywood Reporter

## Update Schedule

| Data Type | Frequency |
|-----------|-----------|
| App rankings | Weekly |
| Revenue estimates | Monthly |
| Trending titles | Weekly |
| Competitive intel | As available |

## Tech Stack

- **Frontend:** Streamlit
- **Charts:** Plotly
- **Data:** Pandas
- **Hosting:** Render

## Author

**Vinitha Nair**  
📧 vinithanair.v1@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/vinithanair)

## License

MIT License - feel free to use and modify for your own projects.

---

*Built as part of market intelligence efforts in the content acquisitions space.*
