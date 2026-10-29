"""Generate the per-app pages under apps/ from the data below.

Run from the site root:  python tools/build-app-pages.py
Edit the APPS list, re-run, commit. index.html is hand-written and links to /apps/<slug>.
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "apps"

APPS = [
    {
        "slug": "liveby",
        "name": "liveby",
        "tagline": "Live-streaming camera with overlays",
        "icon": "../assets/logo/fullrink-mark.svg",
        "summary": (
            "liveby turns an Android phone into a live broadcast camera for rink sports. "
            "Its first overlay is an ice-hockey scoreboard you control from another phone over the internet, "
            "and you can layer images, video, text, music and replays on top of the stream. Every feature is free."
        ),
        "features": [
            "Stream live from the phone camera to your audience",
            "Hockey scoreboard overlay: period, clock, score, shots on goal and penalties",
            "Control the scoreboard from a second phone, anywhere with internet",
            "Overlays for images, looping video, text, web pages and music",
            "Instant replay of the last 10, 20 or 30 seconds, in slow motion",
            "Stream to YouTube, Facebook, Instagram, your own RTMP/RTSP, OBS and local recording at once",
            "Free, with every feature included: no subscription, no watermark",
        ],
        "links": [
            {"label": "Join the test on Google Play", "href": "https://play.google.com/apps/testing/th.co.aftershoot.liveby", "primary": True},
            {"label": "Original site: live.aftershoot.co.th", "href": "https://live.aftershoot.co.th/"},
        ],
        "shots": [],
        "status": "In testing on Google Play (package th.co.aftershoot.liveby).",
        # Content carried over from live.aftershoot.co.th (Thai), kept in its own language.
        "th_tagline": "แอพไลฟ์สดสำหรับกีฬาจริง — สกอร์บอร์ด ควบคุมระยะไกล รีเพลย์ ทุกอย่างฟรี",
        "feature_cards": [
            ("สกอร์บอร์ดในภาพ", "ฮอกกี้เต็มรูปแบบ: เวลา พีเรียด สกอร์ ชอตออนโกล เพนัลตี้ โลโก้ทีม ปรับขนาด/ตำแหน่งได้ และเปลี่ยนคำอธิบายให้ใช้กับกีฬาอื่นได้"),
            ("คุมสกอร์จากอีกเครื่อง", "เปิดหน้าเว็บควบคุมจากมือถือ/โน้ตบุ๊กเครื่องอื่น ทั้งในวง WiFi และผ่านอินเทอร์เน็ต — คนคุมสกอร์ไม่ต้องแตะกล้อง"),
            ("ซิงก์เวลากับบอร์ดจริง", "ส่องกล้องไปที่บอร์ดในลาน แล้วให้แอพอ่านเวลาเอง นาฬิกาบนภาพเดินตรงกับในสนาม"),
            ("รีเพลย์ทันที", "ย้อนดู 10/20/30 วินาทีที่ผ่านมา เล่นช้า x0.5 พร้อมป้าย REPLAY ให้คนดูรู้"),
            ("ใส่ภาพ วิดีโอ ข้อความ เว็บ", "โลโก้ผู้สนับสนุน วิดีโอวนลูป ข้อความบนจอ หน้าเว็บ — ลากนิ้วย้าย หนีบสองนิ้วย่อขยาย ตัดขอบได้"),
            ("เพลงเข้าสตรีม", "ใส่เพลงจากเครื่อง คนดูได้ยิน แต่ลำโพงมือถือเงียบ ปรับระดับเสียงได้"),
            ("ไลฟ์หลายที่พร้อมกัน", "YouTube, Facebook, Instagram, RTMP/RTSP ของคุณเอง, OBS และอัดลงเครื่องไปพร้อมกัน"),
            ("โหมด Clean feed", "ปุ่มเดียวย่อภาพให้ไปอยู่มุมจอ ปุ่มควบคุมทั้งหมดออกไปอยู่นอกกรอบ — เห็นชัดว่าคนดูเห็นอะไร"),
        ],
        "notice": ("ทุกฟีเจอร์เปิดใช้ฟรี", "ไม่มีสมาชิกรายเดือน ไม่มีลายน้ำ ไม่มีหน้าอัปเกรด ต่างจากแอพไลฟ์อื่นที่ล็อกการใส่รูป/วิดีโอไว้หลังค่าสมาชิก"),
        "steps": [
            ("เข้าร่วมทดสอบ", "เปิดลิงก์ทดสอบบน Play Store ด้วยบัญชี Google ที่ลงทะเบียนไว้ แล้วกดยอมรับ"),
            ("ติดตั้งจาก Play Store", "หลังกดเข้าร่วมแล้ว กดติดตั้งจากหน้าเดียวกัน"),
            ("เลือกปลายทาง", "ติ๊ก YouTube/Facebook/บันทึกลงเครื่อง แล้วกด START"),
            ("ส่งลิงก์ให้คนคุมสกอร์", "ป้ายล่างขวาคือที่อยู่หน้าควบคุม แตะเพื่อคัดลอก (ตั้ง Telegram ไว้ในหน้าตั้งค่าให้ส่งลิงก์อัตโนมัติก็ได้)"),
        ],
        "changelog": [
            ("3.15.0 — ส่งลิงก์เข้า Telegram", [
                "ตั้งค่า → Scoreboard: ใส่ Telegram bot token แล้วแอพส่งลิงก์หน้าควบคุมเข้าแชทให้เอง (ลิงก์ในวงทันทีที่เปิดแอพ ลิงก์อินเทอร์เน็ตเมื่อพร้อม)",
                "หน้า About บอกเวอร์ชันที่ใช้อยู่ พร้อมประวัติการอัปเดต",
            ]),
            ("3.14.x — จัดวางด้วยนิ้ว + Clean feed", [
                "แตะเลเยอร์แล้วลากย้าย/หนีบซูมบนภาพจริง พร้อมปุ่มหมุน ตัดขอบ สลับชั้น ลบ",
                "ปุ่ม Clean สลับภาพเต็มจอ ↔ กรอบ 16:9 ที่ไม่มีปุ่มบัง",
            ]),
            ("3.13.x — เพลง ตัดขอบ และปุ่มเพิ่มที่หาเจอ", [
                "ใส่เพลงเข้าสตรีม ปรับเสียงได้",
                "ตัดขอบรูป/ข้อความ/เว็บเป็นเปอร์เซ็นต์",
                "ทุกแท็บมีแถบเพิ่มเต็มความกว้าง",
            ]),
            ("3.12.x — เสถียรภาพ", [
                "กราฟิกล้นแล้วไม่ดับ — ตัดเลเยอร์เสริมแล้วสตรีมต่อ",
                "แก้ความละเอียดถูกตั้งเป็นค่าสูงสุดเองจนเครื่องเก่าดับ",
            ]),
            ("3.9–3.11 — ปุ่มจริง รีเพลย์ และลิงก์อินเทอร์เน็ต", [
                "ไฟฉาย ความเป็นส่วนตัว แกลเลอรี พักการอัด",
                "รีเพลย์ สโลว์โมชัน · Pro camera (EV/WB/โฟกัส)",
                "ลิงก์ควบคุมผ่านเน็ตใช้งานได้จริง ไม่ตายตอนจอดับ ต่อใหม่เอง",
                "รองรับ Android 16 (targetSdk 36)",
            ]),
        ],
        "footnote": "หน้าควบคุมสกอร์บอร์ดของแต่ละงานจะอยู่ที่ลิงก์ที่แอพสร้างให้ ไม่ใช่หน้านี้",
    },
    {
        "slug": "dejavucam",
        "name": "dejavucam",
        "tagline": "Retroactive recording. Tap after it happens.",
        "icon": "../assets/apps/dejavucam/icon-512.png",
        "summary": (
            "dejavucam is always recording to memory, so you never miss the moment. "
            "When the goal, the save or the hit happens, one tap saves the last 5 to 30 seconds as a clip, "
            "with a few extra seconds of tail. Replay it in slow motion, step through it frame by frame, keep or share."
        ),
        "features": [
            "Always-on recording to a RAM buffer, nothing saved until you tap",
            "Buffer of 5, 10, 15, 20 or 30 seconds, plus up to 5 seconds of tail",
            "1080p at 60 fps when the phone supports it",
            "Replay at 1x, 0.5x and 0.25x with single-frame stepping",
            "Corner replay loops the last clip while you keep recording",
            "Pinch zoom, rule-of-thirds grid, sound on or off",
            "Clips go straight to your gallery and are easy to share",
        ],
        "links": [
            {"label": "Join the test on Google Play", "href": "https://play.google.com/apps/testing/th.co.aftershoot.drillcam", "primary": True},
        ],
        "shots": [
            ("../assets/apps/dejavucam/store-0-auto-goal.jpg", "Automatic goal clip"),
            ("../assets/apps/dejavucam/store-1-capture.jpg", "Capture screen"),
            ("../assets/apps/dejavucam/store-2-overlays.jpg", "Overlays"),
            ("../assets/apps/dejavucam/store-3-replay.jpg", "Replay with frame stepping"),
            ("../assets/apps/dejavucam/store-4-landscape.jpg", "Landscape capture"),
        ],
        "status": "In testing on Google Play (package th.co.aftershoot.drillcam).",
    },
    {
        "slug": "mobilevar",
        "name": "mobileVAR",
        "tagline": "Video review from your pocket",
        "icon": "../assets/logo/fullrink-mark.svg",
        "summary": (
            "mobileVAR brings video review to the bench. Freeze the play, step through it frame by frame "
            "and compare angles so officials and coaches can check a goal or a close call without leaving the rink. "
            "It is in development; the page will be updated when a build is ready to try."
        ),
        "features": [
            "Review a clip on the phone right after the play",
            "Freeze and single-frame stepping",
            "Side-by-side angles from more than one camera",
            "Built to work with clips from dejavucam and liveby",
        ],
        "links": [
            {"label": "Ask about early access", "href": "mailto:hello@fullrink.com?subject=mobileVAR", "primary": True},
        ],
        "shots": [],
        "status": "In development.",
    },
    {
        "slug": "analytic-cam",
        "name": "analytic cam",
        "tagline": "Skating technique, measured on your phone",
        "icon": "../assets/apps/analytic-cam/icon-512.png",
        "summary": (
            "analytic cam records a skating clip with an on-screen horizon level, then analyses it on the phone with "
            "pose tracking. The replay shows a skeleton with live lean, left-knee, right-knee and balance cards, "
            "followed by a scored report. Record at 240 or 120 fps for slow-motion detail, or import a clip from the gallery."
        ),
        "features": [
            "On-device pose tracking, no upload needed",
            "Live lean, knee-angle and balance readouts on the replay",
            "Scored technique report after each clip",
            "Slow-motion capture at 240 or 120 fps on supported phones",
            "Import existing clips from the gallery",
            "Export the replay with the skeleton overlay as a video",
        ],
        "links": [
            {"label": "Join the test on Google Play", "href": "https://play.google.com/apps/testing/th.co.aftershoot.analyticcam", "primary": True},
        ],
        "shots": [
            ("../assets/apps/analytic-cam/screenshot-1-capture.jpg", "Capture with horizon level"),
            ("../assets/apps/analytic-cam/screenshot-2-replay.jpg", "Replay with skeleton and cards"),
            ("../assets/apps/analytic-cam/screenshot-3-report.jpg", "Scored report"),
        ],
        "status": "In testing on Google Play (package th.co.aftershoot.analyticcam).",
    },
    {
        "slug": "scoreboard",
        "name": "liveby scoreboard",
        "tagline": "A live hockey scoreboard in any browser",
        "icon": "../assets/logo/fullrink-mark.svg",
        "summary": (
            "liveby scoreboard puts a live scoreboard on any screen with a browser: period, clock, score and penalties, "
            "updated in real time. Run it on a rink display, share the link with viewers, or overlay it on a liveby stream."
        ),
        "features": [
            "Period, clock, score and penalties, live",
            "Works in any browser, no install",
            "Controlled remotely while the game runs",
            "Made to overlay on a liveby broadcast",
        ],
        "links": [
            {"label": "Open liveby scoreboard", "href": "https://livebyscoreboard.vercel.app/", "primary": True},
        ],
        "shots": [],
        "status": "Live on the web.",
    },
]

NAV_ORDER = [a["slug"] for a in APPS]

# Product names shown on the site, applied to text only (slugs and hrefs stay lowercase).
DISPLAY_NAMES = [
    ("liveby scoreboard", "Live By Scoreboard"),
    ("analytic cam", "Analytic Cam"),
    ("mobileVAR", "Mobile VAR"),
    ("dejavucam", "DejaVu Cam"),
    ("liveby", "Live By"),
]
DEVELOPER_URL = "https://app.aftershoot.co.th/"


def brand_names(doc: str) -> str:
    import re

    def fix(m):
        t = m.group(0)
        for a, b in DISPLAY_NAMES:
            t = t.replace(a, b)
        return t

    doc = re.sub(r">[^<]+<", fix, doc)
    doc = re.sub(r'(content="[^"]*")', lambda m: fix_attr(m.group(1)), doc)
    return doc


def fix_attr(t: str) -> str:
    for a, b in DISPLAY_NAMES:
        t = t.replace(a, b)
    return t


def e(s: str) -> str:
    return html.escape(s, quote=True)


def page(app: dict) -> str:
    name = e(app["name"])
    links = "".join(
        f'<a class="btn{"" if l.get("primary") else " btn-ghost"}" href="{e(l["href"])}"'
        f'{" target=_blank rel=noopener" if l["href"].startswith("http") else ""}>{e(l["label"])}</a>\n'
        for l in app["links"]
    )
    features = "".join(f"<li>{e(f)}</li>\n" for f in app["features"])
    shots = ""
    if app["shots"]:
        items = "".join(
            f'<figure><img src="{e(src)}" alt="{e(cap)}" loading="lazy"><figcaption>{e(cap)}</figcaption></figure>\n'
            for src, cap in app["shots"]
        )
        shots = f'<section class="section app-shots"><div class="container"><h2>Screens</h2><div class="shots">{items}</div></div></section>'
    others = "".join(
        f'<a href="{s}"{" aria-current=page" if s == app["slug"] else ""}>{e(a["name"])}</a>\n'
        for s, a in zip(NAV_ORDER, APPS)
    )
    th_tagline = f'<p class="lead th">{e(app["th_tagline"])}</p>' if app.get("th_tagline") else ""
    extra = ""
    if app.get("feature_cards"):
        cards = "".join(
            f'<article class="card"><h3>{e(t)}</h3><p>{e(d)}</p></article>\n' for t, d in app["feature_cards"]
        )
        notice = ""
        if app.get("notice"):
            notice = f'<p class="notice"><strong>{e(app["notice"][0])}</strong> — {e(app["notice"][1])}</p>'
        extra += f'<section class="section"><div class="container"><h2>ทำอะไรได้บ้าง</h2><div class="cards">{cards}</div>{notice}</div></section>\n'
    if app.get("steps"):
        steps = "".join(f"<li><strong>{e(t)}</strong> — {e(d)}</li>\n" for t, d in app["steps"])
        extra += f'<section class="section section-alt" id="how"><div class="container"><h2>เริ่มใช้งาน</h2><ol class="steps-list">{steps}</ol></div></section>\n'
    if app.get("changelog"):
        log = "".join(
            f"<h3>{e(t)}</h3><ul>" + "".join(f"<li>{e(b)}</li>" for b in bullets) + "</ul>\n"
            for t, bullets in app["changelog"]
        )
        extra += f'<section class="section"><div class="container"><h2>อัปเดตล่าสุด</h2><div class="changelog">{log}</div></div></section>\n'
    footnote = f'<p class="muted small">{e(app["footnote"])}</p>' if app.get("footnote") else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{name} — FullRink</title>
  <meta name="description" content="{e(app["tagline"])}. {e(app["summary"][:150])}">
  <meta name="theme-color" content="#071628">
  <meta property="og:title" content="{name} — FullRink">
  <meta property="og:description" content="{e(app["tagline"])}">
  <meta property="og:image" content="https://fullrink.com/assets/logo/fullrink-mark-1200.png">
  <link rel="icon" href="../favicon.ico" sizes="32x32">
  <link rel="icon" href="../assets/icons/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="../assets/icons/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <header class="site-header">
    <div class="container nav">
      <a class="brand" href="../" aria-label="FullRink home">
        <img src="../assets/logo/fullrink-mark.svg" alt="" width="40" height="40">
        <span class="brand-name">Full<span class="accent">Rink</span></span>
      </a>
      <nav aria-label="Primary">
        <a href="../#apps">Apps</a>
        <a href="../#how">How it fits</a>
        <a href="../#contact">Contact</a>
        <a href="{DEVELOPER_URL}" target="_blank" rel="noopener">AfterShoot</a>
        <a class="btn btn-small" href="../#apps">All apps</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="hero app-hero">
      <div class="container">
        <p class="eyebrow"><a href="../#apps">FullRink apps</a> / {name}</p>
        <div class="app-head">
          <img class="app-icon" src="{e(app["icon"])}" alt="" width="96" height="96">
          <div>
            <h1>{name}</h1>
            <p class="by">by FullRink · developed by <a href="{DEVELOPER_URL}" target="_blank" rel="noopener">AfterShoot</a></p>
            <p class="lead">{e(app["tagline"])}</p>
            {th_tagline}
          </div>
        </div>
        <p class="lead app-summary">{e(app["summary"])}</p>
        <div class="hero-actions">
{links}        </div>
        <p class="muted small">{e(app["status"])}</p>
        {footnote}
      </div>
    </section>

    <section class="section section-alt">
      <div class="container app-grid">
        <div>
          <h2>What it does</h2>
          <ul class="features">
{features}          </ul>
        </div>
        <aside class="app-side">
          <h3>Other FullRink apps</h3>
          <nav class="app-nav" aria-label="FullRink apps">
{others}          </nav>
        </aside>
      </div>
    </section>

    {extra}
    {shots}

    <section class="section cta">
      <div class="container cta-box">
        <h2>Questions about {name}?</h2>
        <p class="muted">Tell us what your rink needs, or ask to join the test.</p>
        <div class="hero-actions">
          <a class="btn" href="mailto:hello@fullrink.com?subject={e(app["name"])}">Contact us</a>
          <a class="btn btn-ghost" href="../#apps">Back to all apps</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-bottom">
      <span class="muted small">&copy; <span id="year">2026</span> FullRink · <a href="{DEVELOPER_URL}" target="_blank" rel="noopener">AfterShoot</a>. All rights reserved. FullRink is the app brand of AfterShoot.</span>
    </div>
  </footer>
  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for app in APPS:
        path = OUT / f"{app['slug']}.html"
        path.write_text(brand_names(page(app)), encoding="utf-8", newline="\n")
        print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
