/* ==========================================================================
   Furqan Shahid — Portfolio interactions
   Vanilla JS, no dependencies. Handles theme, navigation, scroll behaviour,
   reveal animations and the AJAX contact form.
   ========================================================================== */
(function () {
  "use strict";

  const root = document.documentElement;
  const header = document.querySelector(".site-header");

  /* ---------------------------------------------------------------------
     1. Theme toggle (persisted in localStorage, respects OS preference)
     --------------------------------------------------------------------- */
  const themeToggle = document.querySelector(".theme-toggle");
  const themeIcon = themeToggle ? themeToggle.querySelector("i") : null;

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    if (themeIcon) {
      themeIcon.className = theme === "dark" ? "fa-solid fa-moon" : "fa-solid fa-sun";
    }
  }

  const savedTheme = localStorage.getItem("theme");
  const prefersLight = window.matchMedia("(prefers-color-scheme: light)").matches;
  applyTheme(savedTheme || (prefersLight ? "light" : "dark"));

  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      applyTheme(next);
      localStorage.setItem("theme", next);
    });
  }

  /* ---------------------------------------------------------------------
     2. Mobile navigation (hamburger menu)
     --------------------------------------------------------------------- */
  const menuToggle = document.querySelector(".menu-toggle");
  const navMenu = document.getElementById("nav-menu");

  function closeMenu() {
    if (!navMenu) return;
    navMenu.classList.remove("open");
    if (menuToggle) menuToggle.setAttribute("aria-expanded", "false");
  }

  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", function () {
      const open = navMenu.classList.toggle("open");
      menuToggle.setAttribute("aria-expanded", String(open));
      const icon = menuToggle.querySelector("i");
      if (icon) icon.className = open ? "fa-solid fa-xmark" : "fa-solid fa-bars";
    });

    navMenu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        closeMenu();
        const icon = menuToggle.querySelector("i");
        if (icon) icon.className = "fa-solid fa-bars";
      });
    });
  }

  /* ---------------------------------------------------------------------
     3. Header shadow + active section highlighting on scroll
     --------------------------------------------------------------------- */
  const sections = Array.from(document.querySelectorAll("main section[id]"));
  const navLinks = Array.from(document.querySelectorAll(".nav-links a"));
  const scrollTopBtn = document.querySelector(".scroll-top");

  function onScroll() {
    const y = window.scrollY;

    if (header) header.classList.toggle("scrolled", y > 8);
    if (scrollTopBtn) scrollTopBtn.classList.toggle("show", y > 500);

    // Active section: the last section whose top has passed the offset.
    let currentId = sections.length ? sections[0].id : "";
    const offset = 120;
    for (const section of sections) {
      if (section.offsetTop - offset <= y) currentId = section.id;
    }
    navLinks.forEach(function (link) {
      link.classList.toggle("active", link.getAttribute("href") === "#" + currentId);
    });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (scrollTopBtn) {
    scrollTopBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------------------------------------------------------------------
     4. Reveal-on-scroll animations (IntersectionObserver)
     --------------------------------------------------------------------- */
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach(function (el) { observer.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("visible"); });
  }

  /* ---------------------------------------------------------------------
     5. Footer year
     --------------------------------------------------------------------- */
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* ---------------------------------------------------------------------
     6. Contact form — client validation + async submission
     --------------------------------------------------------------------- */
  const form = document.getElementById("contact-form");
  if (!form) return;

  const statusEl = form.querySelector(".form-status");

  function getCookie(name) {
    const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return match ? decodeURIComponent(match[2]) : null;
  }

  function setError(fieldId, message) {
    const errEl = document.getElementById(fieldId + "-error");
    const field = document.getElementById(fieldId);
    if (errEl) errEl.textContent = message || "";
    if (field && field.parentElement) {
      field.parentElement.classList.toggle("has-error", Boolean(message));
    }
  }

  function validate() {
    let ok = true;
    const name = form.name.value.trim();
    const email = form.email.value.trim();
    const message = form.message.value.trim();

    setError("name", "");
    setError("email", "");
    setError("message", "");

    if (!name) { setError("name", "Please enter your name."); ok = false; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError("email", "Please enter a valid email address."); ok = false;
    }
    if (message.length < 10) {
      setError("message", "Please enter a message of at least 10 characters."); ok = false;
    }
    return ok;
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    if (statusEl) { statusEl.textContent = ""; statusEl.className = "form-status"; }
    if (!validate()) return;

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalHTML = submitBtn ? submitBtn.innerHTML : "";
    if (submitBtn) { submitBtn.disabled = true; submitBtn.innerHTML = "Sending…"; }

    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken") || "",
          "X-Requested-With": "XMLHttpRequest",
        },
        body: new FormData(form),
      });
      const data = await response.json();

      if (statusEl) {
        statusEl.textContent = data.message;
        statusEl.className = "form-status " + (data.ok ? "success" : "error");
      }
      if (data.ok) form.reset();
    } catch (err) {
      if (statusEl) {
        statusEl.textContent = "Something went wrong. Please try again.";
        statusEl.className = "form-status error";
      }
    } finally {
      if (submitBtn) { submitBtn.disabled = false; submitBtn.innerHTML = originalHTML; }
    }
  });
})();
