"""Shared pieces for the Santa Shooter capture recipes (TIC-80 runtime on the test instance)."""
import json, pathlib
SCR = "/tmp/claude-1000/-home-kc-Work-santa-shooter-subject/0993428a-0fd4-5b74-9851-7d8c57c80d1f/scratchpad/cap"
URL = "http://127.0.0.1:8083/runtime/tic80/3892c7a/"
SRC = pathlib.Path("/home/kc/Work/santa_shooter/starter.lua").read_text()
TAIL = SRC[SRC.index("-- <TILES>"):]                      # sprites, palette, sfx of the subject's cart
HEAD = "-- title: santa\n-- script: lua\n\n"

def cart(body):
    return HEAD + body + "\n" + TAIL

def load(text):
    return "localStorage.setItem('tic80-web-editor-cart', JSON.stringify({version:1, text:%s, ext:'lua', savedAt:Date.now()}))" % json.dumps(text)

# A div laid exactly over the 240x136 screen inside the letterboxed canvas: TIC-80 scales by an
# integer factor and centres (checked: the crop gives 1200x680 at viewport 1280x800, scale 2).
OVERLAY = """(() => { const c = document.getElementById('canvas'); const r = c.getBoundingClientRect();
 const k = Math.floor(Math.min(c.width / 240, c.height / 136)); const sw = 240 * k, sh = 136 * k;
 const ox = (c.width - sw) / 2, oy = (c.height - sh) / 2; const fx = r.width / c.width, fy = r.height / c.height;
 let d = document.getElementById('tic-screen'); if (!d) { d = document.createElement('div'); d.id = 'tic-screen'; document.body.appendChild(d); }
 d.style.cssText = 'position:fixed;pointer-events:none;left:' + (r.left + ox * fx) + 'px;top:' + (r.top + oy * fy) + 'px;width:' + (sw * fx) + 'px;height:' + (sh * fy) + 'px;'; })()"""

KEYS = {"ArrowRight": 39, "ArrowLeft": 37, "ArrowUp": 38, "ArrowDown": 40, "KeyZ": 90, "KeyX": 88}
def _kev(kind, code):
    key = {"KeyZ": "z", "KeyX": "x"}.get(code, code)
    return "document.getElementById('canvas').dispatchEvent(new KeyboardEvent(%s, {key:%s, code:%s, keyCode:%d, which:%d, bubbles:true, cancelable:true}))" % (json.dumps(kind), json.dumps(key), json.dumps(code), KEYS[code], KEYS[code])
def down(code): return _kev("keydown", code)
def up(code): return _kev("keyup", code)

TAP = "(() => { const c = document.getElementById('canvas'); const r = c.getBoundingClientRect(); const t = new Touch({identifier: 1, target: c, clientX: r.left + r.width * 0.5, clientY: r.top + r.height * 0.9}); for (const n of ['touchstart', 'touchend']) c.dispatchEvent(new TouchEvent(n, {touches: n === 'touchstart' ? [t] : [], changedTouches: [t], bubbles: true, cancelable: true})); })()"

def boot(text, tap=False):
    """Steps that load `text` as the cart, boot TIC-80, run it and lay the screen overlay."""
    # The « CLICK TO PLAY » panel shows only on the first boot of the browser context: click it
    # when it is there, otherwise the runtime boots by itself.
    # Reload first so the previous cart's autosave has settled, then store ours and reload again:
    # the editor only re-saves on a change, so what we stored is what the next boot restores.
    s = [{"goto": URL}, {"wait_for": "#root"}, {"wait": 3}, {"js": load(text)}, {"wait": 0.5}, {"goto": URL},
         {"wait_for": "#canvas"}, {"wait": 1},
         {"js": "(() => { const b = document.querySelector('button.panel-message'); if (b) b.click(); })()"}, {"wait": 4},
         {"click": ".monaco-editor"},
         {"type": "#canvas", "text": "run", "delay": 80}, {"key": "Enter"}, {"wait": 1.5}]
    if tap:
        s += [{"js": TAP}, {"wait": 1.0}]
    s += [{"js": OVERLAY}]
    return s

def recipe(steps, touch=False, out=SCR, into=None, viewport=(1280, 800)):
    r = {"url": URL, "viewport": list(viewport), "scale": 2, "theme": "dark", "touch": touch, "out": out, "steps": steps}
    if into:
        r["into"] = into
    return r

def write(name, rec):
    pathlib.Path(SCR + "/" + name + ".json").write_text(json.dumps(rec, indent=1))
    return SCR + "/" + name + ".json"

# A gamepad band drawn in the page under the screen, in the style of the subject's earlier GIFs
# (dark band, a d-pad and two round buttons; a pressed key lights its button). The browser draws
# it before the capture: nothing is painted onto the image afterwards. #tic-frame = screen + band.
PAD = """(() => { const s = document.getElementById('tic-screen'); const r = s.getBoundingClientRect();
 const H = r.height * 132 / 408; const W = r.width;
 let f = document.getElementById('tic-frame'); if (!f) { f = document.createElement('div'); f.id = 'tic-frame'; document.body.appendChild(f); }
 f.style.cssText = 'position:fixed;pointer-events:none;z-index:99998;left:' + r.left + 'px;top:' + r.top + 'px;width:' + W + 'px;height:' + (r.height + H) + 'px;';
 let p = document.getElementById('tic-pad'); if (!p) { p = document.createElement('div'); p.id = 'tic-pad'; document.body.appendChild(p); }
 p.style.cssText = 'position:fixed;pointer-events:none;left:' + r.left + 'px;top:' + (r.top + r.height) + 'px;width:' + W + 'px;height:' + H + 'px;background:#1a1c2c;z-index:99999;';
 const u = H / 132;
 p.innerHTML = '<div style="position:absolute;left:' + (W/2 - 230*u) + 'px;top:' + (12*u) + 'px;width:' + (460*u) + 'px;height:' + (108*u) + 'px;border-radius:' + (54*u) + 'px;background:#333c57"></div>';
 const cell = (x, y, w, h, id, rad) => '<div id="' + id + '" style="position:absolute;left:' + (W/2 + x*u) + 'px;top:' + (y*u) + 'px;width:' + (w*u) + 'px;height:' + (h*u) + 'px;background:#566c86;border-radius:' + (rad*u) + 'px"></div>';
 p.innerHTML += cell(-174, 24, 28, 84, 'pad-v', 4) + cell(-202, 52, 84, 28, 'pad-h', 4)
   + cell(-174, 24, 28, 28, 'k-ArrowUp', 4) + cell(-174, 80, 28, 28, 'k-ArrowDown', 4) + cell(-202, 52, 28, 28, 'k-ArrowLeft', 4) + cell(-146, 52, 28, 28, 'k-ArrowRight', 4)
   + cell(72, 58, 44, 44, 'k-KeyX', 22) + cell(132, 36, 44, 44, 'k-KeyZ', 22);
 if (!window.__padBound) { window.__padBound = true;
   document.addEventListener('keydown', e => { const b = document.getElementById('k-' + e.code); if (b) b.style.background = '#94b0c2'; }, true);
   document.addEventListener('keyup', e => { const b = document.getElementById('k-' + e.code); if (b) b.style.background = '#566c86'; }, true); } })()"""

def boot_pad(text):
    return boot(text) + [{"js": PAD}]
