(function () {
  var root = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---- language -----------------------------------------------------------------------------
  var buttons = document.querySelectorAll("[data-set-lang]");
  function apply(lang) {
    root.setAttribute("data-lang", lang);
    root.setAttribute("lang", lang);
    for (var i = 0; i < buttons.length; i++)
      buttons[i].setAttribute("aria-pressed", String(buttons[i].getAttribute("data-set-lang") === lang));
  }
  var saved = null;
  try { saved = localStorage.getItem("offews-lang"); } catch (e) {}
  if (saved !== "ru" && saved !== "en")
    saved = (navigator.language || "ru").toLowerCase().indexOf("ru") === 0 ? "ru" : "en";
  apply(saved);
  for (var i = 0; i < buttons.length; i++)
    buttons[i].addEventListener("click", function () {
      var lang = this.getAttribute("data-set-lang");
      if (lang === root.getAttribute("data-lang")) return;
      if (document.startViewTransition && !reduce) document.startViewTransition(function () { apply(lang); });
      else apply(lang);
      try { localStorage.setItem("offews-lang", lang); } catch (e) {}
    });

  // ---- header turns solid after the hero starts scrolling away --------------------------------
  var top = document.getElementById("top");
  function onScroll() { top.classList.toggle("is-solid", window.scrollY > 40); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // ---- download counters: summed from GitHub release assets, cached for two minutes ----------
  var slots = document.querySelectorAll("[data-dl]");
  function pluralRu(n, one, few, many) {
    if (n % 10 === 1 && n % 100 !== 11) return one;
    if (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14)) return few;
    return many;
  }
  function showCounts(releases) {
    for (var i = 0; i < slots.length; i++) {
      var prefix = slots[i].getAttribute("data-dl"), n = 0;
      for (var r = 0; r < releases.length; r++)
        for (var a = 0; a < (releases[r].assets || []).length; a++)
          if (releases[r].assets[a].name.indexOf(prefix) === 0) n += releases[r].assets[a].download_count || 0;
      var num = n.toLocaleString("ru-RU");
      slots[i].innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11M7 10.5l5 5 5-5M5 20h14"/></svg><b>' + num + '</b>' +
        '<span lang="ru">' + pluralRu(n, "скачивание", "скачивания", "скачиваний") + '</span>' +
        '<span lang="en">' + (n === 1 ? "download" : "downloads") + '</span>';
      slots[i].hidden = false;
    }
  }
  // GitHub's API allows 60 anonymous requests an hour per IP, and visitors behind one mobile or
  // provider address share that. The site's own downloads.json (refreshed by a workflow every half
  // hour) is shown first, then replaced by live numbers when the API answers.
  function slim(data) {
    return data.map(function (r) { return { assets: (r.assets || []).map(function (a) { return { name: a.name, download_count: a.download_count }; }) }; });
  }
  if (slots.length && window.fetch) {
    var cached = null;
    try { cached = JSON.parse(sessionStorage.getItem("offews-dl")); } catch (e) {}
    if (cached && Date.now() - cached.at < 120000) showCounts(cached.data);
    else {
      var live = false;
      fetch("/downloads.json", { cache: "no-cache" })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (data) { if (!live) showCounts(data); })
        .catch(function () {});
      fetch("https://api.github.com/repos/IvanGri2/OFFEWS-Trainers/releases?per_page=100")
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (data) {
          var s = slim(data);
          live = true;
          try { sessionStorage.setItem("offews-dl", JSON.stringify({ at: Date.now(), data: s })); } catch (e) {}
          showCounts(s);
        })
        .catch(function () {});
    }
  }

  // ---- comments: giscus (GitHub Discussions), loaded when the section comes near ------------
  var commentSlots = document.querySelectorAll(".giscus-slot");
  function loadComments(slot) {
    if (slot.getAttribute("data-loaded")) return;
    slot.setAttribute("data-loaded", "1");
    var s = document.createElement("script");
    s.src = "https://giscus.app/client.js";
    s.async = true;
    s.crossOrigin = "anonymous";
    var attrs = {
      "data-repo": slot.getAttribute("data-repo"), "data-repo-id": slot.getAttribute("data-repo-id"),
      "data-category": slot.getAttribute("data-category"), "data-category-id": slot.getAttribute("data-category-id"),
      "data-mapping": "specific", "data-term": slot.getAttribute("data-term"), "data-strict": "1",
      "data-reactions-enabled": "1", "data-emit-metadata": "0", "data-input-position": "top",
      "data-theme": "transparent_dark", "data-lang": root.getAttribute("data-lang") === "en" ? "en" : "ru", "data-loading": "lazy"
    };
    for (var k in attrs) s.setAttribute(k, attrs[k]);
    slot.appendChild(s);
  }
  if (commentSlots.length) {
    if ("IntersectionObserver" in window) {
      var co = new IntersectionObserver(function (en) {
        for (var i = 0; i < en.length; i++) if (en[i].isIntersecting) { loadComments(en[i].target); co.unobserve(en[i].target); }
      }, { rootMargin: "600px 0px" });
      for (var cs = 0; cs < commentSlots.length; cs++) co.observe(commentSlots[cs]);
    } else for (var cs2 = 0; cs2 < commentSlots.length; cs2++) loadComments(commentSlots[cs2]);
  }

  // ---- comments: Cusdis (no account), all trainer threads rendered once its script is in -------
  var cusdisSlots = document.querySelectorAll(".cusdis-slot");
  if (cusdisSlots.length) {
    if (root.getAttribute("data-lang") !== "en")
      window.CUSDIS_LOCALE = window.CUSIDS_LOCALE = {
        powered_by: "Комментарии Cusdis", post_comment: "Отправить", loading: "Загрузка",
        email: "Email (необязательно)", nickname: "Имя", reply_placeholder: "Ответ...", reply_btn: "Ответить",
        sending: "отправка...", mod_badge: "АВТОР", content_is_required: "Напиши комментарий",
        nickname_is_required: "Укажи имя", comment_has_been_sent: "Комментарий отправлен и появится после проверки."
      };
    var cu = document.createElement("script");
    cu.src = "https://cusdis.com/js/cusdis.es.js";
    cu.async = true;
    cu.onload = function () {
      if (typeof window.renderCusdis !== "function") return;
      for (var i = 0; i < cusdisSlots.length; i++) window.renderCusdis(cusdisSlots[i]);
    };
    document.body.appendChild(cu);
  }

  if (reduce) return;

  // ---- hero stage follows the pointer -------------------------------------------------------
  var hero = document.querySelector(".hero");
  var stage = document.querySelector(".stage-inner");
  if (hero && stage && window.matchMedia("(pointer: fine)").matches) {
    hero.addEventListener("pointermove", function (e) {
      var r = hero.getBoundingClientRect();
      stage.style.setProperty("--mx", ((e.clientX - r.left) / r.width - 0.5).toFixed(3));
      stage.style.setProperty("--my", ((e.clientY - r.top) / r.height - 0.5).toFixed(3));
    });
    hero.addEventListener("pointerleave", function () { stage.style.setProperty("--mx", 0); stage.style.setProperty("--my", 0); });
  }

  // ---- cards tilt toward the pointer with a moving glare ------------------------------------
  var cards = document.querySelectorAll("[data-tilt]");
  for (var c = 0; c < cards.length; c++) (function (card) {
    card.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse") return;
      var r = card.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      card.style.setProperty("--ry", ((x - 0.5) * 12).toFixed(2) + "deg");
      card.style.setProperty("--rx", ((0.5 - y) * 10).toFixed(2) + "deg");
      card.style.setProperty("--gx", (x * 100).toFixed(1) + "%");
      card.style.setProperty("--gy", (y * 100).toFixed(1) + "%");
    });
    card.addEventListener("pointerleave", function () {
      card.style.setProperty("--rx", "0deg"); card.style.setProperty("--ry", "0deg");
    });
  })(cards[c]);

  // ---- embers rising through the hero -------------------------------------------------------
  var canvas = document.querySelector(".embers");
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext("2d"), w = 0, h = 0, dpr = Math.min(window.devicePixelRatio || 1, 2), parts = [], running = true;
  function size() {
    w = canvas.clientWidth; h = canvas.clientHeight;
    canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function spawn(initial) {
    return {
      x: Math.random() * w,
      y: initial ? Math.random() * h : h + 10,
      r: 0.6 + Math.random() * 2.2,
      vy: 0.25 + Math.random() * 0.9,
      vx: (Math.random() - 0.5) * 0.3,
      phase: Math.random() * Math.PI * 2,
      life: 0.4 + Math.random() * 0.6,
      hue: 8 + Math.random() * 28
    };
  }
  size();
  var count = Math.round(Math.min(90, w / 14));
  for (var p = 0; p < count; p++) parts.push(spawn(true));
  window.addEventListener("resize", size);
  if ("IntersectionObserver" in window)
    new IntersectionObserver(function (en) { running = en[0].isIntersecting; if (running) frame(); }).observe(canvas);
  function frame() {
    if (!running) return;
    ctx.clearRect(0, 0, w, h);
    ctx.globalCompositeOperation = "lighter";
    for (var i = 0; i < parts.length; i++) {
      var q = parts[i];
      q.phase += 0.02;
      q.y -= q.vy;
      q.x += q.vx + Math.sin(q.phase) * 0.35;
      var fade = Math.max(0, Math.min(1, q.y / h)) * q.life;
      var g = ctx.createRadialGradient(q.x, q.y, 0, q.x, q.y, q.r * 4);
      g.addColorStop(0, "hsla(" + q.hue + ",100%,65%," + fade + ")");
      g.addColorStop(1, "hsla(" + q.hue + ",100%,50%,0)");
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(q.x, q.y, q.r * 4, 0, Math.PI * 2); ctx.fill();
      if (q.y < -20) parts[i] = spawn(false);
    }
    requestAnimationFrame(frame);
  }
  frame();
})();
