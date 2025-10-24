import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re

SPORTYBET_VFL_URL = "https://www.sportybet.com/ng/sport/virtuals/football"

async def get_live_vfl_fixtures():
    data = {"over_15": [], "under_25": []}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(SPORTYBET_VFL_URL, timeout=60000)
        await page.wait_for_timeout(4000)
        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, "html.parser")
    
    # Try multiple selector patterns to stay adaptive
    match_blocks = soup.select("div[class*='match']") or soup.select("div[class*='fixture']")
    
    for block in match_blocks:
        text = block.get_text(" ", strip=True)
        teams = re.findall(r"[A-Z][a-zA-Z\s]+ vs [A-Z][a-zA-Z\s]+", text)
        if not teams:
            continue

        match_name = teams[0]
        odds = re.findall(r"\d+\.\d+", text)

        if odds and len(odds) >= 2:
            over = odds[0]
            under = odds[1]
            home, away = match_name.split(" vs ")
            data["over_15"].append({"home": home, "away": away, "prediction": f"Over 1.5 ({over})"})
            data["under_25"].append({"home": home, "away": away, "prediction": f"Under 2.5 ({under})"})
    
    # Limit to top 3 and 2 for dashboard
    data["over_15"] = data["over_15"][:3]
    data["under_25"] = data["under_25"][:2]
    return data
