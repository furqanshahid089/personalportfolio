/**
 * Furqan Shahid — Portfolio server
 *
 * A small Node.js + Express server that:
 *   1. Serves the static site (index.html + the static/ assets)
 *   2. Exposes POST /api/contact to save contact-form submissions to
 *      messages.json (no database required)
 *
 * Run with:  npm start   (then open http://localhost:3000)
 */

"use strict";

const express = require("express");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = process.env.PORT || 3000;
const MESSAGES_FILE = path.join(__dirname, "messages.json");

// --- Middleware ------------------------------------------------------------
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve the static site from the project root (index.html, static/ assets).
app.use(express.static(__dirname));

// --- Helpers ---------------------------------------------------------------

/** Read all stored messages, returning [] if the file is missing/empty. */
function readMessages() {
  try {
    const raw = fs.readFileSync(MESSAGES_FILE, "utf8");
    const data = JSON.parse(raw);
    return Array.isArray(data) ? data : [];
  } catch {
    return [];
  }
}

/** Persist the messages array back to disk. */
function writeMessages(messages) {
  fs.writeFileSync(MESSAGES_FILE, JSON.stringify(messages, null, 2), "utf8");
}

/** Basic email format check. */
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// --- API: contact form -----------------------------------------------------
app.post("/api/contact", (req, res) => {
  const name = String(req.body.name || "").trim();
  const email = String(req.body.email || "").trim();
  const message = String(req.body.message || "").trim();

  // Server-side validation (never trust the client alone).
  if (!name) {
    return res.status(400).json({ ok: false, message: "Please enter your name." });
  }
  if (!isValidEmail(email)) {
    return res.status(400).json({ ok: false, message: "Please enter a valid email address." });
  }
  if (message.length < 10) {
    return res
      .status(400)
      .json({ ok: false, message: "Please enter a message of at least 10 characters." });
  }

  const messages = readMessages();
  messages.unshift({
    name,
    email,
    message,
    created_at: new Date().toISOString(),
  });

  try {
    writeMessages(messages);
  } catch (err) {
    console.error("Failed to save message:", err);
    return res
      .status(500)
      .json({ ok: false, message: "Could not save your message. Please try again later." });
  }

  return res.json({ ok: true, message: "Thanks, your message has been sent successfully." });
});

// --- Fallback: always return index.html for the root -----------------------
app.get("/", (_req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.listen(PORT, () => {
  console.log(`Portfolio running at http://localhost:${PORT}`);
});

module.exports = app;
