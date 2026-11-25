// NYE ticket count: update `sold` as tickets sell.
// Read by every [data-meter] bar (homepage events row, /nye/, /seasonpass)
// and the homepage hero line.
window.NYE_SALES = { sold: 17, capacity: 100, passes: 50 };

// Sales meters. While season passes remain (first 50 sold), they count those
// down; after that they count tickets left of 100.
(function () {
  function render() {
    var s = window.NYE_SALES, sold = s.sold;
    var passPhase = sold < s.passes;
    var total = passPhase ? s.passes : s.capacity;
    var left = Math.max(total - sold, 0);
    var pct = Math.min(sold / total * 100, 100);
    var text = left === 0 ? 'Sold out'
      : passPhase ? 'of 50 free season passes left'
      : (left === 1 ? 'ticket left' : 'tickets left');
    var sub = passPhase ? 'First 50 buyers only' : 'No door sales';
    document.querySelectorAll('[data-meter]').forEach(function (m) {
      m.querySelector('[data-meter-left]').textContent = left === 0 ? '' : left;
      m.querySelector('[data-meter-text]').textContent = text;
      m.querySelector('[data-meter-sub]').textContent = sub;
      var bar = m.querySelector('[data-meter-bar]');
      bar.setAttribute('aria-valuemax', total);
      bar.setAttribute('aria-valuenow', sold);
      bar.setAttribute('aria-label', (left ? left + ' ' : '') + text);
      m.hidden = false;
      requestAnimationFrame(function () {
        requestAnimationFrame(function () { bar.firstElementChild.style.width = pct + '%'; });
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render);
  else render();
})();
