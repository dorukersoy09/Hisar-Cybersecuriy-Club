# Interception setup guide (instructor)

This shows the class, first-hand, that credentials typed into an untrusted link
travel in plain text over HTTP, and why an untrusted network can undermine even
HTTPS. Three ways, easiest first. Use whichever fits your room.

> **Guardrails — say these out loud and keep to them**
> - **Dummy credentials only.** Students type fake names and fake passwords. Never a real password from any real account. Nobody's actual credentials are ever entered or captured.
> - **Your own equipment and your own network only.** Do not point any of this at a network, device, or site you don't own or run. Capturing other people's traffic without consent is illegal in most places.
> - **Always debrief** (see `TEACHER-SCRIPT.md`). The point is to make students safer, not to collect anything.
> - Close the tools and clear the capture when the lesson ends. Nothing here needs to be saved.

---

## Option A — The capture server (no extra tools, start here)

The included `capture_server.py` serves the login page over plain HTTP and prints
whatever is typed straight to its console. This alone makes the point and needs
nothing installed but Python 3.

1. On your computer, in the folder with the files:
   ```
   python3 capture_server.py
   ```
2. It prints a URL like `http://192.168.1.50:8000/`. That `192.168.x.x` is your
   computer's address on your local network.
3. On the student device (same Wi-Fi), open that URL. Have a student type a fake
   email and a fake password and click **Sign in**.
4. Look at your server console: the username and password appear in plain text,
   and the student's own screen flips to a red "that link just stole your login"
   page showing the same thing.

> Note: this must be **HTTP**, not HTTPS. GitHub Pages forces HTTPS, so the live
> `github.io` version can't be sniffed — which is itself the lesson. The plain-HTTP
> capture server is what demonstrates the insecure case.

---

## Option B — Wireshark (see it on the wire)

Shows the exact bytes crossing the network, so students see it isn't magic.

1. Install Wireshark (https://www.wireshark.org). Run `capture_server.py` as above.
2. Open Wireshark and start a capture on the interface your network uses
   (Wi-Fi, or Ethernet).
3. In the filter bar type:
   ```
   http.request.method == "POST"
   ```
   and press Enter.
4. Have a student submit the fake login on `http://<your-ip>:8000/`.
5. The POST to `/login` appears. Right-click it → **Follow → HTTP Stream** (or
   **TCP Stream**). The request body reads, in the clear:
   ```
   identifier=student@fake.example&password=Hunter2Fake
   ```
6. Point out: no decryption, no hacking tools — the password is simply *there*,
   because HTTP has no encryption at all.

Capturing another device's traffic (not just your own machine's) may need your
Wi-Fi adapter in monitor mode or a mirrored switch port; for a classroom it's
simplest to run the browser and Wireshark on the same machine, or use a small
hub/mirror you own.

---

## Option C — mitmproxy (intercepting proxy; also shows the HTTPS angle)

mitmproxy sits between the browser and the site and shows every request. It's how
you demonstrate the "even HTTPS can be undermined on a hostile network" point.

1. Install mitmproxy (https://mitmproxy.org) and run:
   ```
   mitmweb
   ```
   It opens a web dashboard (usually http://127.0.0.1:8081) and listens as a proxy
   on port 8080.
2. On the student device, set the Wi-Fi proxy to your computer's IP, port `8080`.
3. **HTTP demo:** browse to the plain-HTTP capture page and submit the fake login.
   The POST and its plaintext body show up in the mitmweb flow list immediately.
4. **HTTPS demo (the important debrief):** browse to any normal `https://` site.
   The browser shows a **certificate warning** — because mitmproxy is presenting
   its own certificate that the device doesn't trust. Stop here and make the point:
   - On HTTPS, the attacker-in-the-middle can't read the traffic **unless the user
     ignores that warning / installs the attacker's certificate**.
   - A hostile "free Wi-Fi" works exactly this way. The warning is the user's
     protection. Clicking through it, or installing a "required" certificate to
     "get online", is what hands the attacker everything.
   - Do **not** install mitmproxy's CA certificate on the student device. The
     warning staying up *is* the lesson. (If you installed it for an earlier test,
     remove it afterwards.)
5. When done: remove the proxy setting from the student device.

---

## Quick troubleshooting
- **Student device can't load the page:** both devices must be on the same
  network, and your computer's firewall must allow the port. Try
  `http://localhost:8000/` on the serving computer first to confirm it runs.
- **Wireshark shows nothing:** check you're on the right interface and the traffic
  is really HTTP (the capture server is; `github.io` is HTTPS and won't show a
  readable body).
- **No second device:** run everything on one laptop — open the page in the
  browser and watch the server console / Wireshark on the same machine.
