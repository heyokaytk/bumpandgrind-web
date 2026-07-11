# Hero Countdown to Next Patio Party Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a live countdown to the July 26, 2026 3:00 PM Patio Party in the hero section of `index.html`, and fix the stale July 19 event card to read July 26.

**Architecture:** Single-file static site (`index.html`, no build step). All changes are additive edits to the existing `<style>` block, hero markup, one event card, and the existing bottom `<script>` block — following the file's established patterns (CSS custom properties, `clamp()` for responsive sizing, plain IIFEs for behavior).

**Tech Stack:** Plain HTML/CSS/JS, no framework, no build tooling, no package.json.

## Global Constraints

- Countdown target is a fixed date: `2026-07-26T15:00:00-03:00` (Atlantic Time, explicit UTC offset so it's timezone-correct for any visitor) — copied verbatim from the spec.
- No new build tooling, no package.json, no test framework — this repo has none today and the task doesn't warrant introducing one.
- Visual style must reuse existing tokens only: `var(--white)`, `var(--blush)`, `var(--blush-deep)`, `var(--sans)`, `var(--display)`, and the hero's existing `text-shadow: 0 4px 40px rgba(0,0,0,0.5)` convention.
- Responsive sizing uses `clamp()` inline in the base rule, matching how every other hero element already handles mobile (no separate breakpoint override needed for the countdown itself).

---

### Task 1: Fix stale event card date (July 19 → July 26)

**Files:**
- Modify: `index.html:823-837`

**Interfaces:** None (isolated markup edit).

- [ ] **Step 1: Update the event card**

In `index.html`, find:

```html
    <!-- JULY 19 — COMING SOON -->
    <div class="event-card reveal">
      <div class="event-date-block">
        <div class="event-month">Jul</div>
        <div class="event-day">19</div>
        <div class="event-month">Sun</div>
      </div>
```

Replace with:

```html
    <!-- JULY 26 — COMING SOON -->
    <div class="event-card reveal">
      <div class="event-date-block">
        <div class="event-month">Jul</div>
        <div class="event-day">26</div>
        <div class="event-month">Sun</div>
      </div>
```

- [ ] **Step 2: Verify in browser**

Open `index.html` directly in a browser (double-click or `open index.html` on macOS). Scroll to "Upcoming Events" and confirm the third card now reads "JUL 26 SUN" instead of "JUL 19 SUN".

- [ ] **Step 3: Commit**

```bash
cd "/Users/okaytk/Documents/GITHUB/BUMPANDGRIND-WEB"
git add index.html
git commit -m "Fix stale event card date: July 19 to July 26"
```

---

### Task 2: Add static hero countdown markup and CSS

**Files:**
- Modify: `index.html` (CSS in the `<style>` block, HTML in `#hero`)

**Interfaces:**
- Produces: DOM elements `#heroCountdown`, `#cdDays`, `#cdHours`, `#cdMinutes`, `#cdSeconds` — Task 3's JS reads/writes these by ID.
- Produces: CSS classes `.hero-countdown`, `.hero-countdown-label`, `.hero-countdown-units`, `.countdown-unit`, `.countdown-num`, `.countdown-unit-label`, `.countdown-colon`, `.hero-countdown-message` — Task 3's JS references `.hero-countdown-message` when swapping content on expiry.

- [ ] **Step 1: Add the countdown CSS**

In `index.html`, find this existing block (right after `.hero-logo`'s second declaration, before `.hero-cta-row`):

```css
  .hero-logo {
    position: relative;
    z-index: 2;
  }
  .hero-cta-row {
```

Replace with:

```css
  .hero-logo {
    position: relative;
    z-index: 2;
  }
  .hero-countdown {
    position: relative;
    z-index: 2;
    margin-bottom: 32px;
    animation: fadeUp 0.9s 0.25s ease both;
  }
  .hero-countdown-label {
    font-family: var(--sans);
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--white);
    text-shadow: 0 4px 40px rgba(0,0,0,0.5);
    margin-bottom: 16px;
  }
  .hero-countdown-units {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    gap: 14px;
    flex-wrap: wrap;
  }
  .countdown-unit {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 48px;
  }
  .countdown-num {
    font-family: var(--display);
    font-size: clamp(32px, 6vw, 56px);
    line-height: 1;
    color: var(--white);
    text-shadow: 0 4px 40px rgba(0,0,0,0.5);
  }
  .countdown-unit-label {
    font-family: var(--sans);
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--blush-deep);
    margin-top: 6px;
  }
  .countdown-colon {
    font-family: var(--display);
    font-size: clamp(32px, 6vw, 56px);
    line-height: 1;
    color: var(--blush);
    margin-top: -4px;
  }
  .hero-countdown-message {
    font-family: var(--sans);
    font-size: 15px;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--white);
    text-shadow: 0 4px 40px rgba(0,0,0,0.5);
  }
  .hero-cta-row {
```

- [ ] **Step 2: Add the countdown markup to the hero**

In `index.html`, find:

```html
  <p class="hero-eyebrow">Est. 2016</p>
  <div class="hero-cta-row">
```

Replace with:

```html
  <p class="hero-eyebrow">Est. 2016</p>
  <div class="hero-countdown" id="heroCountdown">
    <p class="hero-countdown-label">Next Patio Party In</p>
    <div class="hero-countdown-units">
      <div class="countdown-unit">
        <span class="countdown-num" id="cdDays">00</span>
        <span class="countdown-unit-label">Days</span>
      </div>
      <span class="countdown-colon">:</span>
      <div class="countdown-unit">
        <span class="countdown-num" id="cdHours">00</span>
        <span class="countdown-unit-label">Hours</span>
      </div>
      <span class="countdown-colon">:</span>
      <div class="countdown-unit">
        <span class="countdown-num" id="cdMinutes">00</span>
        <span class="countdown-unit-label">Minutes</span>
      </div>
      <span class="countdown-colon">:</span>
      <div class="countdown-unit">
        <span class="countdown-num" id="cdSeconds">00</span>
        <span class="countdown-unit-label">Seconds</span>
      </div>
    </div>
  </div>
  <div class="hero-cta-row">
```

- [ ] **Step 3: Verify in browser**

Open `index.html` in a browser. Confirm:
- A row reading "NEXT PATIO PARTY IN" appears above the two hero buttons, showing static `00 : 00 : 00 : 00` with "Days/Hours/Minutes/Seconds" labels underneath each number.
- Numerals are legible (white with shadow) against the hero photo, colons are in the blush accent color.
- Resize the browser to a narrow (mobile) width — the row should shrink smoothly via `clamp()` and wrap without overlapping the buttons below it.

- [ ] **Step 4: Commit**

```bash
cd "/Users/okaytk/Documents/GITHUB/BUMPANDGRIND-WEB"
git add index.html
git commit -m "Add static hero countdown markup and styling"
```

---

### Task 3: Wire up live countdown logic and expiry message

**Files:**
- Modify: `index.html` (bottom `<script>` block, after the existing "Burger menu toggle" IIFE and before the `window.formspree` lines, i.e. around `index.html:1158-1160`)
- Scratch (not committed): a temporary Node script in the scratchpad directory to verify the pure date-math function before wiring it into the DOM

**Interfaces:**
- Consumes: `#heroCountdown`, `#cdDays`, `#cdHours`, `#cdMinutes`, `#cdSeconds` (from Task 2), and CSS class `.hero-countdown-message` (from Task 2) for the expiry swap.
- Produces: nothing consumed by later tasks — this is the last task.

- [ ] **Step 1: Write and run a scratch test for the pure date-math function**

Create a temporary file (do not add this to the repo) at
`/private/tmp/claude-501/-Users-okaytk-Documents-CLAUDE/ca01bada-bc2e-40bb-98b4-f0dc8162d56a/scratchpad/countdown-test.js`:

```js
const assert = require('assert');

function getCountdownParts(targetMs, nowMs) {
  const diff = targetMs - nowMs;
  if (diff <= 0) return null;
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
  const minutes = Math.floor((diff / (1000 * 60)) % 60);
  const seconds = Math.floor((diff / 1000) % 60);
  return { days, hours, minutes, seconds };
}

// 1 day, 2 hours, 3 minutes, 4 seconds remaining
const now = Date.parse('2026-07-25T00:00:00-03:00');
const target = Date.parse('2026-07-26T02:03:04-03:00');
assert.deepStrictEqual(getCountdownParts(target, now), { days: 1, hours: 2, minutes: 3, seconds: 4 });

// target already passed returns null
assert.strictEqual(getCountdownParts(now - 1000, now), null);

// exactly at target returns null (not a fractional-negative day count)
assert.strictEqual(getCountdownParts(now, now), null);

console.log('all pass');
```

Run: `node /private/tmp/claude-501/-Users-okaytk-Documents-CLAUDE/ca01bada-bc2e-40bb-98b4-f0dc8162d56a/scratchpad/countdown-test.js`

Expected: FAIL first if you run it before the function is written correctly — since the function is written inline above, instead deliberately break it first (e.g. change `<= 0` to `< 0`) to confirm the "exactly at target" assertion fails, then restore it.

- [ ] **Step 2: Restore the correct function and confirm the scratch test passes**

Run: `node /private/tmp/claude-501/-Users-okaytk-Documents-CLAUDE/ca01bada-bc2e-40bb-98b4-f0dc8162d56a/scratchpad/countdown-test.js`

Expected output: `all pass`

- [ ] **Step 3: Add the countdown wiring to the site's script block**

In `index.html`, find:

```html
    links.querySelectorAll('a').forEach(function(a) {
      a.addEventListener('click', closeMenu);
    });
  })();

  window.formspree = window.formspree || function () { (formspree.q = formspree.q || []).push(arguments); };
```

Replace with:

```html
    links.querySelectorAll('a').forEach(function(a) {
      a.addEventListener('click', closeMenu);
    });
  })();

  // Hero countdown to next Patio Party
  (function() {
    var target = new Date('2026-07-26T15:00:00-03:00').getTime();
    var container = document.getElementById('heroCountdown');
    var els = {
      days: document.getElementById('cdDays'),
      hours: document.getElementById('cdHours'),
      minutes: document.getElementById('cdMinutes'),
      seconds: document.getElementById('cdSeconds')
    };

    function getCountdownParts(targetMs, nowMs) {
      var diff = targetMs - nowMs;
      if (diff <= 0) return null;
      var days = Math.floor(diff / (1000 * 60 * 60 * 24));
      var hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
      var minutes = Math.floor((diff / (1000 * 60)) % 60);
      var seconds = Math.floor((diff / 1000) % 60);
      return { days: days, hours: hours, minutes: minutes, seconds: seconds };
    }

    function pad(n) {
      return String(n).padStart(2, '0');
    }

    var timer;
    function tick() {
      var parts = getCountdownParts(target, Date.now());
      if (!parts) {
        clearInterval(timer);
        container.innerHTML = '<p class="hero-countdown-message">See You On The Patio! 🎉</p>';
        return;
      }
      els.days.textContent = pad(parts.days);
      els.hours.textContent = pad(parts.hours);
      els.minutes.textContent = pad(parts.minutes);
      els.seconds.textContent = pad(parts.seconds);
    }

    tick();
    timer = setInterval(tick, 1000);
  })();

  window.formspree = window.formspree || function () { (formspree.q = formspree.q || []).push(arguments); };
```

- [ ] **Step 4: Verify live ticking in browser**

Open `index.html` in a browser. Confirm the countdown numbers show a real (non-zero) days count and the seconds unit visibly decrements once per second. Reload the page — the numbers should recompute correctly on load.

- [ ] **Step 5: Verify the expiry swap**

Temporarily edit the `target` line to a past timestamp, e.g.:

```js
var target = new Date('2020-01-01T00:00:00-03:00').getTime();
```

Reload `index.html` in the browser and confirm the countdown row is replaced with "SEE YOU ON THE PATIO! 🎉" styled consistently with the rest of the hero (white, uppercase, letter-spaced, legible against the photo). Then revert the line back to:

```js
var target = new Date('2026-07-26T15:00:00-03:00').getTime();
```

- [ ] **Step 6: Delete the scratch test file**

```bash
rm /private/tmp/claude-501/-Users-okaytk-Documents-CLAUDE/ca01bada-bc2e-40bb-98b4-f0dc8162d56a/scratchpad/countdown-test.js
```

- [ ] **Step 7: Commit**

```bash
cd "/Users/okaytk/Documents/GITHUB/BUMPANDGRIND-WEB"
git add index.html
git commit -m "Add live countdown logic and patio-party-day message swap"
```

---

## Final Verification

- [ ] Open `index.html` fresh in a browser and confirm, top to bottom of the hero: logo/eyebrows → live-ticking countdown → CTA buttons, with no layout shift or overlap.
- [ ] Confirm the Upcoming Events section's third card now reads July 26.
- [ ] Confirm mobile width (resize to ~375px) still looks clean.
- [ ] Confirm `git log --oneline -5` shows the three commits from this plan.
