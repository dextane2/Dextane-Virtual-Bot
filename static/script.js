const menuBtn = document.getElementById("menuBtn");
const dropdown = document.getElementById("dropdown");
menuBtn.addEventListener("click", () => {
  dropdown.classList.toggle("hidden");
});

const cardWrapper = document.querySelector(".card-wrapper");
document.getElementById("nextBtn").addEventListener("click", () => {
  cardWrapper.scrollBy({ left: 320, behavior: "smooth" });
});
document.getElementById("prevBtn").addEventListener("click", () => {
  cardWrapper.scrollBy({ left: -320, behavior: "smooth" });
});

// Live blue digital clock on both cards
function updateClocks() {
  const now = new Date();
  const time = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  document.getElementById("clock1").textContent = `🕒 ${time}`;
  document.getElementById("clock2").textContent = `🕒 ${time}`;
}
setInterval(updateClocks, 1000);
updateClocks();
