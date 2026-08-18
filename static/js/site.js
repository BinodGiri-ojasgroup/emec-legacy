/**
 * EMEC — minimal site interactions.
 * Two responsibilities only: (1) draw-in the signature trace dividers /
 * reveal sections as they enter the viewport, (2) persist the light/dark
 * mode preference. Everything respects prefers-reduced-motion.
 */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // --- Theme toggle ---------------------------------------------------
  var THEME_KEY = "emec-theme";
  function applyTheme(theme) {
    document.documentElement.classList.toggle("light", theme === "light");
  }
  var saved = localStorage.getItem(THEME_KEY);
  if (saved) applyTheme(saved);

  document.addEventListener("click", function (e) {
    var toggle = e.target.closest("[data-theme-toggle]");
    if (!toggle) return;
    var next = document.documentElement.classList.contains("light") ? "dark" : "light";
    applyTheme(next);
    localStorage.setItem(THEME_KEY, next);
  });

  // --- Scroll reveal + trace draw-in -----------------------------------
  if (reduceMotion || !("IntersectionObserver" in window)) return;

  var revealTargets = document.querySelectorAll("[data-reveal], [data-trace]");
  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-revealed");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );
  revealTargets.forEach(function (el) {
    observer.observe(el);
  });
})();
