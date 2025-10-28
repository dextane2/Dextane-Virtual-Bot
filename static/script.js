// Time display (Lagos)
function updateTime() {
  const now = new Date();
  const options = { timeZone: 'Africa/Lagos', hour12: false };
  const timeString = now.toLocaleTimeString('en-GB', options);
  document.getElementById('lagosTime').textContent = timeString;
}
setInterval(updateTime, 1000);
updateTime();

// Countdown simulation
let countdown = 5;
setInterval(() => {
  countdown--;
  if (countdown <= 0) countdown = 5;
  document.getElementById('countdown').textContent = countdown + 's';
}, 1000);

// Predictions switching logic
const predictionTitle = document.getElementById('predictionTitle');
const predictionCards = document.getElementById('predictionCards');
const nextBtn = document.getElementById('nextBtn');
const prevBtn = document.getElementById('prevBtn');

let currentSet = 0;
const predictions = [
  {
    title: 'Over 1.5 Predictions',
    matches: [
      'BOU vs EVE - Over 1.5',
      'FUL vs BRE - Over 1.5',
      'LEI vs LEE - Over 1.5'
    ]
  },
  {
    title: 'Under 2.5 Predictions',
    matches: [
      'LIV vs BHA - Under 2.5',
      'ARS vs CHE - Under 2.5'
    ]
  }
];

function renderPredictions(index) {
  const set = predictions[index];
  predictionTitle.textContent = set.title;
  predictionCards.innerHTML = set.matches
    .map(match => `<div class="card">${match}</div>`)
    .join('');
}

nextBtn.addEventListener('click', () => {
  currentSet = (currentSet + 1) % predictions.length;
  renderPredictions(currentSet);
});

prevBtn.addEventListener('click', () => {
  currentSet = (currentSet - 1 + predictions.length) % predictions.length;
  renderPredictions(currentSet);
});
