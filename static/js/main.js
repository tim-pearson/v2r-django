(function () {
  "use strict";

  /* ---------- Mobile drawer ---------- */
  var menuBtn = document.getElementById("menu-btn");
  var drawer = document.getElementById("drawer");
  var overlay = document.getElementById("drawer-overlay");

  function openDrawer() {
    drawer.classList.add("is-open");
    drawer.setAttribute("aria-hidden", "false");
    overlay.hidden = false;
    menuBtn.setAttribute("aria-expanded", "true");
    menuBtn.setAttribute("aria-label", "Close menu");
  }

  function closeDrawer() {
    drawer.classList.remove("is-open");
    drawer.setAttribute("aria-hidden", "true");
    overlay.hidden = true;
    menuBtn.setAttribute("aria-expanded", "false");
    menuBtn.setAttribute("aria-label", "Open menu");
  }

  if (menuBtn && drawer && overlay) {
    menuBtn.addEventListener("click", function () {
      drawer.classList.contains("is-open") ? closeDrawer() : openDrawer();
    });
    overlay.addEventListener("click", closeDrawer);
    drawer.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeDrawer);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeDrawer();
    });
  }

  /* ---------- Hero crossfade ---------- */
  var heroSlides = document.querySelectorAll(".hero-slide");
  var heroDots = document.querySelectorAll("#hero-dots .dot");
  if (heroSlides.length > 1) {
    var current = 0;
    function showHero(index) {
      heroSlides[current].classList.remove("is-active");
      if (heroDots[current]) heroDots[current].classList.remove("is-active");
      current = index;
      heroSlides[current].classList.add("is-active");
      if (heroDots[current]) heroDots[current].classList.add("is-active");
    }
    heroDots.forEach(function (dot, i) {
      dot.addEventListener("click", function () { showHero(i); });
    });
    setInterval(function () { showHero((current + 1) % heroSlides.length); }, 5000);
  }

  /* ---------- Testimonials carousel ---------- */
  var track = document.getElementById("t-track");
  var tDotsWrap = document.getElementById("t-dots");
  if (track && tDotsWrap) {
    var cards = Array.prototype.slice.call(track.children);
    if (cards.length) {
      var GAP = 12;
      var page = 0;
      var dotEls = [];

      function perView() {
        return window.matchMedia("(min-width: 900px)").matches ? 3 : 1;
      }

      function go(p) {
        var view = perView();
        var pages = Math.max(1, Math.ceil(cards.length / view));
        page = p >= pages ? 0 : p;
        var w = cards[0].offsetWidth + GAP;
        track.style.transform = "translateX(" + -page * view * w + "px)";
        dotEls.forEach(function (d, i) { d.classList.toggle("is-active", i === page); });
        cards.forEach(function (c) { c.classList.remove("is-active"); });
        var center = page * view + Math.floor((view - 1) / 2);
        if (cards[center]) cards[center].classList.add("is-active");
      }

      var pages = Math.max(1, Math.ceil(cards.length / perView()));
      for (var i = 0; i < pages; i++) {
        var d = document.createElement("span");
        d.className = "dot";
        d.setAttribute("role", "button");
        d.addEventListener("click", (function (idx) { return function () { go(idx); }; })(i));
        tDotsWrap.appendChild(d);
        dotEls.push(d);
      }
      window.addEventListener("resize", function () { go(page); });
      go(0);
      if (pages > 1) setInterval(function () { go(page + 1); }, 6000);
    }
  }

  /* ---------- Back to top ---------- */
  var toTop = document.querySelector(".back-to-top");
  if (toTop) {
    window.addEventListener("scroll", function () {
      toTop.classList.toggle("is-visible", window.scrollY > 400);
    });
  }

  /* ---------- Scrollspy (nav active state) ---------- */
  var navLinks = document.querySelectorAll(".main-nav a, .drawer-nav a");
  if (navLinks.length) {
    var ids = ["home", "about", "services", "who", "experience", "contact"];
    function spy() {
      var active = "home";
      ids.forEach(function (id) {
        var el = document.getElementById(id);
        if (el && el.getBoundingClientRect().top <= 140) active = id;
      });
      navLinks.forEach(function (a) {
        a.classList.toggle("active", a.getAttribute("href").slice(-1 - active.length) === "#" + active);
      });
    }
    window.addEventListener("scroll", spy, { passive: true });
    spy();
  }
})();