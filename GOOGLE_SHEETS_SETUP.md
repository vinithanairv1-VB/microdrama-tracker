# Google Sheets Setup Guide for Micro-Drama Tracker

This guide shows you how to connect a Google Sheet to your dashboard so you can update data weekly without touching code.

---

## Step 1: Create Your Google Sheet

1. Go to [sheets.google.com](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it: `Micro-Drama Tracker Data`

---

## Step 2: Create 4 Tabs with These Exact Names

Click the `+` at the bottom to add tabs. Name them **exactly**:

- `platforms`
- `titles`
- `genres`
- `regions`

---

## Step 3: Add Column Headers

### Tab: `platforms`

| platform | company | origin | score | installs | revenue_2024 | revenue_q1_2025 | rank_current | rank_last_week | us_share | content_count | monetization | threat_level |
|----------|---------|--------|-------|----------|--------------|-----------------|--------------|----------------|----------|---------------|--------------|--------------|
| ReelShort | Crazy Maple Studio | China | 4.2 | 50000000 | 400 | 180 | 1 | 1 | 55 | 500 | Coins + Subscription | Market Leader |
| DramaBox | StoryMatrix (Tencent) | Singapore | 4.6 | 100000000 | 323 | 145 | 2 | 2 | 30 | 400 | Coins + Ads | Strong Challenger |

*(Copy the full data from your current app.py default data)*

### Tab: `titles`

| title | platform | genre | sub_genre | episodes | revenue_est | views_est | weeks_trending | status |
|-------|----------|-------|-----------|----------|-------------|-----------|----------------|--------|
| The Double Life of My Billionaire Husband | ReelShort | Romance | Billionaire | 92 | 22 | 180M | 12 | 🔥 #1 Overall |

### Tab: `genres`

| genre | market_share | growth_rate | avg_completion |
|-------|--------------|-------------|----------------|
| Romance | 45 | 25 | 78 |
| Revenge | 18 | 85 | 82 |

### Tab: `regions`

| region | market_share | revenue_q1 | growth | top_platform |
|--------|--------------|------------|--------|--------------|
| United States | 49 | 343 | 380 | ReelShort |
| Southeast Asia | 18 | 126 | 450 | DramaBox |

---

## Step 4: Publish Each Tab to Web

For **each tab** (platforms, titles, genres, regions):

1. Go to **File → Share → Publish to web**
2. In the dropdown, select the **specific tab name** (not "Entire Document")
3. In the format dropdown, select **Comma-separated values (.csv)**
4. Click **Publish**
5. Copy the URL that appears

You'll get 4 URLs like:
```
https://docs.google.com/spreadsheets/d/e/2PACX-xxxxx/pub?gid=0&single=true&output=csv
https://docs.google.com/spreadsheets/d/e/2PACX-xxxxx/pub?gid=123456&single=true&output=csv
...
```

---

## Step 5: Add URLs to Your Dashboard

Open `app.py` and find this section near the top:

```python
SHEET_URLS = {
    "platforms": "",  # Paste your platforms tab CSV URL here
    "titles": "",     # Paste your titles tab CSV URL here
    "genres": "",     # Paste your genres tab CSV URL here
    "regions": "",    # Paste your regions tab CSV URL here
}

USE_GOOGLE_SHEETS = False
```

Replace with your URLs and set to True:

```python
SHEET_URLS = {
    "platforms": "https://docs.google.com/spreadsheets/d/e/2PACX-xxxxx/pub?gid=0&single=true&output=csv",
    "titles": "https://docs.google.com/spreadsheets/d/e/2PACX-xxxxx/pub?gid=123456&single=true&output=csv",
    "genres": "https://docs.google.com/spreadsheets/d/e/2PACX-xxxxx/pub?gid=789012&single=true&output=csv",
    "regions": "https://docs.google.com/spreadsheets/d/e/2PACX-xxxxx/pub?gid=345678&single=true&output=csv",
}

USE_GOOGLE_SHEETS = True
```

---

## Step 6: Push to GitHub and Redeploy

```bash
git add .
git commit -m "Connected Google Sheets for live data"
git push
```

Render will auto-redeploy within a few minutes.

---

## Weekly Update Workflow

Every week, your process is now:

1. **Open your Google Sheet**
2. **Update the data** (rankings, revenue, new titles, etc.)
3. **That's it!** Dashboard refreshes automatically within ~5 minutes

No code changes. No git commands. No redeployment.

---

## Tips

- **Backup:** Keep a copy of the previous week's data in a separate tab for historical tracking
- **Rank Changes:** Update `rank_last_week` before changing `rank_current` so the Δ column shows correctly
- **Cache:** If changes don't appear immediately, wait 5 minutes (Google's cache refresh time)
- **Validation:** Test your Sheet URLs directly in a browser to make sure they return CSV data

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Dashboard shows "Using default dataset" | Check that `USE_GOOGLE_SHEETS = True` |
| "Error loading Google Sheets" | Verify your URLs are correct and the sheet is published |
| Data not updating | Wait 5 min for Google's cache, or re-publish the sheet |
| Wrong columns showing | Make sure column headers match exactly (case-sensitive) |

---

## Need Help?

If you run into issues, check:
1. Sheet is published to web (not just shared)
2. URLs end with `output=csv`
3. Column headers match exactly
4. `USE_GOOGLE_SHEETS = True` is set

---

Built by Vinitha Nair | vinithanair.v1@gmail.com
