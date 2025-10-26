// Dropdown toggle
const menuBtn = document.getElementById("menuBtn");
const dropdown = document.getElementById("dropdown");
menuBtn.addEventListener("click", () => dropdown.classList.toggle("hidden"));

// Arrow navigation
const cardWrapper = document.querySelector(".card-wrapper");
document.getElementById("nextBtn").addEventListener("click", () => {
  cardWrapper.scrollBy({ left: 320, behavior: "smooth" });
});
document.getElementById("prevBtn").addEventListener("click", () => {
  cardWrapper.scrollBy({ left: -320, behavior: "smooth" });
});

// Lagos time live clock
function updateClocks() {
  const now = new Date().toLocaleString("en-NG", { timeZone: "Africa/Lagos" });
  const time = new Date(now).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  document.getElementById("clock1").textContent = `🕒 ${time}`;
  document.getElementById("clock2").textContent = `🕒 ${time}`;
}
setInterval(updateClocks, 1000);
updateClocks();

// Yellow countdown for 2 minutes
function startCountdown(duration, display1, display2) {
  let timer = duration;
  setInterval(() => {
    const minutes = String(Math.floor(timer / 60)).padStart(2, "0");
    const seconds = String(timer % 60).padStart(2, "0");
    display1.textContent = `⏳ ${minutes}:${seconds}`;
    display2.textContent = `⏳ ${minutes}:${seconds}`;
    if (--timer < 0) timer = duration; // auto restart
  }, 1000);
}

const countdownDuration = 120; // 2 minutes
const display1 = document.getElementById("countdown1");
const display2 = document.getElementById("countdown2");
startCountdown(countdownDuration, display1, display2);
