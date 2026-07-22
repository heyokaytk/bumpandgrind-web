# Bump & Grind Website

## What This Is

Website for Bump & Grind — R&B event series based in Halifax, NS.

Website: bumpandgrindhfx.com (canonical: www.bumpandgrindhfx.com)
Repo: heyokaytk/bumpandgrind-web (GitHub)
Hosting: GitHub Pages (`CNAME` file sets custom domain), fronted by Cloudflare DNS/proxy — same pattern as Golden Service.
Ticketing: Showpass / Bloom Tickets. Newsletter: Beehiiv, but the on-page signup form posts to a Cloudflare Worker, not directly to Beehiiv.

Business context, newsletter drafting, and Instagram captions are handled in the separate `BUMP & GRIND` project folder (`/Users/okaytk/Documents/CLAUDE/PROJECTS/BUMP & GRIND`) — that folder's `index.html` is a **stale, disconnected snapshot**, not this site's source. Always edit here.

---

## Stack

Static HTML (`index.html`), no build step. Additional standalone pages: `seasonpass.html`, `waitlist.html`. JSON-LD Event structured data covers listed patio/Marquee dates.
SEO files: `sitemap.xml`, Google Search Console verification file at root.

After any site change: push to `main` on GitHub (Pages rebuilds automatically). If the change doesn't appear live, purge Cloudflare cache in addition to the push — same as Golden Service.

---

## Pre-Commit / Pre-Push Audit

Before every `git commit` + `git push` on this site, run this audit on the diff being shipped. Act as a Principal Web Developer, UX/UI Expert, and Technical SEO Strategist. Give a rigorous, customized audit based on the actual code, copy, and architecture changed — not generic advice.

Audit across four pillars:

1. **UX/UI & Conversion Flow** — Does the change help or hurt the path to the primary CTA (ticket purchase / newsletter signup)? Any new friction points that could cause drop-off? Mobile responsiveness impact?
2. **Technical Architecture & Performance** — Is the code efficient? Any rendering roadblocks, bloated scripts, or structural issues introduced? Single-file static HTML on GitHub Pages — watch asset weight (photos, mix cover art) and whether JSON-LD stays valid after copy/date changes.
3. **Technical & On-Page SEO** — Metadata, header hierarchy (H1/H2/H3), alt text — still optimized for target search intent after this change? Confirm Event structured data (dates, venue, ticket link, price) and the www canonical tag aren't broken by the change.
4. **Actionable Roadmap** — Prioritized checklist: Critical (fix before this push), High Impact (this week), Long-Term (this month).

Primary Goal: Convert visitors into ticket sales and newsletter subscribers.
Target Audience: R&B fans in Halifax attending day parties and night events.
Tech Stack Context: Static HTML on GitHub Pages, custom domain via Cloudflare DNS/proxy. No CI build step — what's pushed to `main` is what ships.

Scope the audit to the actual diff unless the change touches enough of the page to warrant a full-page pass. Present findings as a punch list. Don't block the commit — flag issues and let TK decide what to fix now vs. later.
