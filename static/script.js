// ---------- Configuration ----------
const ROUND_SECONDS = 180; // 3 minutes per round
const MAX_WEEKS = 38;

// initial week start (simulation start)
let currentWeek = 1;

// Predictions dataset (example - adapt as needed)
const predictions = [
  {
    title: 'Over 1.5 Predictions',
    items: [
      'BOU vs EVE - Over 1.5',
      'FUL vs BRE - Over 1.5',
      'LEI vs LEE - Over 1.5'
    ]
  },
  {
    title: 'Under 2.5 Predictions',
    items: [
      'LIV vs BHA - Under 2.5',
      'ARS vs CHE - Under 2.5'
    ]
  }
];

// ---------- DOM refs ----------
const countdownEl = document.getElementById('countdown');
const weekEl = document.getElementById('week');
const cardFrame = document.getElementById('cardFrame');
const nextBtn = document.getElementById('nextBtn');
const prevBtn = document.getElementById('prevBtn');

let currentIndex = 0; // which predictions set shown
let remaining = ROUND_SECONDS; // seconds left in current round
let countdownInterval = null;
let animating = false;

// ---------- helpers ----------
function formatTime(s){
  const mm = String(Math.floor(s/60)).padStart(2,'0');
  const ss = String(s % 60).padStart(2,'0');
  return `${mm}:${ss}`;
}

function updateCountdownDisplay(){
  countdownEl.textContent = formatTime(remaining);
}

// When a round completes: increment week and reset timer
function onRoundComplete(){
  // increment week (loop 1..MAX_WEEKS)
  currentWeek = (currentWeek % MAX_WEEKS) + 1;
  weekEl.textContent = `Week ${currentWeek} of ${MAX_WEEKS}`;
  // reset timer
  remaining = ROUND_SECONDS;
  updateCountdownDisplay();
}

// start the repeating countdown
function startCountdown(){
  // show initial week
  weekEl.textContent = `Week ${currentWeek} of ${MAX_WEEKS}`;
  updateCountdownDisplay();

  // clear any existing
  if (countdownInterval) clearInterval(countdownInterval);

  countdownInterval = setInterval(() => {
    remaining--;
    if (remaining <= 0){
      // round finished -> simulate round completion
      onRoundComplete();
    } else {
      updateCountdownDisplay();
    }
  }, 1000);
}

// ---------- render card (single view) ----------
function makeCardElement(set){
  const wrap = document.createElement('div');
  wrap.className = 'card-content';
  // title
  const h = document.createElement('div');
  h.className = 'card-title';
  h.textContent = set.title;
  wrap.appendChild(h);

  // entries
  const ul = document.createElement('ul');
  ul.className = 'entry-list';
  set.items.forEach(it => {
    const li = document.createElement('li');
    li.textContent = it;
    ul.appendChild(li);
  });
  wrap.appendChild(ul);

  return wrap;
}

// show current index with optional direction for slide
function showIndex(nextIndex, direction = 'right'){
  if (animating) return;
  if (nextIndex === currentIndex) return;

  const fromEl = cardFrame.querySelector('.card-content');
  const nextSet = predictions[nextIndex];
  const nextEl = makeCardElement(nextSet);

  // apply entry animation classes
  if (!fromEl){
    // first render, just show
    cardFrame.innerHTML = '';
    cardFrame.appendChild(nextEl);
    currentIndex = nextIndex;
    return;
  }

  animating = true;
  // outgoing animation
  if (direction === 'right'){
    fromEl.classList.add('slide-out-left');
    nextEl.classList.add('slide-in-right');
  } else {
    fromEl.classList.add('slide-out-right');
    nextEl.classList.add('slide-in-left');
  }

  // place next element into DOM (above/outside)
  cardFrame.appendChild(nextEl);

  // wait for animation end (~420ms)
  setTimeout(() => {
    // remove old
    if (fromEl && fromEl.parentElement) fromEl.parentElement.removeChild(fromEl);
    // clean classes on nextEl
    nextEl.classList.remove('slide-in-right','slide-in-left');
    animating = false;
    currentIndex = nextIndex;
  }, 460); // slightly longer than css animation
}

// initial render
function initialRender(){
  cardFrame.innerHTML = '';
  const el = makeCardElement(predictions[currentIndex]);
  cardFrame.appendChild(el);
}

// arrow handlers
nextBtn.addEventListener('click', () => {
  const nextI = (currentIndex + 1) % predictions.length;
  showIndex(nextI, 'right');
});
prevBtn.addEventListener('click', () => {
  const nextI = (currentIndex - 1 + predictions.length) % predictions.length;
  showIndex(nextI, 'left');
});

// keyboard left/right arrows
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight') nextBtn.click();
  if (e.key === 'ArrowLeft') prevBtn.click();
});

// touch swipe support for mobile (optional)
let touchStartX = null;
cardFrame.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; });
cardFrame.addEventListener('touchend', (e) => {
  if (touchStartX === null) return;
  const diff = e.changedTouches[0].clientX - touchStartX;
  if (Math.abs(diff) > 40){
    if (diff < 0) nextBtn.click(); else prevBtn.click();
  }
  touchStartX = null;
});

// initialize page
initialRender();
startCountdown();

// ensure countdown display updates every second (even while animating)
updateCountdownDisplay();
