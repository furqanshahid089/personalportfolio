# Furqan Shahid — Personal Portfolio

A modern, responsive personal portfolio for **Furqan Shahid** — a BS Data Science
student and developer from Lahore, Pakistan. Built with **HTML, CSS, and
JavaScript** on the front end and a small **Node.js + Express** server on the
back end (no Python, no database).

## Overview

A single-page portfolio with sections for Home, About, Skills, Projects,
Experience, Services, Education, Resume, and Contact. The Express server serves
the site and provides a contact API that stores submissions in `messages.json`.

## Features

- Premium **Midnight Indigo** theme — deep navy base with an indigo→cyan gradient
- Dark / light mode toggle (remembers your choice)
- Sticky navbar, mobile hamburger menu, smooth scrolling, active-section highlight
- Reveal-on-scroll animations that respect `prefers-reduced-motion`
- Interactive skill badges, project cards, experience, services and timeline
- **Working contact form** — submits to the Node API and saves to `messages.json`
  (falls back to opening your email client if no server is running)
- SEO: title/description, Open Graph, Twitter cards, Person schema (JSON-LD), favicon

## Tech Stack

- **Front end:** HTML5, CSS3 (Grid & Flexbox, custom properties), vanilla JavaScript
- **Back end:** Node.js + Express
- **Storage:** `messages.json` (simple file-based, no database)
- Google Fonts (Inter, Space Grotesk) and Font Awesome via CDN

## Project Structure

```text
personal portfolio/
├── server.js                  # Express server + contact API
├── package.json               # Node dependencies & scripts
├── index.html                 # The whole site (all sections)
├── static/
│   ├── css/style.css          # Styles + Midnight Indigo theme
│   ├── js/script.js           # Nav, theme, animations, contact fetch
│   ├── icons/favicon.svg
│   ├── images/og-image.svg
│   └── assets/                # Resume PDF, etc.
├── messages.json              # Created at runtime (git-ignored)
├── screenshots/
└── README.md
```

## Setup & Run

Requires **Node.js 18+**.

```bash
# 1. Install dependencies
npm install

# 2. Start the server
npm start

# 3. Open the site
#    http://localhost:3000
```

Submit the contact form and the message is appended to `messages.json` in the
project root.

## Contact API

`POST /api/contact` — JSON body: `{ "name", "email", "message" }`

- Validates the input (name required, valid email, message ≥ 10 chars)
- Appends the message to `messages.json`
- Returns `{ ok: true, message }` on success or `{ ok: false, message }` on error

## Deploy

The site can be deployed to any Node host (Render, Railway, Fly.io, a VPS, etc.):

1. Push the repository to the host.
2. Ensure the start command is `npm start` and Node 18+ is available.
3. The host provides a `PORT` environment variable, which the server reads
   automatically.

> **Note:** On serverless/ephemeral hosts, `messages.json` is not persistent.
> For durable storage, swap the file read/write in `server.js` for a database
> or an email service.

## Editing Content

- **Text, projects, skills, experience** — edit `index.html`
- **Colors, spacing, theme** — edit `static/css/style.css` (`:root` / `[data-theme]`)
- **Behavior (nav, theme, contact)** — edit `static/js/script.js`
- **Contact API / storage** — edit `server.js`
- **Resume** — replace `static/assets/Furqan_Shahid_CV.pdf`

## Contact

- Email: furqanshahid089@gmail.com
- GitHub: https://github.com/furqanshahid089
- LinkedIn: https://www.linkedin.com/in/furqan-shahid9878
- WhatsApp: +92 308 9369211

## Author

**Furqan Shahid** — BS Data Science Student | Developer | AI & Automation Enthusiast
