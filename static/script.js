let currentSlide = 0;
const slides = document.querySelectorAll(".card");
const countdownEl = document.getElementById("countdown");

function moveSlide(direction) {
  currentSlide += direction;
  if (currentSlide < 0) currentSlide = slides.length - 1;
  if (currentSlide >= slides.length) currentSlide = 0;
  document.querySelector(".carousel").style.transform = `translateX(-${currentSlide * 100}%)`;
}

function handleMenu(select) {
  const value = select.value;
  if (value === "scrape") window.location.href = "/scrape";
  else if (value === "refresh") location.reload();
  else if (value === "about") alert("Dextane Virtual Bot v1.0\nPowered by SportyBet Scheduled VFL Data");
  select.selectedIndex = 0;
}

// Countdown (2 minutes)
let timeLeft = 120;
function startCountdown() {
  const timer = setInterval(() => {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    countdownEl.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    if (timeLeft <= 0) {
      clearInterval(timer);
      countdownEl.textContent = "Starting soon...";
    }
    timeLeft--;
  }, 1000);
}
startCountdown();
