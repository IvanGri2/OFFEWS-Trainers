#!/usr/bin/env python3
"""Builds the OFFEWS site.

    python3 build.py

writes index.html at the repository root (served by GitHub Pages) and tools/preview.html
(the same page without the document wrapper, for the claude.ai preview). Trainer data lives in TRAINERS
below; the function lists come from trainers-functions.json, which is generated from each
trainer's Cheats/CheatList.cs.
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(ROOT)   # the repository root is the published site
FUNCS = json.load(open(os.path.join(ROOT, "trainers-functions.json"), encoding="utf-8"))

# "download" is the file in downloads/. The release workflow publishes every file there as a
# GitHub release tagged with the file name, and the button links to that release asset so GitHub
# counts the downloads; "dl_prefix" sums the counts across all versions of a trainer.
TRAINERS = [
    {
        "id": "gears-e-day",
        "funcs": "gears",
        "title": "Gears of War: E-Day",
        "poster": "assets/gears-eday-poster.jpg",
        "shots": [("assets/gears-eday-main.jpg", "Окно трейнера", "Trainer window")],
        "version": "0.3.3",
        "updated": "2026-10-10",
        "game_build_ru": "omega-release, сборка 4894958",
        "game_build_en": "omega-release, build 4894958",
        "mode_ru": "Одиночная кампания",
        "mode_en": "Single-player campaign",
        "about_ru": "Бессмертие героя и отряда, бесконечные патроны и гранаты, убийство с одного выстрела, заморозка врагов, множитель урона и скорость игры.",
        "about_en": "Invincible hero and squad, unlimited ammo and grenades, one-hit kills, frozen enemies, a damage multiplier and game speed.",
        "download": "downloads/GearsEDayTrainer-0.3.3.exe",
        "dl_prefix": "GearsEDayTrainer-",
        "size_kb": 336,
        "glow": "#ff5a1f",
        "highlights": [("Бессмертие отряда", "Immortal squad"), ("Убийство с одного выстрела", "One-hit kills"),
                       ("Заморозка врагов", "Freeze enemies"), ("Множитель урона", "Damage multiplier")],
    },
    {
        "id": "hellraiser-revival",
        "funcs": "hellraiser",
        "title": "Clive Barker's Hellraiser: Revival",
        "poster": "assets/hellraiser-poster.jpg",
        "shots": [("assets/hellraiser-main.jpg", "Вкладка «Основное»", "Main tab"),
                  ("assets/hellraiser-more.jpg", "Вкладка «Дополнительно»", "More tab")],
        "version": "0.7.7",
        "updated": "2026-10-10",
        "game_build_ru": "1.0.1, сборка 227219",
        "game_build_en": "1.0.1, build 227219",
        "mode_ru": "Одиночная игра",
        "mode_en": "Single-player",
        "about_ru": "Режим бога и полёт, бесконечные страдания и патроны, монеты и предметы, убийство всех врагов, открытая карта, режим призрака, телепорт и сохранение в любом месте.",
        "about_en": "God mode and flight, unlimited suffering and ammo, coins and items, kill all enemies, full map reveal, ghost mode, teleport and save anywhere.",
        "download": "downloads/HellraiserRevivalTrainer-0.7.7.exe",
        "dl_prefix": "HellraiserRevivalTrainer-",
        "size_kb": 333,
        "glow": "#5f8cff",
        "highlights": [("Режим призрака", "Ghost mode"), ("Убить всех врагов", "Kill all enemies"),
                       ("Открыть всю карту", "Reveal map"), ("Сохранение в любом месте", "Save anywhere")],
    },
]

PAGE_RU = {0: "Основное", 1: "Дополнительно"}
PAGE_EN = {0: "Main", 1: "More"}


def e(s):
    return html.escape(s, quote=True)


def t(ru, en, tag="span"):
    """A bilingual text pair; CSS shows the one matching the page language."""
    return f'<{tag} lang="ru">{e(ru)}</{tag}><{tag} lang="en">{e(en)}</{tag}>'


def plural_ru(n, one, few, many):
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


def count(tr):
    return sum(len(g["items"]) for g in FUNCS[tr["funcs"]])


def keycap(combo):
    parts = combo.split("+")
    return '<span class="keys">' + '<i>+</i>'.join(f"<kbd>{e(p)}</kbd>" for p in parts) + "</span>"


def date_ru(d):
    y, m, dd = d.split("-")
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    return f"{int(dd)} {months[int(m) - 1]} {y}"


def date_en(d):
    y, m, dd = d.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return f"{months[int(m) - 1]} {int(dd)}, {y}"


def download_button(tr, big=False):
    cls = "btn btn-primary" + (" btn-big" if big else "")
    if tr["download"]:
        return (f'<a class="{cls}" href="{e(release_url(tr["download"]))}">{POWER_SMALL}'
                f'{t("Скачать", "Download")}<small>v{tr["version"]} · {tr["size_kb"]} {t("КБ", "KB")}</small></a>')
    return (f'<span class="{cls} is-off" aria-disabled="true">{POWER_SMALL}'
            f'{t("Скоро на GitHub", "Coming to GitHub")}<small>v{tr["version"]}</small></span>')


POWER_SMALL = ('<svg class="pw" viewBox="0 0 24 24" aria-hidden="true"><path d="M7.5 6.6a7.5 7.5 0 1 0 9 0" />'
               '<path d="M12 3v8" /></svg>')

EMBLEM = ('<svg class="emblem" viewBox="0 0 48 48" aria-hidden="true">'
          '<polygon class="hex" pathLength="1" points="24,3 42.2,13.5 42.2,34.5 24,45 5.8,34.5 5.8,13.5" />'
          '<path class="ring" pathLength="1" d="M17.4 18.3a9.6 9.6 0 1 0 13.2 0" /><path class="ring bar" pathLength="1" d="M24 13.6v10.6" /></svg>')

# Donation services: (name, link). An empty link shows the button as "soon".
SITE_URL = "https://ivangri2.github.io/OFFEWS-Trainers/"
REPO = "IvanGri2/OFFEWS-Trainers"

# Comments: giscus stores each trainer's thread as a GitHub Discussion in REPO. The section is
# left out until category_id is filled in (Discussions on, giscus app installed).
GISCUS = {"repo_id": "R_kgDOVDfyEw", "category": "Announcements", "category_id": ""}


def comments(tr):
    if not GISCUS["category_id"]:
        return ""
    return f"""
        <section class="comments reveal" aria-labelledby="{tr["id"]}-comments">
          <h3 id="{tr["id"]}-comments">{t("Комментарии", "Comments")}</h3>
          <p class="demo-hint">{t("Пиши, что работает, что нет и какую функцию добавить. Для комментария нужен аккаунт GitHub.", "Tell what works, what doesn't and which function to add. Commenting needs a GitHub account.")}</p>
          <div class="giscus-slot" data-term="{e(tr["id"])}" data-repo="{REPO}" data-repo-id="{GISCUS["repo_id"]}"
               data-category="{e(GISCUS["category"])}" data-category-id="{GISCUS["category_id"]}"></div>
        </section>"""


def release_url(path):
    name = os.path.basename(path)
    return f"https://github.com/{REPO}/releases/download/{name[:-4]}/{name}"


def dl_count(tr, cls):
    """Filled in by site.js from the GitHub releases API; stays hidden until a count arrives."""
    return f'<span class="{cls}" data-dl="{e(tr["dl_prefix"])}" hidden></span>' if tr.get("dl_prefix") else ""
DONATE = [("DonationAlerts", "https://www.donationalerts.com/r/offews")]


def chips(tr):
    return "".join(f'<li>{t(ru, en)}</li>' for ru, en in tr["highlights"])


def card(tr, i):
    n = count(tr)
    return f"""
      <article class="card reveal" style="--glow:{tr["glow"]}" data-tilt>
        <a class="card-link" href="#{tr["id"]}" aria-label="{e(tr["title"])}">
          <img class="card-art" src="{tr["poster"]}" alt="" width="480" height="720" loading="lazy">
          <span class="card-glare" aria-hidden="true"></span>
          <span class="card-count"><b>+{n}</b>{t(plural_ru(n, "функция", "функции", "функций"), "functions")}</span>
          {dl_count(tr, "card-dl")}
          <span class="card-info">
            <span class="card-ver mono">v{tr["version"]} · {t(tr["game_build_ru"], tr["game_build_en"])}</span>
            <span class="card-title">{e(tr["title"])}</span>
            <ul class="chips">{chips(tr)}</ul>
          </span>
        </a>
      </article>"""


def detail(tr):
    n = count(tr)
    groups = FUNCS[tr["funcs"]]
    pages = sorted({g["page"] for g in groups})
    blocks = []
    for page in pages:
        gs = [g for g in groups if g["page"] == page]
        inner = []
        for g in gs:
            rows = "".join(
                f'<li><span class="fn">{t(i["ru"], i["en"])}</span>{keycap(i["key"])}</li>' for i in g["items"])
            inner.append(f'<section class="group reveal"><h4>{t(g["ru"], g["en"])}</h4><ul>{rows}</ul></section>')
        head = f'<h3 class="page-tab">{t(PAGE_RU[page], PAGE_EN[page])}</h3>' if len(pages) > 1 else ""
        blocks.append(head + '<div class="groups">' + "".join(inner) + "</div>")
    shots = "".join(
        f'<figure class="reveal"><img src="{s}" alt="{e(ru)}" loading="lazy"><figcaption>{t(ru, en)}</figcaption></figure>'
        for s, ru, en in tr["shots"])
    word_ru = plural_ru(n, "функция", "функции", "функций")
    return f"""
    <section class="trainer" id="{tr["id"]}" style="--glow:{tr["glow"]}" aria-labelledby="{tr["id"]}-title">
      <div class="trainer-banner" style="--art:url('{tr["poster"]}')">
        <div class="wrap banner-grid">
          <img class="banner-poster reveal" src="{tr["poster"]}" alt="" width="480" height="720" loading="lazy">
          <div class="banner-copy">
            <p class="eyebrow">{t(f"Трейнер · {n} {word_ru}", f"Trainer · {n} functions")}</p>
            <h2 id="{tr["id"]}-title">{e(tr["title"])}</h2>
            <p class="lead">{t(tr["about_ru"], tr["about_en"])}</p>
            <dl class="facts">
              <div><dt>{t("Проверено на версии", "Tested on")}</dt><dd>{t(tr["game_build_ru"], tr["game_build_en"])}</dd></div>
              <div><dt>{t("Трейнер", "Trainer")}</dt><dd class="mono">v{tr["version"]}</dd></div>
              <div><dt>{t("Обновлён", "Updated")}</dt><dd>{t(date_ru(tr["updated"]), date_en(tr["updated"]))}</dd></div>
              <div><dt>{t("Режим", "Mode")}</dt><dd>{t(tr["mode_ru"], tr["mode_en"])}</dd></div>
            </dl>
            <div class="trainer-actions">{download_button(tr, big=True)}{dl_count(tr, "dl-count")}<span class="req">Windows 10/11 · .NET Framework 4.8</span></div>
          </div>
        </div>
      </div>
      <div class="wrap trainer-body">
        <div class="shots shots-{len(tr["shots"])}">{shots}</div>
        <details class="funcs">
          <summary>{t(f"Все {n} {word_ru} и горячие клавиши", f"All {n} functions and hotkeys")}</summary>
          <p class="demo-hint">{t("Горячие клавиши указаны по умолчанию, в трейнере их можно переназначить.", "Hotkeys are defaults and can be rebound in the trainer.")}</p>
          {"".join(blocks)}
        </details>
        {comments(tr)}
      </div>
    </section>"""


def donate_buttons():
    out = []
    for name, link in DONATE:
        if link:
            out.append(f'<a class="btn btn-donate" href="{e(link)}" target="_blank" rel="noopener">{e(name)}</a>')
        else:
            out.append(f'<span class="btn btn-donate is-off" aria-disabled="true">{e(name)}<small>{t("скоро", "soon")}</small></span>')
    return "".join(out)


def ticker():
    seen, items = set(), []
    for tr in TRAINERS:
        for g in FUNCS[tr["funcs"]]:
            for i in g["items"]:
                if i["ru"] not in seen and len(items) < 26:
                    seen.add(i["ru"])
                    items.append(i)
    row = "".join(f'<span>{t(i["ru"], i["en"])}</span>' for i in items)
    return f'<div class="ticker" aria-hidden="true"><div class="ticker-track">{row}{row}</div></div>'


def build():
    total = sum(count(tr) for tr in TRAINERS)
    cards = "".join(card(tr, i) for i, tr in enumerate(TRAINERS))
    details = "".join(detail(tr) for tr in TRAINERS)
    front, back = TRAINERS[0], TRAINERS[1]
    head = f"""<title>OFFEWS — трейнеры для Gears of War: E-Day и Hellraiser: Revival</title>
<meta name="description" content="Бесплатные трейнеры OFFEWS для одиночных игр: Gears of War: E-Day (+11) и Clive Barker's Hellraiser: Revival (+53). Бессмертие, бесконечные патроны, убийство с одного удара и другие функции в один клик.">
<link rel="canonical" href="{SITE_URL}">
<meta name="google-site-verification" content="LGgZCnU1x5ZTDmNnzVbXTUddLsuJ42UH349fdWI2jtk">
<meta property="og:type" content="website">
<meta property="og:site_name" content="OFFEWS Trainers">
<meta property="og:title" content="OFFEWS — трейнеры для одиночных игр">
<meta property="og:description" content="Gears of War: E-Day и Hellraiser: Revival. Бессмертие, бесконечные патроны и десятки функций в один клик. Бесплатно.">
<meta property="og:image" content="{SITE_URL}assets/gears-eday-main.jpg">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"OFFEWS Trainers","alternateName":["OFFEWS","offews trainers"],"url":"{SITE_URL}"}}</script>
<meta name="theme-color" content="#0b0b0d">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600&family=JetBrains+Mono:wght@500;600&family=Unbounded:wght@500;700;900&display=swap">
<style>{open(os.path.join(ROOT, "style.css"), encoding="utf-8").read()}</style>"""
    body = f"""<a class="skip" href="#catalog">{t("К трейнерам", "Skip to trainers")}</a>
<header class="top" id="top">
  <div class="wrap top-row">
    <a class="brand" href="#" aria-label="OFFEWS">{EMBLEM}<span class="word"><b>OFF</b>EWS<small>TRAINERS</small></span></a>
    <nav class="nav" aria-label="Sections">
      <a href="#catalog">{t("Игры", "Games")}</a>
      <a href="#howto">{t("Как это работает", "How it works")}</a>
      <a href="#faq">{t("Вопросы", "FAQ")}</a>
      <a class="nav-donate" href="#support">{t("Поддержать", "Support")}</a>
    </nav>
    <div class="lang" role="group" aria-label="Language">
      <button type="button" id="lang-ru" data-set-lang="ru" aria-pressed="true">RU</button>
      <button type="button" id="lang-en" data-set-lang="en" aria-pressed="false">EN</button>
    </div>
  </div>
</header>

<main>
  <section class="hero" style="--art-a:url('{back["poster"]}'); --art-b:url('{front["poster"]}')">
    <canvas class="embers" aria-hidden="true"></canvas>
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <div class="hero-mark" aria-hidden="true">{EMBLEM}</div>
        <h1>{t("Играй", "Play by")}<br><em>{t("по своим", "your own")}</em><br>{t("правилам", "rules")}</h1>
        <p class="lead">{t("Трейнеры для одиночных игр: бессмертие, бесконечные патроны, убийство с одного удара и ещё десятки функций. Запускаешь, трейнер сам находит игру, всё включается в один клик.", "Trainers for single-player games: god mode, unlimited ammo, one-hit kills and dozens more. Start it, the trainer finds the game, every function is one click away.")}</p>
        <div class="hero-cta">
          <a class="btn btn-primary btn-big" href="#catalog">{POWER_SMALL}{t("Выбрать игру", "Pick a game")}</a>
          <a class="btn btn-ghost btn-big" href="#howto">{t("Как это работает", "How it works")}</a>
        </div>
        <dl class="hero-stats">
          <div><dt>{t("игры", "games")}</dt><dd>{len(TRAINERS)}</dd></div>
          <div><dt>{t(plural_ru(total, "функция", "функции", "функций"), "functions")}</dt><dd>{total}</dd></div>
          <div><dt>{t("языка", "languages")}</dt><dd>RU/EN</dd></div>
        </dl>
      </div>
      <div class="stage" aria-hidden="true">
        <div class="stage-inner">
          <img class="win win-back" src="{back["shots"][0][0]}" alt="" width="1346" height="820">
          <img class="win win-front" src="{front["shots"][0][0]}" alt="" width="1174" height="628">
          <span class="stage-glow"></span>
        </div>
      </div>
    </div>
    {ticker()}
  </section>

  <section class="catalog" id="catalog" aria-labelledby="catalog-title">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="eyebrow">{t("Каталог", "Catalog")}</p>
        <h2 id="catalog-title">{t("Выбери игру", "Pick your game")}</h2>
      </div>
      <div class="cards">{cards}
      </div>
    </div>
  </section>
{details}
  <section class="howto" id="howto" aria-labelledby="howto-title">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="eyebrow">{t("Как это работает", "How it works")}</p>
        <h2 id="howto-title">{t("Четыре шага до бессмертия", "Four steps to god mode")}</h2>
      </div>
      <ol class="steps">
        <li class="reveal"><b>{t("Скачай", "Download")}</b><p>{t("Один exe-файл, устанавливать ничего не нужно.", "A single exe, nothing to install.")}</p></li>
        <li class="reveal"><b>{t("Запусти трейнер и игру", "Start trainer and game")}</b><p>{t("В любом порядке: трейнер сам найдёт игру.", "In any order: the trainer finds the game.")}</p></li>
        <li class="reveal"><b>{t("Дождись «подключено»", "Wait for “connected”")}</b><p>{t("Статус внизу окна. Загрузи сохранение или главу.", "Status is at the bottom. Load a save or chapter.")}</p></li>
        <li class="reveal"><b>{t("Включай", "Switch on")}</b><p>{t("Кликом в окне или горячей клавишей прямо в игре.", "Click in the window or press a hotkey in game.")}</p></li>
      </ol>
    </div>
  </section>

  <section class="support" id="support" aria-labelledby="support-title">
    <div class="wrap">
      <div class="support-panel reveal">
        <div class="support-mark" aria-hidden="true">{EMBLEM}</div>
        <div class="support-copy">
          <p class="eyebrow">{t("Поддержать OFFEWS", "Support OFFEWS")}</p>
          <h2 id="support-title">{t("Трейнеры бесплатные. Донаты делают их быстрее", "The trainers are free. Donations make them faster")}</h2>
          <p class="lead">{t("Каждый трейнер — это дни разбора игры и проверок после патчей. Если трейнер пригодился, поддержи проект: донаты идут на новые игры и обновления.", "Every trainer takes days of digging into the game and re-testing after patches. If one helped you, support the project: donations go to new games and updates.")}</p>
          <div class="donate-row">{donate_buttons()}</div>
        </div>
      </div>
    </div>
  </section>

  <section class="faq" id="faq" aria-labelledby="faq-title">
    <div class="wrap faq-grid">
      <div class="section-head reveal">
        <p class="eyebrow">{t("Вопросы", "FAQ")}</p>
        <h2 id="faq-title">{t("Частые вопросы", "Common questions")}</h2>
      </div>
      <div class="faq-list">
        <details class="reveal" open><summary>{t("Антивирус ругается на трейнер. Это вирус?", "My antivirus flags the trainer. Is it a virus?")}</summary>
          <p>{t("Нет. Трейнер меняет память игры, и некоторые антивирусы по эвристике считают это подозрительным. Обычно срабатывает один антивирус из семидесяти. Трейнер ничего не скачивает, не устанавливает и не отправляет в сеть.", "No. The trainer changes the game’s memory, and some antivirus heuristics find that suspicious. Usually one scanner out of seventy reacts. The trainer downloads, installs and sends nothing.")}</p></details>
        <details class="reveal"><summary>{t("Можно ли играть с трейнером по сети?", "Can I use a trainer online?")}</summary>
          <p>{t("Нет. Трейнеры сделаны только для одиночной игры. Если трейнер видит античит или сетевую игру, функции не включаются.", "No. The trainers are for single-player only. If a trainer detects an anti-cheat or an online session, functions stay off.")}</p></details>
        <details class="reveal"><summary>{t("Игра обновилась, и трейнер перестал работать", "The game updated and the trainer stopped working")}</summary>
          <p>{t("Сравни версию игры в окне трейнера с проверенной. Если они различаются, дождись обновления трейнера.", "Compare the game version in the trainer window with the tested one. If they differ, wait for a trainer update.")}</p></details>
        <details class="reveal"><summary>{t("Трейнер не запускается", "The trainer does not start")}</summary>
          <p>{t("Нужен .NET Framework 4.8. В Windows 10 и 11 он уже есть, в старых системах его можно поставить с сайта Microsoft.", "It needs .NET Framework 4.8. Windows 10 and 11 already have it; on older systems install it from Microsoft.")}</p></details>
        <details class="reveal"><summary>{t("Не испортит ли трейнер сохранения?", "Can the trainer break my saves?")}</summary>
          <p>{t("Функции меняют игру, только пока включены. Перед изменением денег, предметов и опыта на всякий случай сделай копию сохранений.", "Functions only change the game while they are on. Before changing money, items or experience, back up your saves just in case.")}</p></details>
      </div>
    </div>
  </section>
</main>

<footer class="foot">
  <div class="wrap foot-row">
    <a class="brand brand-small" href="#" aria-label="OFFEWS">{EMBLEM}<span class="word"><b>OFF</b>EWS</span></a>
    <p>{t("Трейнеры только для одиночной игры. OFFEWS не связан с разработчиками и издателями игр, названия и изображения игр принадлежат их владельцам.", "Trainers for single-player only. OFFEWS is not affiliated with game developers or publishers; game names and images belong to their owners.")}</p>
    <p class="mono">© 2026 OFFEWS</p>
  </div>
</footer>
<script>{open(os.path.join(ROOT, "site.js"), encoding="utf-8").read()}</script>"""

    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write('<!doctype html>\n<html lang="ru" data-lang="ru">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                + head + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")
    with open(os.path.join(ROOT, "preview.html"), "w", encoding="utf-8") as f:
        f.write(head + "\n" + body + "\n")
    with open(os.path.join(OUT, "assets", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><polygon points="24,3 42.2,13.5 42.2,34.5 24,45 5.8,34.5 5.8,13.5" '
                'fill="#2a1416" stroke="#c8262c" stroke-width="4"/><g fill="none" stroke="#eae7e2" stroke-width="4" stroke-linecap="round">'
                '<path d="M17.4 18.3a9.6 9.6 0 1 0 13.2 0"/><path d="M24 13.6v10.6"/></g></svg>')
    print("built", total, "functions")


if __name__ == "__main__":
    build()
