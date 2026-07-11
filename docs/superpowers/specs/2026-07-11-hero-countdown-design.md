# Hero Countdown to Next Patio Party

## Problem

The site has no visible urgency signal for the next Patio Party. The Upcoming
Events list also has a stale date: it shows "July 19" as the next
"Coming Soon" event, but the actual next Patio Party is **Sunday, July 26,
2026, 3:00 PM** (Atlantic Time) at The Pint Patio.

## Goals

- Add a live countdown to the July 26 Patio Party, placed in the hero section.
- Fix the July 19 event card in Upcoming Events to read July 26.
- Keep the visual language consistent with the existing site theme (Bebas
  Neue numerals, Outfit for labels, blush-deep accent, hero-eyebrow styling).

## Non-goals

- Not touching the stale May 17 ("on sale / 75% sold") or June 21
  (waitlist) content — those are past-dated but out of scope for this task.
- Not adding a CMS/config for the target date — it's a single hardcoded
  event, hardcoding the date in JS is fine.

## Design

### Placement

Inserted into `#hero` (`index.html`), between the last `.hero-eyebrow`
("Est. 2016") and `.hero-cta-row`. New markup block, e.g.:

```html
<div class="hero-countdown" id="heroCountdown">
  <p class="hero-countdown-label">Next Patio Party In</p>
  <div class="hero-countdown-units">
    <div class="countdown-unit"><span class="countdown-num" id="cdDays">00</span><span class="countdown-unit-label">Days</span></div>
    <span class="countdown-colon">:</span>
    <div class="countdown-unit"><span class="countdown-num" id="cdHours">00</span><span class="countdown-unit-label">Hours</span></div>
    <span class="countdown-colon">:</span>
    <div class="countdown-unit"><span class="countdown-num" id="cdMinutes">00</span><span class="countdown-unit-label">Minutes</span></div>
    <span class="countdown-colon">:</span>
    <div class="countdown-unit"><span class="countdown-num" id="cdSeconds">00</span><span class="countdown-unit-label">Seconds</span></div>
  </div>
</div>
```

### Visual style

- `.hero-countdown-label`: same treatment as `.hero-eyebrow` (Outfit,
  15px, 500 weight, 0.3em letter-spacing, uppercase, white, same
  text-shadow), smaller bottom margin than the eyebrows above it.
- `.countdown-num`: Bebas Neue, large (clamp between ~40px and ~64px),
  white, same `text-shadow: 0 4px 40px rgba(0,0,0,0.5)` used elsewhere in
  hero so it reads against the photo.
- `.countdown-unit-label`: Outfit, ~10px, uppercase, 0.15em letter-spacing,
  blush-deep (`var(--blush-deep)`).
- `.countdown-colon`: Bebas Neue, same size as `.countdown-num`, blush
  (`var(--blush)`) color, small negative top margin to visually align with
  the numerals rather than the unit labels.
- Row uses flexbox, centered, `gap` between units, `flex-wrap: wrap` so it
  never breaks the hero layout on narrow screens.
- Mobile (`max-width: 768px`): reduce `.countdown-num` font-size and gap
  via the existing mobile media query block, consistent with how other
  hero elements shrink.
- Whole block gets the existing `fadeUp` entrance animation (same pattern
  as `.hero-tagline` / `.hero-cta-row`), sequenced after the eyebrows and
  before the CTA row.

### Behavior (JS)

- Fixed target: `new Date("2026-07-26T15:00:00-03:00")` (Atlantic Time,
  explicit offset so it's correct regardless of visitor's own timezone).
- On `DOMContentLoaded`, run an update function immediately, then every
  1000ms via `setInterval`.
- Update function: compute `target - now`. If `> 0`, derive days/hours/
  minutes/seconds and write them into the four `#cd*` spans, zero-padded
  to 2 digits (days can exceed 2 digits naturally, no padding needed
  there beyond 2).
- When `target - now <= 0`: clear the interval and replace
  `#heroCountdown`'s innerHTML with a single centered message reusing the
  `.hero-countdown-label`-equivalent styling, e.g. "See You On The
  Patio! 🎉" — no negative numbers ever shown.
- Script is a small inline `<script>` at the bottom of `<body>`, matching
  the existing pattern used for `loadMix()` and the nav burger / waitlist
  form handling already in the file (no new build tooling).

### Events section fix

In the "JULY 19 — COMING SOON" event card (`index.html:823-837`), update:

- `.event-month` "Jul" → unchanged, `.event-day` "19" → "26".
- Leave the card as "Coming Soon" (no ticket link yet, matching the
  existing pattern for other not-yet-on-sale dates) unless a ticket link
  is provided later.

## Testing / Verification

Static HTML/CSS/JS, no build step. Verify by opening `index.html` directly
in a browser:

1. Countdown renders in the hero, above the CTA buttons, and visually
   matches the theme (numerals legible against the hero photo).
2. Numbers tick down once per second without layout shift.
3. Resize to mobile width — countdown wraps/shrinks without breaking the
   hero.
4. Temporarily point the target date at a past timestamp to confirm the
   "See You On The Patio!" swap renders correctly, then revert to the
   real July 26 date.
5. Confirm the Upcoming Events card now reads July 26 instead of July 19.
