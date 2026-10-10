(function () {
  var root = document.documentElement;
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
      apply(lang);
      try { localStorage.setItem("offews-lang", lang); } catch (e) {}
    });
})();
