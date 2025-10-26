// script.js — countdown, Lagos clock, swipe, AJAX refresh

// ---- Lagos clock (uses browser timezone with Africa/Lagos)
function updateLagosTime() {
  const el = document.getElementById("lagos-time");
  if (!el) return;
  const now = new Date();
  const opts = { timeZone: "Africa/Lagos", hour12: false, hour:"2-digit", minute:"2-digit", second:"2-digit" };
  el.textContent = now.toLocaleTimeString("en-GB", opts);
}
setInterval(updateLagosTime, 1000);
updateLagosTime();

// ---- menu toggle
const menuToggle = document.getElementById("menu-toggle");
const menuDropdown = document.getElementById("menu-dropdown");
if (menuToggle){
  menuToggle.addEventListener("click", ()=> {
    menuDropdown.style.display = menuDropdown.style.display === "flex" ? "none" : "flex";
  });
}

// ---- manual scrape button: calls /scrape and updates UI
const scrapeBtn = document.getElementById("scrape-btn");
if (scrapeBtn) {
  scrapeBtn.addEventListener("click", async () => {
    scrapeBtn.textContent = "⏳";
    try {
      const res = await fetch("/scrape");
      const data = await res.json();
      // update lists and last-updated if response OK
      if (data.status === "success") {
        updateFixtures(data.over, data.under, data.timestamp);
        resetCountdown(data.countdown || 120);
      }
    } catch (err) {
      console.error("scrape error", err);
      alert("Scrape failed (demo).");
    }
    scrapeBtn.textContent = "🧠 Scrape Now";
    menuDropdown.style.display = "none";
  });
}

// ---- populate fixtures helper
function updateFixtures(overArr, underArr, timestamp){
  const overList = document.getElementById("over-list");
  const underList = document.getElementById("under-list");
  const lastUpdated = document.getElementById("last-updated");

  if (overList && underList){
    overList.innerHTML = (overArr || []).slice(0,3).map(i => `<li>${i}</li>`).join("");
    underList.innerHTML = (underArr || []).slice(0,2).map(i => `<li>${i}</li>`).join("");
  }
  if (lastUpdated && timestamp) lastUpdated.textContent = timestamp;
}

// ---- auto refresh (AJAX) when countdown reaches zero
let countdown = window.__INITIAL_COUNTDOWN__ || 120;
const display = document.getElementById("countdown-display");

function tick(){
  if (!display) return;
  const m = Math.floor(countdown/60);
  const s = countdown % 60;
  display.textContent = `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
  if (countdown <= 0){
    // fetch new predictions from /api/predictions
    fetch("/api/predictions").then(r => r.json()).then(data => {
      updateFixtures(data.over, data.under, data.timestamp);
      countdown = data.countdown || 120;
    }).catch(err => {
      console.error("Refresh failed", err);
      // reset countdown anyway to try again
      countdown = 120;
    });
  } else {
    countdown--;
  }
}
setInterval(tick, 1000);
tick(); // immediate

// ---- swipe logic (touch)
let startX = null;
const cards = Array.from(document.querySelectorAll(".card"));
let cur = 0;
function showCard(i){
  cards.forEach((c, idx) => {
    c.classList.toggle("card-visible", idx === i);
  });
}
if (cards.length > 0){
  showCard(0);
  const swipeArea = document.getElementById("swipe-wrapper");
  swipeArea.addEventListener("touchstart", (e)=> startX = e.touches[0].clientX);
  swipeArea.addEventListener("touchmove", (e)=>{
    if (startX === null) return;
    const x2 = e.touches[0].clientX;
    const diff = x2 - startX;
    if (Math.abs(diff) > 60){
      // left swipe -> next card
      if (diff < 0) cur = (cur + 1) % cards.length;
      else cur = (cur - 1 + cards.length) % cards.length;
      showCard(cur);
      startX = null;
    }
  });
  swipeArea.addEventListener("touchend", ()=> startX = null);
}
