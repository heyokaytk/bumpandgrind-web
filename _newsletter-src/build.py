#!/usr/bin/env python3
"""Build the web versions of the newsletter from issues.json.

Writes newsletter/index.html and newsletter/<slug>/index.html, and refreshes the
"latest issue" link on the homepage and the newsletter URLs in sitemap.xml
(both between NEWSLETTER markers).

Also builds Rewind: every R&B Rewind and On This Day section becomes its own
page at rewind/<slug>/, plus rewind/index.html, the homepage Rewind strip and
the Rewind URLs in sitemap.xml (between REWIND markers). Run from anywhere:

    python3 _newsletter-src/build.py
"""
import html
import json
import re
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.bumpandgrindhfx.com"
SRC = json.loads((Path(__file__).parent / "issues.json").read_text())
ISSUES = SRC["issues"]
UP_NEXT = SRC.get("up_next")

KINDS = {
    "rewind": ("⏪️", "R&amp;B Rewind"),
    "radar": ("📡", "R&amp;B Radar"),
    "otd": ("🗓️", "On This Day"),
    "thisorthat": ("🤔", "This or That"),
}


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def attr(s):
    return html.escape(strip_tags(s), quote=True)


def nice_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


PIXEL = """<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '1478717332720361');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=1478717332720361&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->"""

CSS = """
  .hero-giant {
    font-family: var(--display-fat); font-weight: 400;
    font-size: clamp(44px, 9vw, 104px); line-height: 0.9; letter-spacing: -0.01em;
    text-transform: uppercase; color: var(--white); text-shadow: 0 2px 30px rgba(0,0,0,0.35);
  }
  .nl-headline {
    font-family: var(--display); font-weight: 400; color: var(--white);
    font-size: clamp(38px, 6.4vw, 72px); line-height: 0.98; letter-spacing: 0.01em;
    max-width: 18ch; text-shadow: 0 2px 30px rgba(0,0,0,0.35);
  }
  .nl-article { max-width: 720px; }
  .nl-intro p, .nl-sec p, .nl-card p { font-family: var(--body); font-weight: 300; font-size: 18px; line-height: 1.65; letter-spacing: normal; }
  .nl-intro p + p, .nl-sec p + p { margin-top: 16px; }
  .nl-intro { padding-bottom: 8px; }
  .nl-article a { color: var(--blush-deep-text); text-underline-offset: 3px; }
  .nl-note { color: var(--mid-gray); }
  .nl-gate {
    margin: 36px 0 8px; padding: 20px 22px; border-radius: var(--radius-card);
    border: 1px dashed var(--blush); background: var(--blush-light);
  }
  .nl-gate p { font-family: var(--body); font-weight: 400; font-size: 16px; line-height: 1.55; letter-spacing: normal; }
  .nl-sec { border-top: 1px solid var(--light-gray); padding-top: 40px; margin-top: 44px; }
  .nl-sec h2 {
    font-family: var(--display); font-weight: 400; font-size: clamp(28px, 4vw, 38px);
    line-height: 1.05; letter-spacing: 0.02em; margin: 10px 0 18px;
  }
  .nl-sec h2 i { font-style: normal; }
  .nl-dyk { margin-top: 22px; padding: 18px 20px; border-radius: var(--radius-card); background: var(--blush-light); }
  .nl-dyk .eyebrow { display: block; margin-bottom: 6px; }
  .nl-video {
    position: relative; display: block; margin-top: 24px; border-radius: var(--radius-card);
    overflow: hidden; background: var(--dark); text-decoration: none;
  }
  .nl-video img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; opacity: 0.88; transition: opacity 0.2s, transform 0.4s; }
  .nl-video:hover img { opacity: 1; transform: scale(1.02); }
  .nl-video span {
    position: absolute; left: 0; right: 0; bottom: 0; padding: 40px 18px 14px;
    background: linear-gradient(transparent, rgba(0,0,0,0.75));
    font-family: var(--sans); font-size: 17px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--white);
  }
  .nl-video span::before { content: "▶"; margin-right: 10px; color: var(--blush); }
  .nl-video-live { cursor: default; }
  .nl-video-live iframe { display: block; width: 100%; aspect-ratio: 16 / 9; border: 0; }
  .nl-upnext { margin-top: 56px; padding: 26px 24px; border-radius: var(--radius-card); background: var(--dark); color: var(--off-white); }
  .nl-upnext h2 { font-family: var(--display); font-weight: 400; font-size: clamp(28px, 4vw, 36px); letter-spacing: 0.02em; margin: 6px 0 10px; color: var(--white); }
  .nl-upnext p { font-family: var(--body); font-weight: 300; font-size: 17px; line-height: 1.55; letter-spacing: normal; color: rgba(253,248,247,0.85); margin-bottom: 20px; }
  .nl-upnext .eyebrow { color: var(--blush); }
  .nl-pager { display: flex; justify-content: space-between; gap: 16px; margin-top: 48px; flex-wrap: wrap; }
  .nl-pager a { font-family: var(--sans); font-size: 17px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--dark); text-decoration: none; max-width: 48%; }
  .nl-pager a:hover { color: var(--blush-deep-text); }
  .nl-pager small { display: block; font-family: var(--body); font-size: 15px; letter-spacing: normal; text-transform: none; color: var(--mid-gray); margin-top: 4px; }
  .nl-list { max-width: 820px; }
  .nl-card { display: block; padding: 28px 0; border-bottom: 1px solid var(--light-gray); text-decoration: none; color: var(--dark); }
  .nl-card:first-child { border-top: 1px solid var(--light-gray); }
  .nl-card h2 { font-family: var(--display); font-weight: 400; font-size: clamp(26px, 3.6vw, 36px); line-height: 1.05; letter-spacing: 0.02em; margin: 8px 0 8px; transition: color 0.2s; }
  .nl-card:hover h2 { color: var(--blush-deep-text); }
  .nl-card p { color: var(--mid-gray); font-size: 17px; }
  /* Signup panel */
  .nl-signup { background: var(--dark); color: var(--off-white); text-align: center; }
  .nl-signup .shell { max-width: 640px; }
  .nl-signup .section-title { color: var(--white); }
  .nl-signup .eyebrow { color: var(--blush); }
  .nl-signup-sub { font-family: var(--body); font-weight: 300; font-size: 18px; line-height: 1.5; letter-spacing: normal; color: rgba(253,248,247,0.82); margin: 0 auto 26px; max-width: 46ch; }
  .newsletter-form { display: flex; max-width: 460px; margin: 0 auto; }
  .newsletter-form input[type="email"] { flex: 1; min-width: 0; background: var(--off-white); border: 1.5px solid var(--off-white); border-right: none; color: var(--dark); font-family: var(--body); font-size: 16px; padding: 15px 18px; outline: none; }
  .newsletter-form input[type="email"]:focus { border-color: var(--blush-deep); }
  .newsletter-form button { background: var(--blush-deep); border: none; color: var(--white); font-family: var(--sans); font-size: 15px; letter-spacing: 0.16em; text-transform: uppercase; padding: 15px 24px; cursor: pointer; white-space: nowrap; }
  .newsletter-form button:hover:not(:disabled) { background: var(--blush); color: var(--dark); }
  .newsletter-form button:disabled { opacity: 0.7; cursor: default; }
  .nl-msg { display: none; max-width: 460px; margin: 14px auto 0; padding: 14px 18px; border: 1px solid rgba(255,255,255,0.2); font-family: var(--body); font-size: 15px; letter-spacing: normal; }
  .nl-msg.err { color: var(--error-on-dark); }
  .nl-fine { font-family: var(--body); font-size: 14px; letter-spacing: normal; color: rgba(253,248,247,0.6); margin-top: 14px; }
"""

VIDEO_JS = """<script>
  // Tap a video card to play it here instead of leaving for YouTube.
  // The player only loads on tap, so pages stay light. No JS = the link still works.
  document.querySelectorAll('.nl-video[data-yt]').forEach(function(a) {
    a.addEventListener('click', function(e) {
      e.preventDefault();
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + a.dataset.yt + '?autoplay=1&rel=0&playsinline=1';
      f.title = a.textContent.trim();
      f.referrerPolicy = 'strict-origin-when-cross-origin';  // YouTube needs this (error 153 without)
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      var w = document.createElement('div');
      w.className = 'nl-video nl-video-live';
      w.appendChild(f);
      a.replaceWith(w);
      if (typeof fbq === 'function') fbq('trackCustom', 'VideoPlay', { video: a.dataset.yt });
    });
  });
</script>"""

SUBSCRIBE_JS = """<script>
  function getCookie(name) {
    var m = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return m ? m[2] : undefined;
  }
  document.getElementById('newsletterForm').addEventListener('submit', function(e) {
    e.preventDefault();
    if (this.querySelector('[name="website"]').value) return;
    var email = document.getElementById('newsletterEmail').value;
    var btn = document.getElementById('newsletterBtn');
    btn.textContent = 'Subscribing…'; btn.disabled = true;
    var eventId = crypto.randomUUID();
    fetch('https://bumpandgrind-subscribe.okaytkokay.workers.dev/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, event_id: eventId, fbp: getCookie('_fbp'), fbc: getCookie('_fbc') })
    }).then(function(res) {
      if (!(res.ok || res.status === 201)) throw new Error();
      document.getElementById('newsletterForm').style.display = 'none';
      document.getElementById('newsletterSuccess').style.display = 'block';
      if (typeof fbq === 'function') fbq('track', 'Lead', { content_name: 'Newsletter Signup (web issue)' }, { eventID: eventId });
    }).catch(function() {
      btn.textContent = 'Subscribe'; btn.disabled = false;
      document.getElementById('newsletterError').style.display = 'block';
    });
  });
</script>"""


def head(title, desc, url, og_type="website", extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#181412">
<title>{html.escape(title)}</title>
{PIXEL}
<meta name="description" content="{attr(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{attr(title)}">
<meta property="og:description" content="{attr(desc)}">
<meta property="og:image" content="{SITE}/IMAGES/BUMPANDGRIND-HERO-TOP.jpg">
<meta property="og:url" content="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Bump & Grind Halifax">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="64x64" href="/favicon-64.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{extra}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Bebas+Neue&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
<style>{CSS}</style>
</head>
<body>

<nav>
  <a href="/" aria-label="Bump & Grind home"><img class="nav-logo" src="/IMAGES/logo-nav.png" width="114" height="120" alt=""></a>
  <div class="nav-links">
    <a href="/newsletter/">Newsletter</a>
    <a href="/rewind/">Rewind</a>
    <a href="/nye/">NYE</a>
  </div>
</nav>
"""


def hero(eyebrow, h1, lede, h1_class="nl-headline"):
    return f"""
<section id="hero">
  <div class="hero-bg" aria-hidden="true"></div>
  <div class="hero-tint" aria-hidden="true"></div>
  <div class="hero-scrim" aria-hidden="true"></div>
  <div class="hero-inner">
    <p class="eyebrow">{eyebrow}</p>
    <h1 class="{h1_class}">{h1}</h1>
    <p class="hero-lede">{lede}</p>
  </div>
</section>
"""


SIGNUP = """
<section class="nl-signup" id="subscribe">
  <div class="shell">
    <p class="eyebrow">The Bump &amp; Grind newsletter</p>
    <h2 class="section-title">Get the next one first.</h2>
    <p class="nl-signup-sub">Every Wednesday: R&amp;B Rewind, R&amp;B Radar and On This Day, plus ticket links and VIP pricing before anyone else. Free.</p>
    <form class="newsletter-form" id="newsletterForm">
      <div style="position:absolute;left:-9999px" aria-hidden="true"><input type="text" name="website" tabindex="-1" autocomplete="off"></div>
      <label for="newsletterEmail" class="sr-only">Email address</label>
      <input type="email" id="newsletterEmail" placeholder="Your email address" required autocomplete="email">
      <button type="submit" id="newsletterBtn">Subscribe</button>
    </form>
    <div class="nl-msg" id="newsletterSuccess" role="status" aria-live="polite">You're on the list. See you Wednesday.</div>
    <div class="nl-msg err" id="newsletterError" role="status" aria-live="polite">Something went wrong. Try again in a minute.</div>
    <p class="nl-fine">Web versions go up a week after they hit inboxes.</p>
  </div>
</section>

<footer class="page-footer">
  <a href="/">← bumpandgrindhfx.com</a>
  <p>Halifax, NS · © 2026 Bump &amp; Grind</p>
</footer>
"""


def section_html(sec):
    emoji, label = KINDS[sec["kind"]]
    out = [f'  <section class="nl-sec">\n    <p class="eyebrow">{emoji} {label}</p>\n    <h2>{sec["title"]}</h2>']
    out += [f"    <p>{p}</p>" for p in sec["body"]]
    if sec.get("dyk"):
        out.append(f'    <div class="nl-dyk"><span class="eyebrow">Did you know 🧠</span><p>{sec["dyk"]}</p></div>')
    v = sec.get("video")
    if v:
        out.append(
            f'    <a class="nl-video" href="https://www.youtube.com/watch?v={v["id"]}" data-yt="{v["id"]}" target="_blank" rel="noopener">'
            f'<img src="https://i.ytimg.com/vi/{v["id"]}/hqdefault.jpg" width="480" height="270" loading="lazy" alt="">'
            f'<span>{v["label"]}</span></a>'
        )
    out.append("  </section>")
    return "\n".join(out)


def up_next_html():
    if not UP_NEXT:
        return ""
    u = UP_NEXT
    return f"""
  <aside class="nl-upnext">
    <p class="eyebrow">{u['eyebrow']}</p>
    <h2>{u['title']}</h2>
    <p>{u['body']}</p>
    <a class="btn" href="{u['href']}">{u['cta']}</a>
  </aside>"""


def issue_page(i, issue):
    url = f"{SITE}/newsletter/{issue['slug']}/"
    title = f"{strip_tags(issue['headline'])} | Bump & Grind Newsletter"
    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": strip_tags(issue["headline"]),
        "description": strip_tags(issue["dek"]),
        "datePublished": issue["date"],
        "url": url,
        "image": f"{SITE}/IMAGES/BUMPANDGRIND-HERO-TOP.jpg",
        "author": {"@type": "Organization", "name": "Bump & Grind", "url": SITE},
        "publisher": {"@type": "Organization", "name": "Bump & Grind", "url": SITE},
        "isPartOf": {"@type": "Blog", "name": "Bump & Grind Newsletter", "url": f"{SITE}/newsletter/"},
    }
    extra = f'<meta property="article:published_time" content="{issue["date"]}">\n<script type="application/ld+json">\n{json.dumps(ld, indent=2, ensure_ascii=False)}\n</script>\n'
    newer = ISSUES[i - 1] if i > 0 else None
    older = ISSUES[i + 1] if i + 1 < len(ISSUES) else None
    pager = ['<nav class="nl-pager" aria-label="More issues">']
    pager.append(f'<a href="/newsletter/{older["slug"]}/">← Older<small>{older["headline"]}</small></a>' if older else "<span></span>")
    pager.append(f'<a href="/newsletter/{newer["slug"]}/" style="text-align:right">Newer →<small>{newer["headline"]}</small></a>' if newer else '<a href="/newsletter/" style="text-align:right">All issues →</a>')
    pager.append("</nav>")
    intro = "\n".join(f"    <p>{p}</p>" for p in issue["intro"])
    sections = "\n".join(section_html(s) for s in issue["sections"])
    body = f"""{head(title, issue['dek'], url, 'article', extra)}{hero(f'<a href="/newsletter/" style="color:inherit">Newsletter</a> · {nice_date(issue["date"])}', issue['headline'], issue['dek'])}
<section>
  <article class="shell nl-article">
  <div class="nl-intro">
    <p class="eyebrow">What's up B&amp;G!</p>
{intro}
  </div>
  <div class="nl-gate"><p>🎟️ Subscribers also got this week's ticket links and early pricing. Those stay in the inbox. <a href="#subscribe">Get the next issue first</a>.</p></div>
{sections}
{up_next_html()}
  {''.join(pager)}
  </article>
</section>
{SIGNUP}
{SUBSCRIBE_JS}
{VIDEO_JS}
</body>
</html>
"""
    out = ROOT / "newsletter" / issue["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body)


def archive_page():
    url = f"{SITE}/newsletter/"
    cards = "\n".join(
        f'    <a class="nl-card" href="/newsletter/{x["slug"]}/"><span class="eyebrow">{nice_date(x["date"])}</span><h2>{x["headline"]}</h2><p>{x["dek"]}</p></a>'
        for x in ISSUES
    )
    body = f"""{head("The Newsletter | Bump & Grind Halifax R&B", "Halifax's R&B newsletter. Every Wednesday: R&B Rewind, R&B Radar, On This Day and first access to Bump & Grind tickets. Read recent issues.", url)}{hero('Bump <span>&amp;</span> Grind · Every Wednesday', 'The newsletter', "Halifax's R&amp;B newsletter. The story behind a classic, new R&amp;B worth your time, a moment in R&amp;B history, and first dibs on every ticket drop.", 'hero-giant')}
<section>
  <div class="shell nl-list">
{cards}
  </div>
</section>
{SIGNUP}
{SUBSCRIBE_JS}
{VIDEO_JS}
</body>
</html>
"""
    (ROOT / "newsletter" / "index.html").write_text(body)


def replace_between(path, start, end, new):
    s = path.read_text()
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pat.search(s):
        raise SystemExit(f"Markers missing in {path.name}: {start}")
    path.write_text(pat.sub(lambda m: start + new + end, s, count=1))


# ── REWIND ──────────────────────────────────────────────────────────────

REWIND_KINDS = ("rewind", "otd")


def slugify(s):
    s = unicodedata.normalize("NFKD", strip_tags(s)).encode("ascii", "ignore").decode()
    s = s.lower().replace("&", " and ")
    s = re.sub(r"[’'\u2019]", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def clip(s, n):
    s = re.sub(r"\s+", " ", strip_tags(s)).strip()
    if len(s) <= n:
        return s
    return s[: n - 1].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def rewind_posts():
    posts, seen = [], set()
    for issue in ISSUES:
        for sec in issue["sections"]:
            if sec["kind"] not in REWIND_KINDS or not sec.get("video"):
                continue
            title = sec.get("web_title") or sec["title"]
            slug = slugify(title)
            if slug in seen:
                slug = f"{slug}-{issue['date']}"
            seen.add(slug)
            posts.append({
                "slug": slug, "title": title, "kind": sec["kind"], "date": issue["date"],
                "issue": issue, "sec": sec,
                "thumb": f"https://i.ytimg.com/vi/{sec['video']['id']}/hqdefault.jpg",
                # Evergreen line for cards and meta: the fact box if there is one,
                # since body copy says things like "5 years ago this week".
                "dek": clip(sec.get("dyk") or " ".join(sec["body"]), 160),
            })
    return posts


def rw_kicker(post):
    emoji, label = KINDS[post["kind"]]
    return f"{emoji} {label}"


def rw_feature(post, eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (
        f'<a class="rw-feature" href="/rewind/{post["slug"]}/">'
        f'<span class="rw-feature-img"><img src="{post["thumb"]}" width="480" height="270" {load} alt=""></span>'
        f'<span class="rw-feature-body"><span class="rw-kicker">{rw_kicker(post)}</span>'
        f'<h3>{post["title"]}</h3><p>{html.escape(post["dek"])}</p>'
        f'<span class="rw-more">Read the story →</span></span></a>'
    )


def rw_row(post, heading="h3"):
    return (
        f'<a class="rw-row" href="/rewind/{post["slug"]}/">'
        f'<img src="{post["thumb"]}" width="132" height="74" loading="lazy" alt="">'
        f'<span><span class="rw-kicker">{rw_kicker(post)}</span>'
        f'<{heading}>{post["title"]}</{heading}><p>{html.escape(post["dek"])}</p></span></a>'
    )


REWIND_CSS = """
  .rw-body p { font-family: var(--body); font-weight: 300; font-size: 18px; line-height: 1.65; letter-spacing: normal; }
  .rw-body > p + p { margin-top: 16px; }
  .rw-body .nl-dyk p { font-size: 17px; }
  .nl-article .rw-row, .nl-article .btn-ghost { color: var(--dark); }
  .hero-lede a { color: inherit; text-underline-offset: 3px; }
  .rw-related { margin-top: 56px; }
  .rw-related .rw-list { grid-template-columns: 1fr; }
  .rw-index-feature { max-width: 760px; }
  .rw-index .rw-list { margin-top: 28px; }
"""


def rewind_page(post, posts):
    url = f"{SITE}/rewind/{post['slug']}/"
    sec, issue = post["sec"], post["issue"]
    title = f"{strip_tags(post['title'])} | Bump & Grind Rewind"
    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": strip_tags(post["title"]),
        "description": post["dek"],
        "datePublished": post["date"],
        "url": url,
        "image": post["thumb"],
        "author": {"@type": "Organization", "name": "Bump & Grind", "url": SITE},
        "publisher": {"@type": "Organization", "name": "Bump & Grind", "url": SITE},
        "isPartOf": {"@type": "Blog", "name": "Bump & Grind Rewind", "url": f"{SITE}/rewind/"},
    }
    extra = (
        f'<meta property="article:published_time" content="{post["date"]}">\n'
        f'<script type="application/ld+json">\n{json.dumps(ld, indent=2, ensure_ascii=False)}\n</script>\n'
        f"<style>{REWIND_CSS}</style>\n"
    )
    body = "\n".join(f"    <p>{p}</p>" for p in sec["body"])
    dyk = f'\n    <div class="nl-dyk"><span class="eyebrow">Did you know 🧠</span><p>{sec["dyk"]}</p></div>' if sec.get("dyk") else ""
    v = sec["video"]
    video = (
        f'\n    <a class="nl-video" href="https://www.youtube.com/watch?v={v["id"]}" data-yt="{v["id"]}" target="_blank" rel="noopener">'
        f'<img src="{post["thumb"]}" width="480" height="270" loading="lazy" alt="">'
        f'<span>{v["label"]}</span></a>'
    )
    others = [x for x in posts if x is not post][:3]
    related = "\n".join("      " + rw_row(x) for x in others)
    emoji, label = KINDS[post["kind"]]
    page = f"""{head(title, post['dek'], url, 'article', extra)}{hero(f'<a href="/rewind/" style="color:inherit">Rewind</a> · {emoji} {label}', post['title'], f'From the <a href="/newsletter/{issue["slug"]}/">{nice_date(issue["date"])} issue</a> of the Bump &amp; Grind newsletter.')}
<section>
  <article class="shell nl-article">
  <div class="rw-body">
{body}{dyk}{video}
  </div>
    <aside class="rw-related" aria-label="More Rewind">
      <p class="eyebrow">⏪️ More Rewind</p>
      <div class="rw-list">
{related}
      </div>
      <p style="margin-top:22px"><a class="btn-ghost btn" href="/rewind/">All Rewind stories</a></p>
    </aside>
  </article>
</section>
{SIGNUP}
{SUBSCRIBE_JS}
{VIDEO_JS}
</body>
</html>
"""
    out = ROOT / "rewind" / post["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)


def rewind_index(posts):
    url = f"{SITE}/rewind/"
    extra = f"<style>{REWIND_CSS}</style>\n"
    rows = "\n".join("      " + rw_row(x, "h2") for x in posts[1:])
    page = f"""{head("Rewind: The Stories Behind R&B Classics | Bump & Grind Halifax", "The stories behind the R&B classics we still play at every Bump & Grind party: anniversaries, birthdays and moments in R&B history, from Halifax's R&B newsletter.", url, "website", extra)}{hero('Bump <span>&amp;</span> Grind · R&amp;B nostalgia', 'Rewind', "The stories behind the R&amp;B classics we still play at every party. New ones every week from the Bump &amp; Grind newsletter.", 'hero-giant')}
<section>
  <div class="shell rw-index">
    <div class="rw-index-feature">{rw_feature(posts[0], eager=True).replace('<h3>', '<h2>').replace('</h3>', '</h2>')}</div>
    <div class="rw-list">
{rows}
    </div>
  </div>
</section>
{SIGNUP}
{SUBSCRIBE_JS}
{VIDEO_JS}
</body>
</html>
"""
    out = ROOT / "rewind" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)


def build_rewind():
    posts = rewind_posts()
    if not posts:
        return posts
    for post in posts:
        rewind_page(post, posts)
    rewind_index(posts)
    rows = "\n".join("          " + rw_row(x) for x in posts[1:5])
    replace_between(
        ROOT / "index.html", "<!-- REWIND:START -->", "<!-- REWIND:END -->",
        f'\n      <div class="rw-grid reveal">\n        {rw_feature(posts[0])}\n        <div class="rw-rows">\n{rows}\n        </div>\n      </div>\n      ',
    )
    urls = [f"{SITE}/rewind/"] + [f"{SITE}/rewind/{x['slug']}/" for x in posts]
    sm = "".join(f"\n  <url>\n    <loc>{u}</loc>\n    <changefreq>{'weekly' if u.endswith('/rewind/') else 'yearly'}</changefreq>\n    <priority>{'0.7' if u.endswith('/rewind/') else '0.5'}</priority>\n  </url>" for u in urls)
    replace_between(ROOT / "sitemap.xml", "<!-- REWIND:START -->", "<!-- REWIND:END -->", sm + "\n  ")
    return posts


def main():
    for i, issue in enumerate(ISSUES):
        issue_page(i, issue)
    archive_page()
    latest = ISSUES[0]
    replace_between(
        ROOT / "index.html", "<!-- NEWSLETTER-LATEST:START -->", "<!-- NEWSLETTER-LATEST:END -->",
        f'\n      <a href="/newsletter/{latest["slug"]}/" class="newsletter-recap-link">Read a recent issue: {latest["headline"]} →</a>\n      ',
    )
    urls = [f"{SITE}/newsletter/"] + [f"{SITE}/newsletter/{x['slug']}/" for x in ISSUES]
    sm = "".join(f"\n  <url>\n    <loc>{u}</loc>\n    <changefreq>{'weekly' if u.endswith('/newsletter/') else 'yearly'}</changefreq>\n    <priority>{'0.7' if u.endswith('/newsletter/') else '0.5'}</priority>\n  </url>" for u in urls)
    replace_between(ROOT / "sitemap.xml", "<!-- NEWSLETTER:START -->", "<!-- NEWSLETTER:END -->", sm + "\n  ")
    posts = build_rewind()
    print(f"Built {len(ISSUES)} issues + archive. Latest: {latest['slug']}")
    print(f"Built {len(posts)} Rewind posts + index.")


if __name__ == "__main__":
    main()
