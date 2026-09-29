# Furqan Shahid — Personal Portfolio

A modern, responsive personal portfolio for **Furqan Shahid** — a BS Data Science
student and developer from Lahore, Pakistan. Built as a fast, static website with
plain **HTML, CSS, and JavaScript** (no framework, no backend).

## Overview

A single-page portfolio with sections for Home, About, Skills, Projects,
Experience, Services, Education, Resume, and Contact. It showcases Furqan's
skills and projects and gives visitors easy ways to get in touch.

## Features

- Premium **Midnight Indigo** theme — deep navy base with an indigo→cyan gradient
- Dark / light mode toggle (remembers your choice)
- Sticky navbar, mobile hamburger menu, smooth scrolling, active-section highlight
- Reveal-on-scroll animations that respect `prefers-reduced-motion`
- Interactive skill badges, project cards, experience, services and timeline
- Contact form that opens your email client (via `mailto`) — no backend needed
- SEO: title/description, Open Graph, Twitter cards, Person schema (JSON-LD), favicon
- Fast and lightweight: no build step, deferred JS, `font-display: swap`

## Tech Stack

- **HTML5** — semantic, accessible markup
- **CSS3** — custom properties, Grid & Flexbox, responsive, glassmorphism
- **JavaScript (ES6)** — vanilla, no dependencies
- Google Fonts (Inter, Space Grotesk) and Font Awesome icons via CDN

## Project Structure

```text
personal portfolio/
├── index.html                 # The whole site (all sections)
├── static/
│   ├── css/style.css          # Styles + Midnight Indigo theme
│   ├── js/script.js           # Nav, theme, animations, contact
│   ├── icons/favicon.svg
│   ├── images/og-image.svg
│   └── assets/                # Resume PDF, etc.
├── screenshots/               # Add mobile/tablet/desktop captures here
└── README.md
```

## Run Locally

It's a static site — just open `index.html` in a browser. For a local server
(recommended, so relative paths and the favicon load correctly):

```bash
# Python (any version)
python -m http.server 8000
# then open http://localhost:8000
```

Or use the VS Code **Live Server** extension.

## Deploy to Vercel

1. Push this folder to a GitHub repository.
2. On [vercel.com](https://vercel.com), click **Add New → Project** and import the repo.
3. Framework preset: **Other** (it's a plain static site — no build command needed).
4. Click **Deploy**. Vercel serves `index.html` and the `static/` assets directly.

No environment variables, no server, no database — nothing can crash at runtime.

You can also deploy the same way on **Netlify** or **GitHub Pages**.

## Editing Content

Everything is in plain HTML/CSS/JS, so you can edit freely:

- **Text, projects, skills, experience** — edit `index.html`
- **Colors, spacing, theme** — edit `static/css/style.css` (see the `:root` and
  `[data-theme]` variables at the top)
- **Behavior (nav, theme, contact)** — edit `static/js/script.js`
- **Resume** — replace `static/assets/Furqan_Shahid_CV.pdf` with your own file
- **Contact email** — update `CONTACT_EMAIL` in `static/js/script.js` and the
  `mailto:` links in `index.html`

## Contact

- Email: furqanshahid089@gmail.com
- GitHub: https://github.com/furqanshahid089
- LinkedIn: https://www.linkedin.com/in/furqan-shahid9878
- WhatsApp: +92 308 9369211

## Author

**Furqan Shahid** — BS Data Science Student | Developer | AI & Automation Enthusiast
