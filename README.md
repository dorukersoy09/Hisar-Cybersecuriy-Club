# Phishing-awareness lesson — teaching package

A classroom lesson that shows students, first-hand, why typing credentials into an
untrusted link is dangerous: on **HTTP** the password travels in plain text and can
be read instantly, and on a hostile network even **HTTPS** can be undermined.

> **For instructor-led teaching only.** Dummy/fake credentials only — never real
> passwords. Run it only on your own device and your own network. Always finish with
> the debrief. These rules are repeated in each document.

## What's in here
| File | What it is |
|------|------------|
| `index.html`, `style.css`, `script.js` | The demo login page (two screens: email/phone, then password). Brand-neutral on purpose — a `LOGO` placeholder and a generic "Company Name" footer. |
| `capture_server.py` | Serves the page over plain HTTP and prints whatever is typed to its console — the live "reveal". Needs only Python 3. |
| `CAPTURE.md` | Interception setup: the capture server, Wireshark (see it on the wire), and mitmproxy (incl. the HTTPS-warning demo). |
| `TEACHER-SCRIPT.md` | Run-of-show: the persona/story, the trap, the reveal, and the debrief. |
| `STUDENT-HANDOUT.md` | One-page takeaway for students. |

## Two modes of the page
- **Safe / simulated** — opened by double-clicking `index.html`, or hosted on
  GitHub Pages. Sends nothing anywhere. Use this to show the UI or host it publicly.
- **Capture** — served by `capture_server.py` over HTTP. The page really POSTs the
  (fake) login so it can be seen in plain text. This is the teaching moment.

## Quick start for the lesson
1. Read `TEACHER-SCRIPT.md` and `CAPTURE.md` once beforehand.
2. In this folder: `python3 capture_server.py`
3. It prints a URL like `http://<your-ip>:8000/`. Open that on the student device.
4. Have a student submit a **fake** email + **fake** password. Watch it appear in
   plain text on your console (and optionally in Wireshark/mitmproxy).
5. Run the debrief. Hand out `STUDENT-HANDOUT.md`.

## Hosting the safe version on GitHub Pages
In your repo: **Settings → Pages → Deploy from a branch → `main` / `/ (root)` →
Save**. After ~a minute it's live at `https://<username>.github.io/<repo>/`. Note
that GitHub Pages is HTTPS-only, so the *public* version can't be sniffed — which is
exactly why the plain-HTTP capture server is what demonstrates the insecure case.

## Why no real company name or logo
The page is deliberately generic so it's clearly a teaching demo and never
impersonates a real brand. Keep it that way: don't add a real company's logo or name.
