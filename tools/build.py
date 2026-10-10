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

# Download links: fill in once the files are on GitHub Releases. An empty link shows a
# disabled button.
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
        "download": "",
        "size_kb": 336,
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
        "download": "",
        "size_kb": 333,
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
        return (f'<a class="{cls}" href="{e(tr["download"])}">{POWER_SMALL}'
                f'{t("Скачать", "Download")}<small>v{tr["version"]} · {tr["size_kb"]} КБ</small></a>')
    return (f'<span class="{cls} is-off" aria-disabled="true">{POWER_SMALL}'
            f'{t("Скоро на GitHub", "Coming to GitHub")}<small>v{tr["version"]}</small></span>')


POWER_SMALL = ('<svg class="pw" viewBox="0 0 24 24" aria-hidden="true"><path d="M7.5 6.6a7.5 7.5 0 1 0 9 0" />'
               '<path d="M12 3v8" /></svg>')

EMBLEM = ('<svg class="emblem" viewBox="0 0 48 48" aria-hidden="true">'
          '<polygon class="hex" points="24,3 42.2,13.5 42.2,34.5 24,45 5.8,34.5 5.8,13.5" />'
          '<path class="ring" d="M17.4 18.3a9.6 9.6 0 1 0 13.2 0" /><path class="ring" d="M24 13.6v10.6" /></svg>')


def card(tr):
    n = count(tr)
    return f'''
      <article class="card">
        <a class="card-poster" href="#{tr["id"]}">
          <img src="{tr["poster"]}" alt="{e(tr["title"])}" width="480" height="720" loading="lazy">
          <span class="card-count">+{n}</span>
        </a>
        <div class="card-body">
          <h3><a href="#{tr["id"]}">{e(tr["title"])}</a></h3>
          <p class="card-about">{t(tr["about_ru"], tr["about_en"])}</p>
          <dl class="facts">
            <div><dt>{t("Трейнер", "Trainer")}</dt><dd class="mono">v{tr["version"]}</dd></div>
            <div><dt>{t("Версия игры", "Game version")}</dt><dd>{t(tr["game_build_ru"], tr["game_build_en"])}</dd></div>
          </dl>
          <div class="card-actions">
            {download_button(tr)}
            <a class="btn btn-ghost" href="#{tr["id"]}">{t("Все функции", "All functions")}</a>
          </div>
        </div>
      </article>'''


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
                f'<li>{keycap(i["key"])}<span class="fn">{t(i["ru"], i["en"])}</span></li>' for i in g["items"])
            wide = " wide" if any(i["key"].count("+") >= 2 for i in g["items"]) else ""
            inner.append(f'<section class="group{wide}"><h4>{t(g["ru"], g["en"])}</h4><ul>{rows}</ul></section>')
        head = f'<h3 class="page-tab">{t(PAGE_RU[page], PAGE_EN[page])}</h3>' if len(pages) > 1 else ""
        blocks.append(head + '<div class="groups">' + "".join(inner) + "</div>")
    shots = "".join(
        f'<figure><img src="{s}" alt="{e(ru)}" loading="lazy"><figcaption>{t(ru, en)}</figcaption></figure>'
        for s, ru, en in tr["shots"])
    word_ru = plural_ru(n, "функция", "функции", "функций")
    return f'''
    <section class="trainer" id="{tr["id"]}" aria-labelledby="{tr["id"]}-title">
      <div class="wrap trainer-grid">
        <aside class="trainer-side">
          <img class="side-poster" src="{tr["poster"]}" alt="" width="480" height="720" loading="lazy">
          <dl class="side-facts">
            <div><dt>{t("Проверено на версии игры", "Tested on game version")}</dt><dd class="brass">{t(tr["game_build_ru"], tr["game_build_en"])}</dd></div>
            <div><dt>{t("Версия трейнера", "Trainer version")}</dt><dd class="mono">v{tr["version"]}</dd></div>
            <div><dt>{t("Обновлён", "Updated")}</dt><dd>{t(date_ru(tr["updated"]), date_en(tr["updated"]))}</dd></div>
            <div><dt>{t("Режим", "Mode")}</dt><dd>{t(tr["mode_ru"], tr["mode_en"])}</dd></div>
            <div><dt>{t("Нужно", "Requires")}</dt><dd>Windows 10/11, .NET Framework 4.8</dd></div>
          </dl>
        </aside>
        <div class="trainer-main">
          <p class="eyebrow">{t(f"Трейнер · {n} {word_ru}", f"Trainer · {n} functions")}</p>
          <h2 id="{tr["id"]}-title">{e(tr["title"])}</h2>
          <p class="lead">{t(tr["about_ru"], tr["about_en"])}</p>
          <div class="trainer-actions">{download_button(tr, big=True)}</div>
          <div class="shots shots-{len(tr["shots"])}">{shots}</div>
          {"".join(blocks)}
          <p class="note">{t("Горячие клавиши указаны по умолчанию, в трейнере их можно переназначить.", "Default hotkeys shown; you can rebind them in the trainer.")}</p>
        </div>
      </div>
    </section>'''


def build():
    total = sum(count(tr) for tr in TRAINERS)
    cards = "".join(card(tr) for tr in TRAINERS)
    details = "".join(detail(tr) for tr in TRAINERS)
    head = f'''<title>OFFEWS Trainers</title>
<meta name="description" content="Трейнеры OFFEWS для одиночных игр: включаются кликом или горячей клавишей, без нампада, на русском и английском.">
<meta name="theme-color" content="#111114">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600&family=JetBrains+Mono:wght@500;600&family=Unbounded:wght@500;700;800&display=swap">
<style>{open(os.path.join(ROOT, "style.css"), encoding="utf-8").read()}</style>'''
    body = f'''<a class="skip" href="#catalog">{t("К трейнерам", "Skip to trainers")}</a>
<header class="top">
  <div class="wrap top-row">
    <a class="brand" href="#" aria-label="OFFEWS">{EMBLEM}<span class="word"><b>OFF</b>EWS<small>TRAINERS</small></span></a>
    <nav class="nav" aria-label="{e("Разделы")}">
      <a href="#catalog">{t("Трейнеры", "Trainers")}</a>
      <a href="#howto">{t("Как пользоваться", "How to use")}</a>
      <a href="#faq">{t("Вопросы", "FAQ")}</a>
    </nav>
    <div class="lang" role="group" aria-label="Language">
      <button type="button" id="lang-ru" data-set-lang="ru" aria-pressed="true">RU</button>
      <button type="button" id="lang-en" data-set-lang="en" aria-pressed="false">EN</button>
    </div>
  </div>
</header>

<main>
  <section class="hero">
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <p class="eyebrow">{t("Трейнеры для одиночных игр", "Trainers for single-player games")}</p>
        <h1>{t("Включай читы кликом. Нампад не нужен.", "Switch cheats on with a click. No numpad needed.")}</h1>
        <p class="lead">{t("Трейнер сам находит запущенную игру. Функции включаются в окне или горячими клавишами, клавиши можно переназначить. Интерфейс на русском и английском.", "The trainer finds the running game by itself. Turn functions on in its window or with hotkeys you can rebind. Russian and English interface.")}</p>
        <div class="hero-stats">
          <div><b>{len(TRAINERS)}</b>{t(plural_ru(len(TRAINERS), "трейнер", "трейнера", "трейнеров"), "trainers")}</div>
          <div><b>{total}</b>{t(plural_ru(total, "функция", "функции", "функций"), "functions")}</div>
          <div><b>0</b>{t("нужно установить", "to install")}</div>
        </div>
        <a class="btn btn-primary btn-big" href="#catalog">{POWER_SMALL}{t("Выбрать игру", "Pick a game")}</a>
      </div>
      <figure class="hero-shot">
        <img src="{TRAINERS[0]["shots"][0][0]}" alt="{e("Окно трейнера " + TRAINERS[0]["title"])}" width="1174" height="628">
        <figcaption>{t("Так выглядит трейнер: слева игра и её версия, справа функции с горячими клавишами.", "This is the trainer: the game and its version on the left, functions with hotkeys on the right.")}</figcaption>
      </figure>
    </div>
  </section>

  <section class="catalog" id="catalog" aria-labelledby="catalog-title">
    <div class="wrap">
      <div class="section-head">
        <h2 id="catalog-title">{t("Трейнеры", "Trainers")}</h2>
        <p>{t("Новые игры появляются по мере выхода. Каждый трейнер проверен на указанной версии игры.", "New games are added as they come out. Each trainer is tested on the game version shown.")}</p>
      </div>
      <div class="cards">{cards}
      </div>
    </div>
  </section>
{details}
  <section class="howto" id="howto" aria-labelledby="howto-title">
    <div class="wrap">
      <div class="section-head"><h2 id="howto-title">{t("Как пользоваться", "How to use")}</h2></div>
      <ol class="steps">
        <li><b>{t("Скачайте трейнер", "Download the trainer")}</b><p>{t("Это один exe-файл, устанавливать ничего не нужно. Положите его в любую папку.", "It is a single exe, nothing to install. Put it in any folder.")}</p></li>
        <li><b>{t("Запустите трейнер и игру", "Start the trainer and the game")}</b><p>{t("В любом порядке: трейнер сам найдёт игру и подключится.", "In any order: the trainer finds the game and connects.")}</p></li>
        <li><b>{t("Дождитесь «подключено»", "Wait for “connected”")}</b><p>{t("Статус виден внизу окна трейнера. Загрузите сохранение или главу.", "The status is at the bottom of the trainer window. Load a save or a chapter.")}</p></li>
        <li><b>{t("Включайте функции", "Turn functions on")}</b><p>{t("Кликом по переключателю или горячей клавишей прямо в игре.", "Click a switch, or press its hotkey right in the game.")}</p></li>
      </ol>
    </div>
  </section>

  <section class="faq" id="faq" aria-labelledby="faq-title">
    <div class="wrap">
      <div class="section-head"><h2 id="faq-title">{t("Вопросы", "FAQ")}</h2></div>
      <div class="faq-list">
        <details open><summary>{t("Антивирус ругается на трейнер. Это вирус?", "My antivirus flags the trainer. Is it a virus?")}</summary>
          <p>{t("Нет. Трейнер меняет память игры, и некоторые антивирусы по эвристике считают это подозрительным. Обычно срабатывает один антивирус из семидесяти. Трейнер ничего не скачивает, не устанавливает и не отправляет в сеть.", "No. The trainer changes the game’s memory, and some antivirus heuristics find that suspicious. Usually one scanner out of seventy reacts. The trainer downloads, installs and sends nothing.")}</p></details>
        <details><summary>{t("Можно ли играть с трейнером по сети?", "Can I use a trainer online?")}</summary>
          <p>{t("Нет. Трейнеры сделаны только для одиночной игры. Если трейнер видит античит или сетевую игру, функции не включаются.", "No. The trainers are for single-player only. If a trainer detects an anti-cheat or an online session, functions stay off.")}</p></details>
        <details><summary>{t("Игра обновилась, и трейнер перестал работать", "The game updated and the trainer stopped working")}</summary>
          <p>{t("Сравните версию игры в окне трейнера с проверенной. Если они различаются, дождитесь обновления трейнера.", "Compare the game version in the trainer window with the tested one. If they differ, wait for a trainer update.")}</p></details>
        <details><summary>{t("Трейнер не запускается", "The trainer does not start")}</summary>
          <p>{t("Нужен .NET Framework 4.8. В Windows 10 и 11 он уже есть, в старых системах его можно поставить с сайта Microsoft.", "It needs .NET Framework 4.8. Windows 10 and 11 already have it; on older systems install it from Microsoft.")}</p></details>
        <details><summary>{t("Не испортит ли трейнер сохранения?", "Can the trainer break my saves?")}</summary>
          <p>{t("Функции меняют игру только пока включены. Перед изменением денег, предметов и опыта на всякий случай сделайте копию сохранений.", "Functions only change the game while they are on. Before changing money, items or experience, back up your saves just in case.")}</p></details>
      </div>
    </div>
  </section>
</main>

<footer class="foot">
  <div class="wrap foot-row">
    <a class="brand brand-small" href="#" aria-label="OFFEWS">{EMBLEM}<span class="word"><b>OFF</b>EWS</span></a>
    <p>{t("Трейнеры для одиночных игр. Используйте их только в одиночной игре.", "Trainers for single-player games. Use them in single-player only.")}</p>
    <p class="mono">© 2026 OFFEWS</p>
  </div>
</footer>
<script>{open(os.path.join(ROOT, "site.js"), encoding="utf-8").read()}</script>'''

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
