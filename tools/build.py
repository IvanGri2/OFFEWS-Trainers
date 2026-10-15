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
        "slug": "gears-of-war-e-day-trainer",
        "funcs": "gears",
        "title": "Gears of War: E-Day",
        "poster": "assets/gears-eday-poster.jpg",
        "shots": [("assets/gears-eday-main.jpg", "Окно трейнера", "Trainer window")],
        "version": "1.0.0",
        "updated": "2026-10-10",
        "game_build_ru": "omega-release, сборка 4894958",
        "game_build_en": "omega-release, build 4894958",
        "mode_ru": "Одиночная кампания",
        "mode_en": "Single-player campaign",
        "about_ru": "Бессмертие героя и отряда, бесконечные патроны и гранаты, убийство с одного выстрела, заморозка врагов, множитель урона и скорость игры.",
        "about_en": "Invincible hero and squad, unlimited ammo and grenades, one-hit kills, frozen enemies, a damage multiplier and game speed.",
        "download": "downloads/GearsEDayTrainer-1.0.0.exe",
        "dl_prefix": "GearsEDayTrainer-",
        "size_kb": 341,
        "glow": "#ff5a1f",
        "highlights": [("Бессмертие отряда", "Immortal squad"), ("Убийство с одного выстрела", "One-hit kills"),
                       ("Заморозка врагов", "Freeze enemies"), ("Множитель урона", "Damage multiplier")],
    },
    {
        "id": "hellraiser-revival",
        "slug": "hellraiser-revival-trainer",
        "funcs": "hellraiser",
        "title": "Clive Barker's Hellraiser: Revival",
        "poster": "assets/hellraiser-poster.jpg",
        "shots": [("assets/hellraiser-main.jpg", "Вкладка «Основное»", "Main tab"),
                  ("assets/hellraiser-more.jpg", "Вкладка «Дополнительно»", "More tab")],
        "version": "1.0.0",
        "updated": "2026-10-10",
        "game_build_ru": "1.0.1, сборка 227219",
        "game_build_en": "1.0.1, build 227219",
        "mode_ru": "Одиночная игра",
        "mode_en": "Single-player",
        "about_ru": "Режим бога и полёт, бесконечные страдания и патроны, монеты и предметы, убийство всех врагов, открытая карта, режим призрака, телепорт и сохранение в любом месте.",
        "about_en": "God mode and flight, unlimited suffering and ammo, coins and items, kill all enemies, full map reveal, ghost mode, teleport and save anywhere.",
        "download": "downloads/HellraiserRevivalTrainer-1.0.0.exe",
        "dl_prefix": "HellraiserRevivalTrainer-",
        "size_kb": 334,
        "glow": "#5f8cff",
        "highlights": [("Режим призрака", "Ghost mode"), ("Убить всех врагов", "Kill all enemies"),
                       ("Открыть всю карту", "Reveal map"), ("Сохранение в любом месте", "Save anywhere")],
    },
    {
        "id": "end-of-abyss",
        "slug": "end-of-abyss-trainer",
        "funcs": "abyss",
        "title": "End of Abyss",
        "poster": "assets/abyss-poster.jpg",
        "shots": [("assets/abyss-main.jpg", "Вкладка «Основное»", "Main tab"),
                  ("assets/abyss-more.jpg", "Вкладка «Дополнительно»", "More tab")],
        "version": "1.0.0",
        "updated": "2026-10-10",
        "game_build_ru": "сборка от 03.10.2026",
        "game_build_en": "build of 2026-10-03",
        "mode_ru": "Одиночная игра",
        "mode_en": "Single-player",
        "about_ru": "Режим бога, бесконечные патроны и аптечки, стрельба без перезарядки и перегрева, убийство с одного удара, заморозка врагов, деньги, все улучшения оружия, полёт и телепорт.",
        "about_en": "God mode, unlimited ammo and heals, no reload or overheating, one-hit kills, frozen enemies, money, every weapon upgrade, flight and teleport.",
        "download": "downloads/EndOfAbyssTrainer-1.0.0.exe",
        "dl_prefix": "EndOfAbyssTrainer-",
        "size_kb": 232,
        "glow": "#3fb6ff",
        "highlights": [("Убийство с одного удара", "One-hit kills"), ("Без перезарядки", "No reload"),
                       ("Все улучшения оружия", "All weapon upgrades"), ("Заморозка врагов", "Freeze enemies")],
    },
    {
        "id": "silver-pines",
        "slug": "silver-pines-trainer",
        "funcs": "pines",
        "title": "Silver Pines",
        "poster": "assets/pines-poster.jpg",
        "shots": [("assets/pines-main.jpg", "Вкладка «Основное»", "Main tab"),
                  ("assets/pines-more.jpg", "Вкладка «Дополнительно»", "More tab")],
        "version": "1.0.0",
        "updated": "2026-10-10",
        "game_build_ru": "версия 1.0 (618_173902)",
        "game_build_en": "version 1.0 (618_173902)",
        "mode_ru": "Одиночная игра",
        "mode_en": "Single-player",
        "about_ru": "Бессмертие, бесконечные выносливость и патроны, неломающееся оружие ближнего боя, вечный фонарик, убийство с одного удара, все двери без ключей, открытая карта, скорость игры и деньги.",
        "about_en": "God mode, unlimited stamina and ammo, unbreakable melee weapons, a flashlight that never dies, one-hit kills, every door unlocked, the full map, game speed and money.",
        "download": "downloads/SilverPinesTrainer-1.0.0.exe",
        "dl_prefix": "SilverPinesTrainer-",
        "size_kb": 217,
        "glow": "#e0312f",
        "highlights": [("Бессмертие", "God mode"), ("Все двери без ключей", "Master key"),
                       ("Убийство с одного удара", "One-hit kills"), ("Вечный фонарик", "Endless flashlight")],
    },
    {
        "id": "atomfall",
        "slug": "atomfall-trainer",
        "funcs": "atomfall",
        "title": "Atomfall",
        "poster": "assets/atomfall-poster.jpg",
        "shots": [("assets/atomfall-main.jpg", "Окно трейнера", "Trainer window")],
        "version": "1.0.0",
        "updated": "2026-10-12",
        "game_build_ru": "сборка 2025.10.12.1730162",
        "game_build_en": "build 2025.10.12.1730162",
        "mode_ru": "Одиночная игра",
        "mode_en": "Single-player",
        "about_ru": "Бессмертие, бесконечные выносливость и патроны, убийство с одного удара, невидимость для врагов, предметы не тратятся, материалы для крафта, лёгкая торговля, очки навыков и скорость игры.",
        "about_en": "God mode, unlimited stamina and ammo, one-hit kills, invisibility to enemies, items that are never used up, crafting materials, easy trades, skill points and game speed.",
        "download": "downloads/AtomfallTrainer-1.0.0.exe",
        "dl_prefix": "AtomfallTrainer-",
        "size_kb": 393,
        "glow": "#7bc043",
        "highlights": [("Невидимость", "Invisibility"), ("Убийство с одного удара", "One-hit kills"),
                       ("Лёгкая торговля", "Easy trades"), ("Предметы не тратятся", "Items never run out")],
    },
    {
        "id": "retrospace",
        "slug": "retrospace-trainer",
        "funcs": "retrospace",
        "title": "Retrospace",
        "poster": "assets/retrospace-poster.jpg",
        "shots": [("assets/retrospace-main.jpg", "Окно трейнера", "Trainer window")],
        "version": "1.0.0",
        "updated": "2026-10-13",
        "game_build_ru": "версия 1.0 от 01.10.2026",
        "game_build_en": "version 1.0 of 2026-10-01",
        "mode_ru": "Одиночная игра",
        "mode_en": "Single-player",
        "about_ru": "Бессмертие, бесконечные выносливость, кислород, энергия мутамодов и патроны, скорость передвижения, высота прыжка и скорость игры.",
        "about_en": "God mode, unlimited stamina, oxygen, mutamod energy and ammo, movement speed, jump height and game speed.",
        "download": "downloads/RetroSpaceTrainer-1.0.0.exe",
        "dl_prefix": "RetroSpaceTrainer-",
        "size_kb": 306,
        "glow": "#e8a23a",
        "highlights": [("Бессмертие", "God mode"), ("Бесконечный кислород", "Unlimited oxygen"),
                       ("Бесконечные патроны", "Unlimited ammo"), ("Высота прыжка", "Jump height")],
    },
    {
        "id": "valor-mortis",
        "slug": "valor-mortis-trainer",
        "funcs": "valormortis",
        "title": "Valor Mortis",
        "poster": "assets/valormortis-poster.jpg",
        "shots": [("assets/valormortis-main.jpg", "Вкладка «Основное»", "Main tab"),
                  ("assets/valormortis-more.jpg", "Вкладка «Дополнительно»", "More tab")],
        "version": "1.0.1",
        "updated": "2026-10-14",
        "game_build_ru": "сборка 34495",
        "game_build_en": "build 34495",
        "mode_ru": "Одиночная игра",
        "mode_en": "Single-player",
        "about_ru": "Все функции встроенного меню читов разработчиков: режим бога, бесконечные выносливость, нефтоглобин, фляги и патроны, полёт сквозь стены, невидимость, убийство с одного удара, открытие оружия и способностей, торговцы и меню улучшений.",
        "about_en": "Every function of the developers' built-in cheat menu: god mode, unlimited stamina, nephtoglobin, flasks and ammo, no clip, invisibility, one-hit kills, unlock all weapons and abilities, merchants and upgrade menus.",
        "download": "downloads/ValorMortisTrainer-1.0.1.exe",
        "dl_prefix": "ValorMortisTrainer-",
        "size_kb": 308,
        "glow": "#d8452f",
        "highlights": [("Режим бога", "God mode"), ("Полёт сквозь стены", "No clip"),
                       ("Открыть всё оружие", "Unlock all weapons"), ("Убийство с одного удара", "One-hit kills")],
    },
]

# AI voice-overs: Russian dubbing mods with a setup installer. "download" works like a trainer's: the
# file in downloads/ becomes a GitHub release. "samples" are short mp3 lines in assets/voice/.
VOICE_SECTION = "ai-voiceover/"
MODS_DIR = "Content\\Paks\\~mods"
VOICEOVERS = [
    {
        "id": "end-of-abyss-voice",
        "slug": "end-of-abyss-russian-voiceover",
        "title": "End of Abyss",
        "poster": "assets/abyss-poster.jpg",
        "version": "1.0.0",
        "updated": "2026-10-15",
        "game_build_ru": "версия октября 2026",
        "game_build_en": "October 2026 version",
        "lines": 177,
        "about_ru": "Русская озвучка всех реплик игры: солдаты, капитан, переговоры по рации, катсцены, Fractured и ИИ. Голоса сделаны нейросетью по образцу оригинальных и обработаны как в игре: голос из шлема скафандра, помехи рации. Переговоры экипажа, которые в оригинале звучат неразборчивым бормотанием, тоже озвучены по-русски.",
        "about_en": "Russian dubbing of every voiced line in the game: soldiers, the captain, radio calls, cutscenes, Fractured and the AI. The voices are AI-generated after the original ones and processed like in the game: a voice inside a suit helmet, radio static. Crew chatter that is unintelligible babble in the original is voiced in Russian too.",
        "download": "downloads/EndOfAbyssRuVoice-Setup-1.0.0.exe",
        "dl_prefix": "EndOfAbyssRuVoice-",
        "size_mb": 6.8,
        "shot": ("assets/abyss-voice-setup.png", "Окно установщика", "Installer window"),
        "glow": "#3fb6ff",
        "highlights": [("Все реплики игры", "Every voiced line"), ("Эффект шлема и рации", "Helmet and radio effects"),
                       ("Озвучены переговоры экипажа", "Crew chatter voiced"), ("Удаление в один клик", "One-click uninstall")],
        # (file in assets/voice/, speaker RU, speaker EN, line)
        "samples": [("eoa-ru-soldier-e19.mp3", "Солдат E-19", "Soldier E-19", "Эта дверь защищена активным энергозамком."),
                    ("eoa-ru-captain.mp3", "Капитан", "Captain", "Техник, найди способ открыть дверь."),
                    ("eoa-ru-radio.mp3", "Рация", "Radio", "Кажется, один из энергоканалов не работает.")],
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
SITE_URL = "https://offews-trainers.pro/"
REPO = "IvanGri2/OFFEWS-Trainers"

# Comments. Cusdis (cusdis.com) takes a name and a comment, no account needed, and each comment
# waits for approval in the Cusdis dashboard. Until its app_id is filled in, the page falls back
# to giscus, which stores each trainer's thread as a GitHub Discussion in REPO.
CUSDIS = {"app_id": ""}
GISCUS = {"repo_id": "R_kgDOVDfyEw", "category": "Announcements", "category_id": "DIC_kwDOVDfyE84DHe5a"}


def comments(tr):
    if CUSDIS["app_id"]:
        hint = t("Пиши, что работает, что нет и какую функцию добавить. Регистрация не нужна, комментарий появится после проверки.",
                 "Tell what works, what doesn't and which function to add. No sign-up needed; comments appear after review.")
        slot = (f'<div class="cusdis-slot" data-host="https://cusdis.com" data-app-id="{CUSDIS["app_id"]}" '
                f'data-page-id="{e(tr["id"])}" data-page-url="{SITE_URL}{tr["slug"]}/" data-page-title="{e(tr["title"])}" data-theme="dark"></div>')
    elif GISCUS["category_id"]:
        hint = t("Пиши, что работает, что нет и какую функцию добавить. Для комментария нужен аккаунт GitHub.",
                 "Tell what works, what doesn't and which function to add. Commenting needs a GitHub account.")
        slot = (f'<div class="giscus-slot" data-term="{e(tr["id"])}" data-repo="{REPO}" data-repo-id="{GISCUS["repo_id"]}" '
                f'data-category="{e(GISCUS["category"])}" data-category-id="{GISCUS["category_id"]}"></div>')
    else:
        return ""
    return f"""
        <section class="comments reveal" aria-labelledby="{tr["id"]}-comments">
          <h3 id="{tr["id"]}-comments">{t("Комментарии", "Comments")}</h3>
          <p class="demo-hint">{hint}</p>
          {slot}
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
        <a class="card-link" href="{tr["slug"]}/" aria-label="{e(tr["title"])}">
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


def detail(tr, lang, h="h2"):
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
        f'<figure class="reveal"><img src="{s}" alt="{e(en if lang == "en" else ru)}" loading="lazy"><figcaption>{t(ru, en)}</figcaption></figure>'
        for s, ru, en in tr["shots"])
    word_ru = plural_ru(n, "функция", "функции", "функций")
    return f"""
    <section class="trainer" id="{tr["id"]}" style="--glow:{tr["glow"]}" aria-labelledby="{tr["id"]}-title">
      <div class="trainer-banner" style="--art:url('{tr["poster"]}')">
        <div class="wrap banner-grid">
          <img class="banner-poster reveal" src="{tr["poster"]}" alt="" width="480" height="720" loading="lazy">
          <div class="banner-copy">
            <p class="eyebrow">{t(f"Трейнер · {n} {word_ru}", f"Trainer · {n} functions")}</p>
            <{h} id="{tr["id"]}-title"><small>{t("Трейнер и читы для", "Trainer & cheats for")}</small>{e(tr["title"])}</{h}>
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


def alternates(path):
    """hreflang links for a page that exists at SITE_URL+path (Russian) and SITE_URL+"en/"+path."""
    ru, en = SITE_URL + path, SITE_URL + "en/" + path
    return (f'<link rel="alternate" hreflang="ru" href="{ru}">\n<link rel="alternate" hreflang="en" href="{en}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{ru}">')


def head_tags(title, desc, path, lang, image, extra=""):
    url = SITE_URL + ("en/" if lang == "en" else "") + path
    return f"""<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{alternates(path)}
<meta name="google-site-verification" content="LGgZCnU1x5ZTDmNnzVbXTUddLsuJ42UH349fdWI2jtk">
<meta name="yandex-verification" content="db4692bf265461a0">
<meta property="og:type" content="website">
<meta property="og:site_name" content="OFFEWS Trainers">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{"en_US" if lang == "en" else "ru_RU"}">
<meta property="og:locale:alternate" content="{"ru_RU" if lang == "en" else "en_US"}">
<meta property="og:image" content="{SITE_URL}{image}">
<meta name="twitter:card" content="summary_large_image">
{extra}
<meta name="theme-color" content="#0b0b0d">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600&family=JetBrains+Mono:wght@500;600&family=Unbounded:wght@500;700;900&display=swap">
<style>{open(os.path.join(ROOT, "style.css"), encoding="utf-8").read()}</style>"""


def header(home, path, lang):
    """home is the path back to the front page: "" there, "../" on a game page. path is the page's
    address below the language root, for the RU/EN switch."""
    cur = ' aria-current="true"'
    sw = "".join(f'<a href="{SITE_URL}{"en/" if l == "en" else ""}{path}" hreflang="{l}" data-set-lang="{l}"'
                 f'{cur if l == lang else ""}>{l.upper()}</a>' for l in ("ru", "en"))
    return f"""<a class="skip" href="#main">{t("К содержимому", "Skip to content")}</a>
<header class="top" id="top">
  <div class="wrap top-row">
    <a class="brand" href="{home or "#"}" aria-label="OFFEWS">{EMBLEM}<span class="word"><b>OFF</b>EWS<small>TRAINERS</small></span></a>
    <nav class="nav" aria-label="Sections">
      <a href="{home}#catalog">{t("Игры", "Games")}</a>
      <a class="nav-voice" href="{home}{VOICE_SECTION}">{t("AI озвучка", "AI voice-over")}</a>
      <a href="#howto">{t("Как это работает", "How it works")}</a>
      <a href="#faq">{t("Вопросы", "FAQ")}</a>
      <a class="nav-donate" href="#support">{t("Поддержать", "Support")}</a>
    </nav>
    <div class="lang" role="group" aria-label="Language">
      {sw}
    </div>
  </div>
</header>"""


def howto():
    return f"""
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
  </section>"""


def support():
    return f"""
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
  </section>"""


# (question RU, question EN, answer RU, answer EN). Shown on every page and given to search engines as FAQPage data.
FAQ = [
    ("Антивирус ругается на трейнер. Это вирус?", "My antivirus flags the trainer. Is it a virus?", "Нет. Трейнер меняет память игры, и некоторые антивирусы по эвристике считают это подозрительным. Обычно срабатывает один антивирус из семидесяти. Трейнер ничего не скачивает, не устанавливает и не отправляет в сеть.", "No. The trainer changes the game’s memory, and some antivirus heuristics find that suspicious. Usually one scanner out of seventy reacts. The trainer downloads, installs and sends nothing."),
    ("Можно ли играть с трейнером по сети?", "Can I use a trainer online?", "Нет. Трейнеры сделаны только для одиночной игры. Если трейнер видит античит или сетевую игру, функции не включаются.", "No. The trainers are for single-player only. If a trainer detects an anti-cheat or an online session, functions stay off."),
    ("Игра обновилась, и трейнер перестал работать", "The game updated and the trainer stopped working", "Сравни версию игры в окне трейнера с проверенной. Если они различаются, дождись обновления трейнера.", "Compare the game version in the trainer window with the tested one. If they differ, wait for a trainer update."),
    ("Трейнер не запускается", "The trainer does not start", "Нужен .NET Framework 4.8. В Windows 10 и 11 он уже есть, в старых системах его можно поставить с сайта Microsoft.", "It needs .NET Framework 4.8. Windows 10 and 11 already have it; on older systems install it from Microsoft."),
    ("Не испортит ли трейнер сохранения?", "Can the trainer break my saves?", "Функции меняют игру, только пока включены. Перед изменением денег, предметов и опыта на всякий случай сделай копию сохранений.", "Functions only change the game while they are on. Before changing money, items or experience, back up your saves just in case."),
]


def faq():
    rows = "".join(
        f'\n        <details class="reveal"{" open" if k == 0 else ""}><summary>{t(qr, qe)}</summary>\n          <p>{t(ar, ae)}</p></details>'
        for k, (qr, qe, ar, ae) in enumerate(FAQ))
    return f"""
  <section class="faq" id="faq" aria-labelledby="faq-title">
    <div class="wrap faq-grid">
      <div class="section-head reveal">
        <p class="eyebrow">{t("Вопросы", "FAQ")}</p>
        <h2 id="faq-title">{t("Частые вопросы", "Common questions")}</h2>
      </div>
      <div class="faq-list">{rows}
      </div>
    </div>
  </section>"""


def faq_ld(lang):
    k = 1 if lang == "en" else 0
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q[k], "acceptedAnswer": {"@type": "Answer", "text": q[2 + k]}} for q in FAQ]}


def footer(home):
    return f"""
<footer class="foot">
  <div class="wrap foot-row">
    <a class="brand brand-small" href="{home or "#"}" aria-label="OFFEWS">{EMBLEM}<span class="word"><b>OFF</b>EWS</span></a>
    <p>{t("Трейнеры только для одиночной игры. OFFEWS не связан с разработчиками и издателями игр, названия и изображения игр принадлежат их владельцам.", "Trainers for single-player only. OFFEWS is not affiliated with game developers or publishers; game names and images belong to their owners.")}</p>
    <p class="mono">© 2026 OFFEWS</p>
  </div>
</footer>
<script>{open(os.path.join(ROOT, "site.js"), encoding="utf-8").read()}</script>"""


def write_page(rel, head, body, lang, depth=0):
    """Writes OUT/rel in one language: text pairs of the other language are dropped, and pages
    below the root get their local asset paths rewritten (../assets/, ../../assets/)."""
    other = "en" if lang == "ru" else "ru"
    head, body = (re.sub(rf'<(\w+) lang="{other}">.*?</\1>', "", x, flags=re.S) for x in (head, body))
    doc = (f'<!doctype html>\n<html lang="{lang}" data-lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           + head + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")
    if depth:
        up = "../" * depth
        for a, b in (('src="assets/', f'src="{up}assets/'), ('href="assets/', f'href="{up}assets/'), ("url('assets/", f"url('{up}assets/")):
            doc = doc.replace(a, b)
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    return doc


def ld_script(*items):
    return f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": list(items)}, ensure_ascii=False)}</script>'


def game_page(tr, lang):
    n = count(tr)
    en = lang == "en"
    path = f"{tr['slug']}/"
    root = SITE_URL + ("en/" if en else "")
    url = root + path
    name, about_ru, about_en = tr["title"], tr["about_ru"], tr["about_en"]
    if en:
        title = f"{name} Trainer (+{n} cheats) — free download | OFFEWS"
        desc = f"Free {name} trainer with {n} cheats: {about_en[0].lower()}{about_en[1:]} Version {tr['version']}, a single exe, one-click hotkeys."
    else:
        title = f"Трейнер для {name} (+{n}) — читы, скачать бесплатно | OFFEWS"
        desc = f"Бесплатный трейнер (читы) для {name}: {about_ru[0].lower()}{about_ru[1:]} Версия {tr['version']}, один exe-файл, включение в один клик."
    app = {
        "@type": "SoftwareApplication", "name": f"{name} Trainer (OFFEWS)", "description": about_en if en else about_ru,
        "applicationCategory": "GameApplication", "operatingSystem": "Windows 10, Windows 11",
        "softwareVersion": tr["version"], "dateModified": tr["updated"], "fileSize": f"{tr['size_kb']} KB",
        "inLanguage": ["ru", "en"], "url": url, "image": SITE_URL + tr["shots"][0][0], "screenshot": [SITE_URL + s[0] for s in tr["shots"]],
        "downloadUrl": release_url(tr["download"]),
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "author": {"@type": "Organization", "name": "OFFEWS", "url": SITE_URL},
    }
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "OFFEWS Trainers", "item": root},
        {"@type": "ListItem", "position": 2, "name": f"{name} Trainer" if en else f"Трейнер для {name}", "item": url}]}
    head = head_tags(title, desc, path, lang, tr["shots"][0][0], ld_script(app, crumbs, faq_ld(lang)))
    word_ru = plural_ru(n, "функция", "функции", "функций")
    about = f"""
    <section class="wrap about-text reveal" aria-labelledby="{tr["id"]}-about">
      <h2 id="{tr["id"]}-about">{t(f"Читы для {name}", f"{name} cheats")}</h2>
      <p>{t(f"Трейнер OFFEWS — это {n} {word_ru} читов для {name} в одной небольшой программе, без модов и правки файлов игры. {about_ru}",
             f"The OFFEWS trainer packs {n} cheats for {name} into one small program, with no mods and no changes to game files. {about_en}")}</p>
      <p>{t(f"Трейнер проверен на версии {tr['game_build_ru']}, режим: {tr['mode_ru'].lower()}. Скачай exe-файл, запусти его вместе с игрой и включай читы кликом в окне трейнера или горячими клавишами прямо в игре.",
             f"Tested on {tr['game_build_en']}, mode: {tr['mode_en'].lower()}. Download the exe, run it alongside the game and switch cheats on with a click in the trainer window or with hotkeys in game.")}</p>
    </section>"""
    body = f"""{header("../", path, lang)}

<main id="main" class="game-main">
  <nav class="crumbs wrap" aria-label="Breadcrumbs"><a href="../#catalog">{t("Все трейнеры", "All trainers")}</a><span aria-hidden="true">/</span><span>{e(name)}</span></nav>
{detail(tr, lang, h="h1")}
{about}
{howto()}
{support()}
{faq()}
</main>
{footer("../")}"""
    write_page(("en/" if en else "") + f"{tr['slug']}/index.html", head, body, lang, depth=2 if en else 1)


def home_page(lang):
    en = lang == "en"
    total = sum(count(tr) for tr in TRAINERS)
    cards = "".join(card(tr, i) for i, tr in enumerate(TRAINERS))
    front, back, mid = TRAINERS[0], TRAINERS[1], TRAINERS[2]
    names = ", ".join(tr["title"] for tr in TRAINERS)
    games = ", ".join(f"{tr['title']} (+{count(tr)})" for tr in TRAINERS)
    if en:
        title = "OFFEWS — free game trainers and cheats: " + ", ".join(tr["title"] for tr in TRAINERS)
        desc = f"Free OFFEWS trainers for single-player games: {games}. God mode, unlimited ammo, one-hit kills and more, one click or hotkey away."
    else:
        title = "OFFEWS — трейнеры и читы для игр: " + ", ".join(tr["title"] for tr in TRAINERS)
        desc = f"Бесплатные трейнеры (читы) OFFEWS для одиночных игр: {games}. Бессмертие, бесконечные патроны, убийство с одного удара и другие функции в один клик."
    site = {"@type": "WebSite", "name": "OFFEWS Trainers", "alternateName": ["OFFEWS", "offews trainers"], "url": SITE_URL,
            "inLanguage": ["ru", "en"], "description": desc}
    org = {"@type": "Organization", "name": "OFFEWS", "url": SITE_URL, "logo": SITE_URL + "assets/favicon.svg"}
    catalog = {"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": f"{tr['title']} Trainer", "url": f"{SITE_URL}{'en/' if en else ''}{tr['slug']}/"}
        for k, tr in enumerate(TRAINERS)]}
    head = head_tags(title, desc, "", lang, "assets/gears-eday-main.jpg", ld_script(site, org, catalog, faq_ld(lang)))
    body = f"""{header("", "", lang)}

<main id="main">
  <section class="hero" style="--art-a:url('{back["poster"]}'); --art-b:url('{front["poster"]}')">
    <canvas class="embers" aria-hidden="true"></canvas>
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <div class="hero-mark" aria-hidden="true">{EMBLEM}</div>
        <h1>{t("Играй", "Play by")}<br><em>{t("по своим", "your own")}</em><br>{t("правилам", "rules")}</h1>
        <p class="lead">{t(f"Бесплатные трейнеры и читы для одиночных игр: {names}. Бессмертие, бесконечные патроны, убийство с одного удара и ещё десятки функций. Запускаешь, трейнер сам находит игру, всё включается в один клик.", f"Free trainers and cheats for single-player games: {names}. God mode, unlimited ammo, one-hit kills and dozens more. Start it, the trainer finds the game, every function is one click away.")}</p>
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
          <img class="win win-mid" src="{mid["shots"][0][0]}" alt="" width="1176" height="628">
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
        <h2 id="catalog-title">{t("Трейнеры для игр", "Game trainers")}</h2>
      </div>
      <div class="cards">{cards}
      </div>
    </div>
  </section>
{voice_teaser()}
{howto()}
{support()}
{faq()}
</main>
{footer("")}"""
    doc = write_page("en/index.html" if en else "index.html", head, body, lang, depth=1 if en else 0)
    if not en:
        with open(os.path.join(ROOT, "preview.html"), "w", encoding="utf-8") as f:
            f.write(head + "\n" + body + "\n")
    return total



# ---------- AI voice-over section ----------

VOICE_FAQ = [
    ("Что нужно для установки?", "What do I need to install it?",
     "Лицензионная игра на ПК и Windows 10 или 11. Установщик сам находит папку игры в Steam, если не нашёл, её можно выбрать вручную. Перед установкой закрой игру.",
     "The PC game and Windows 10 or 11. The installer finds the game folder in Steam by itself; if it does not, pick the folder by hand. Close the game before installing."),
    ("Меняет ли озвучка файлы игры?", "Does the voice-over change game files?",
     "Нет. Установщик только добавляет файлы мода в папку Content\\Paks\\~mods, оригинальные файлы игры остаются как есть. Удаление убирает эти файлы, и игра звучит как раньше.",
     "No. The installer only adds the mod files to Content\\Paks\\~mods and leaves the original game files as they are. Uninstalling removes those files and the game sounds as before."),
    ("Как удалить озвучку?", "How do I remove it?",
     "Запусти установщик ещё раз и нажми «Удалить». Можно и вручную: удали файлы zzz_OffewsRU_* из папки Content\\Paks\\~mods.",
     "Run the installer again and press Uninstall. Or by hand: delete the zzz_OffewsRU_* files from Content\\Paks\\~mods."),
    ("Игра обновилась, и озвучка пропала или сломалась", "The game updated and the voice-over is gone or broken",
     "Озвучка сделана под определённую сборку игры, она указана на странице. После крупного патча удали озвучку и дождись обновления.",
     "The voice-over is made for a specific game build, shown on this page. After a big patch uninstall it and wait for an update."),
    ("Кто озвучивал?", "Who voiced it?",
     "Нейросеть. Это неофициальная фанатская озвучка, голоса сгенерированы ИИ и обработаны под звук оригинала. Субтитры остаются из игры.",
     "A neural network. This is an unofficial fan dub: the voices are AI-generated and processed to match the original sound. Subtitles stay as in the game."),
]


def voice_faq():
    rows = "".join(
        f'\n        <details class="reveal"{" open" if k == 0 else ""}><summary>{t(qr, qe)}</summary>\n          <p>{t(ar, ae)}</p></details>'
        for k, (qr, qe, ar, ae) in enumerate(VOICE_FAQ))
    return f"""
  <section class="faq" id="faq" aria-labelledby="faq-title">
    <div class="wrap faq-grid">
      <div class="section-head reveal">
        <p class="eyebrow">{t("Вопросы", "FAQ")}</p>
        <h2 id="faq-title">{t("Частые вопросы об озвучке", "Voice-over questions")}</h2>
      </div>
      <div class="faq-list">{rows}
      </div>
    </div>
  </section>"""


def voice_faq_ld(lang):
    k = 1 if lang == "en" else 0
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q[k], "acceptedAnswer": {"@type": "Answer", "text": q[2 + k]}} for q in VOICE_FAQ]}


def voice_howto():
    return f"""
  <section class="howto" id="howto" aria-labelledby="howto-title">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="eyebrow">{t("Как установить", "How to install")}</p>
        <h2 id="howto-title">{t("Три шага до русской речи", "Three steps to Russian speech")}</h2>
      </div>
      <ol class="steps">
        <li class="reveal"><b>{t("Скачай установщик", "Download the installer")}</b><p>{t("Один exe-файл, внутри уже всё нужное.", "One exe with everything inside.")}</p></li>
        <li class="reveal"><b>{t("Закрой игру и запусти его", "Close the game, run it")}</b><p>{t("Установщик сам найдёт папку игры, проверь путь.", "It finds the game folder; check the path.")}</p></li>
        <li class="reveal"><b>{t("Нажми «Установить»", "Press Install")}</b><p>{t("Запускай игру. Удалить можно тем же установщиком.", "Start the game. The same installer uninstalls.")}</p></li>
      </ol>
    </div>
  </section>"""


def voice_download(v, big=False):
    cls = "btn btn-primary" + (" btn-big" if big else "")
    if v["download"] and v["size_mb"]:
        return (f'<a class="{cls}" href="{e(release_url(v["download"]))}">{POWER_SMALL}'
                f'{t("Скачать установщик", "Download installer")}<small>v{v["version"]} · {v["size_mb"]} {t("МБ", "MB")}</small></a>')
    return (f'<span class="{cls} is-off" aria-disabled="true">{POWER_SMALL}'
            f'{t("Скоро", "Coming soon")}<small>v{v["version"]}</small></span>')


def voice_samples(v):
    if not v["samples"]:
        return ""
    rows = "".join(
        f'<li class="sample reveal"><span class="sample-who">{t(sr, se)}</span><span class="sample-line">{e(line)}</span>'
        f'<audio controls preload="none" src="assets/voice/{e(f)}"></audio></li>'
        for f, sr, se, line in v["samples"])
    return f"""
        <section class="samples" aria-labelledby="{v["id"]}-samples">
          <h3 id="{v["id"]}-samples">{t("Послушай, как звучит", "Hear how it sounds")}</h3>
          <ul class="sample-list">{rows}</ul>
        </section>"""


def voice_card(v):
    return f"""
      <article class="card reveal" style="--glow:{v["glow"]}" data-tilt>
        <a class="card-link" href="{v["slug"]}/" aria-label="{e(v["title"])}">
          <img class="card-art" src="{v["poster"]}" alt="" width="480" height="720" loading="lazy">
          <span class="card-glare" aria-hidden="true"></span>
          <span class="card-count"><b>{v["lines"]}</b>{t(plural_ru(v["lines"], "реплика", "реплики", "реплик"), "lines")}</span>
          {dl_count(v, "card-dl")}
          <span class="card-info">
            <span class="card-ver mono">{t("Русская AI озвучка", "Russian AI dub")} · v{v["version"]}</span>
            <span class="card-title">{e(v["title"])}</span>
            <ul class="chips">{chips(v)}</ul>
          </span>
        </a>
      </article>"""


def voice_game_page(v, lang):
    en = lang == "en"
    path = f"{v['slug']}/"
    root = SITE_URL + ("en/" if en else "")
    url = root + path
    name = v["title"]
    if en:
        title = f"{name} Russian voice-over (AI dub) — free download | OFFEWS"
        desc = f"Free Russian AI voice-over for {name}: {v['lines']} lines with helmet and radio effects, one-click installer and uninstaller. Version {v['version']}."
    else:
        title = f"Русская озвучка {name} (AI) — скачать бесплатно | OFFEWS"
        desc = f"Бесплатная русская AI озвучка {name}: {v['lines']} реплик с эффектом шлема и рации, установка и удаление в один клик. Версия {v['version']}."
    app = {
        "@type": "SoftwareApplication", "name": f"{name} Russian voice-over (OFFEWS)", "description": v["about_en"] if en else v["about_ru"],
        "applicationCategory": "GameApplication", "operatingSystem": "Windows 10, Windows 11",
        "softwareVersion": v["version"], "dateModified": v["updated"], "inLanguage": "ru", "url": url, "image": SITE_URL + v["poster"],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "author": {"@type": "Organization", "name": "OFFEWS", "url": SITE_URL},
    }
    if v["size_mb"]:
        app["downloadUrl"] = release_url(v["download"])
        app["fileSize"] = f"{v['size_mb']} MB"
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "OFFEWS", "item": root},
        {"@type": "ListItem", "position": 2, "name": "AI voice-over" if en else "AI озвучка", "item": root + VOICE_SECTION},
        {"@type": "ListItem", "position": 3, "name": name, "item": url}]}
    head = head_tags(title, desc, path, lang, v["poster"], ld_script(app, crumbs, voice_faq_ld(lang)))
    body = f"""{header("../", path, lang)}

<main id="main" class="game-main">
  <nav class="crumbs wrap" aria-label="Breadcrumbs"><a href="../{VOICE_SECTION}">{t("AI озвучка", "AI voice-over")}</a><span aria-hidden="true">/</span><span>{e(name)}</span></nav>
    <section class="trainer" id="{v["id"]}" style="--glow:{v["glow"]}" aria-labelledby="{v["id"]}-title">
      <div class="trainer-banner" style="--art:url('{v["poster"]}')">
        <div class="wrap banner-grid">
          <img class="banner-poster reveal" src="{v["poster"]}" alt="" width="480" height="720" loading="lazy">
          <div class="banner-copy">
            <p class="eyebrow">{t(f"AI озвучка · {v['lines']} {plural_ru(v['lines'], 'реплика', 'реплики', 'реплик')}", f"AI voice-over · {v['lines']} lines")}</p>
            <h1 id="{v["id"]}-title"><small>{t("Русская озвучка для", "Russian voice-over for")}</small>{e(name)}</h1>
            <p class="lead">{t(v["about_ru"], v["about_en"])}</p>
            <dl class="facts">
              <div><dt>{t("Сделано для версии", "Made for")}</dt><dd>{t(v["game_build_ru"], v["game_build_en"])}</dd></div>
              <div><dt>{t("Озвучка", "Voice-over")}</dt><dd class="mono">v{v["version"]}</dd></div>
              <div><dt>{t("Обновлена", "Updated")}</dt><dd>{t(date_ru(v["updated"]), date_en(v["updated"]))}</dd></div>
              <div><dt>{t("Язык", "Language")}</dt><dd>{t("Русский, субтитры из игры", "Russian, game subtitles")}</dd></div>
            </dl>
            <div class="trainer-actions">{voice_download(v, big=True)}{dl_count(v, "dl-count")}<span class="req">Windows 10/11 · .NET Framework 4.8</span></div>
          </div>
        </div>
      </div>
      <div class="wrap trainer-body">
        {voice_samples(v)}
        <div class="voice-setup">
        <figure class="shots reveal"><img src="{v["shot"][0]}" alt="{e(v["shot"][2] if lang == "en" else v["shot"][1])}" width="626" height="429" loading="lazy"><figcaption>{t(v["shot"][1], v["shot"][2])}</figcaption></figure>
        <section class="about-text reveal">
          <h2>{t("Что внутри", "What is inside")}</h2>
          <p>{t(f"Установщик добавляет мод в папку {MODS_DIR} и не трогает оригинальные файлы игры. Тем же установщиком озвучку можно удалить, и игра снова заговорит по-английски.", f"The installer adds the mod to {MODS_DIR} and does not touch the original game files. The same installer removes it, and the game speaks English again.")}</p>
          <p>{t("Неофициальная фанатская озвучка: голоса сгенерированы нейросетью. Нужна лицензионная игра.", "Unofficial fan dub: the voices are AI-generated. You need the game itself.")}</p>
        </section>
        </div>
      </div>
    </section>
{voice_howto()}
{support()}
{voice_faq()}
</main>
{footer("../")}"""
    write_page(("en/" if en else "") + f"{v['slug']}/index.html", head, body, lang, depth=2 if en else 1)


def voice_section_page(lang):
    en = lang == "en"
    path = VOICE_SECTION
    names = ", ".join(v["title"] for v in VOICEOVERS)
    if en:
        title = f"AI voice-overs for games: Russian dubbing of {names} | OFFEWS"
        desc = f"Free Russian AI voice-overs for games: {names}. Voices made after the originals, with game-like effects and a one-click installer."
    else:
        title = f"AI озвучка игр: русская озвучка {names} | OFFEWS"
        desc = f"Бесплатная русская AI озвучка игр: {names}. Голоса по образцу оригинальных, эффекты как в игре, установка в один клик."
    lst = {"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": f"{v['title']} Russian voice-over", "url": f"{SITE_URL}{'en/' if en else ''}{v['slug']}/"}
        for k, v in enumerate(VOICEOVERS)]}
    head = head_tags(title, desc, path, lang, VOICEOVERS[0]["poster"], ld_script(lst, voice_faq_ld(lang)))
    cards = "".join(voice_card(v) for v in VOICEOVERS)
    body = f"""{header("../", path, lang)}

<main id="main" class="game-main">
  <section class="catalog voice-intro" aria-labelledby="voice-title">
    <div class="wrap">
      <div class="section-head reveal">
        <p class="eyebrow">{t("AI озвучка игр", "AI voice-over for games")}</p>
        <h1 id="voice-title">{t("Игры заговорят по-русски", "Games that speak Russian")}</h1>
        <p class="lead">{t("Русская озвучка для игр, у которых её нет. Нейросеть повторяет характер оригинальных голосов, а звук обработан как в самой игре: шлем, рация, помехи. Ставится и удаляется установщиком, оригинальные файлы игры не меняются.", "Russian dubbing for games that have none. A neural network keeps the character of the original voices, and the sound is processed like in the game itself: helmets, radio, static. An installer adds and removes it; the original game files stay unchanged.")}</p>
      </div>
      <div class="cards">{cards}
      </div>
    </div>
  </section>
{voice_howto()}
{support()}
{voice_faq()}
</main>
{footer("../")}"""
    write_page(("en/" if en else "") + f"{path}index.html", head, body, lang, depth=2 if en else 1)


def voice_teaser():
    v = VOICEOVERS[0]
    return f"""
  <section class="voice-teaser" aria-labelledby="voice-teaser-title">
    <div class="wrap">
      <a class="voice-teaser-panel reveal" href="{VOICE_SECTION}" style="--glow:{v["glow"]}">
        <span class="eyebrow">{t("Новый раздел", "New section")}</span>
        <h2 id="voice-teaser-title">{t("AI озвучка игр", "AI voice-over for games")}</h2>
        <p class="lead">{t(f"Русская озвучка {v['title']}: все реплики, голоса по образцу оригинальных, установка в один клик.", f"Russian dub for {v['title']}: every line, voices after the originals, one-click install.")}</p>
        <span class="btn btn-ghost">{t("Перейти к озвучке", "Open the section")}</span>
      </a>
    </div>
  </section>"""


def build():
    for lang in ("ru", "en"):
        total = home_page(lang)
        for tr in TRAINERS:
            game_page(tr, lang)
        voice_section_page(lang)
        for v in VOICEOVERS:
            voice_game_page(v, lang)
    pages = [("", max(tr["updated"] for tr in TRAINERS + VOICEOVERS))] + [(f"{tr['slug']}/", tr["updated"]) for tr in TRAINERS]
    pages += [(VOICE_SECTION, max(v["updated"] for v in VOICEOVERS))] + [(f"{v['slug']}/", v["updated"]) for v in VOICEOVERS]
    entries = []
    for path, mod in pages:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE_URL}{p}{path}"/>'
                       for l, p in (("ru", ""), ("en", "en/"), ("x-default", "")))
        for p in ("", "en/"):
            entries.append(f"  <url><loc>{SITE_URL}{p}{path}</loc><lastmod>{mod}</lastmod>{alts}</url>\n")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "".join(entries) + "</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n")
    with open(os.path.join(OUT, "assets", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><polygon points="24,3 42.2,13.5 42.2,34.5 24,45 5.8,34.5 5.8,13.5" '
                'fill="#2a1416" stroke="#c8262c" stroke-width="4"/><g fill="none" stroke="#eae7e2" stroke-width="4" stroke-linecap="round">'
                '<path d="M17.4 18.3a9.6 9.6 0 1 0 13.2 0"/><path d="M24 13.6v10.6"/></g></svg>')
    print("built", total, "functions,", len(entries), "pages")


if __name__ == "__main__":
    build()
