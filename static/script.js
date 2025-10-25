// Lagos time with pytz logic backend
function updateLagosTime() {
  const now = new Date();
  document.getElementById("lagos-time").textContent =
    now.toLocaleTimeString("en-GB", { hour12: false, timeZone: "Africa/Lagos" });
}
setInterval(updateLagosTime, 1000);
updateLagosTime();

// Countdown for 2 minutes
let countdownTime = 120;
function updateCountdown() {
  const countdown = document.getElementById("countdown");
  const minutes = Math.floor(countdownTime / 60);
  const seconds = countdownTime % 60;
  countdown.textContent = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  countdownTime--;
  if (countdownTime < 0) countdownTime = 120;
}
setInterval(updateCountdown, 1000);

// Swipe logic
let current = 0;
const cards = document.querySelectorAll(".card");
document.addEventListener("touchstart", handleTouchStart, false);
document.addEventListener("touchmove", handleTouchMove, false);
let x1 = null;

function handleTouchStart(e) { x1 = e.touches[0].clientX; }
function handleTouchMove(e) {
  if (!x1) return;
  let x2 = e.touches[0].clientX;
  let diff = x2 - x1;
  if (Math.abs(diff) > 50) {
    cards[current].classList.remove("active");
    current = diff > 0 ? (current - 1 + cards.length) % cards.length : (current + 1) % cards.length;
    cards[current].classList.add("active");
    x1 = null;
  }
}

// Demo predictions (replace later with SportyBet data)
const overPreds = ["BOU vs EVE - Over 1.5", "FUL vs BRE - Over 1.5", "LEI vs LEE - Over 1.5"];
const underPreds = ["MCI vs WOL - Under 2.5", "TOT vs NEW - Under 2.5"];
document.getElementById("over-list").innerHTML = overPreds.map(m => `<li>${m}</li>`).join("");
document.getElementById("under-list").innerHTML = underPreds.map(m => `<li>${m}</li>`).join("");
