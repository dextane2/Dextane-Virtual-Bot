async function load() {
    const res = await fetch('/api/fixtures');
    const data = await res.json();
    const container = document.getElementById('fixtures');
    if (!data || data.length === 0) {
        container.innerHTML = '<p>No fixtures stored yet. Please wait a few minutes for the bot to populate data.</p>';
        return;
    }
    container.innerHTML = data.map(d => `
        <div class="fixture">
            <strong>${d.home_team} vs ${d.away_team}</strong><br>
            Odds — Home: ${d.odd_home||'-'} | Draw: ${d.odd_draw||'-'} | Away: ${d.odd_away||'-'}<br>
            Markets — Over1.5: ${d.over_1_5||'-'} | Under2.5: ${d.under_2_5||'-'}<br>
            <small>${new Date(d.timestamp).toLocaleString()}</small>
        </div>
    `).join('');
}

load();
setInterval(load, 90000); // refresh UI every 90s
