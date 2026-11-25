"""Local-only API bridge for SAG VCE. No keys or images are written to disk."""
from __future__ import annotations
import base64, json, os, re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app"
MAX_BODY = 35 * 1024 * 1024

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_POST(self):
        if self.path != "/api/generate":
            self.send_error(404); return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY:
                self.reply(413, {"error": "Request too large. Reduce the number or size of reference images."}); return
            body = json.loads(self.rfile.read(length))
            provider, key = body.get("provider"), body.get("key", "")
            if provider not in ("gemini", "openai") or not isinstance(key, str) or not key.strip():
                self.reply(400, {"error": "Choose a provider and supply its API key in Settings."}); return
            prompt = body.get("prompt", "")
            refs = body.get("references", [])
            if not isinstance(prompt, str) or not prompt.strip() or not isinstance(refs, list):
                self.reply(400, {"error": "Prompt or reference list is invalid."}); return
            if provider == "gemini":
                result = self.gemini(key.strip(), body.get("model", "gemini-3.1-flash-image"), prompt, refs)
            else:
                result = self.openai(key.strip(), body.get("model", "gpt-image-2.6-flare"), prompt, refs)
            self.reply(200, result)
        except json.JSONDecodeError:
            self.reply(400, {"error": "Invalid JSON request."})
        except Exception as exc:
            self.reply(500, {"error": str(exc)[:1200]})

    def image_part(self, ref):
        data_url = ref.get("data", "")
        match = re.match(r"^data:(image/[\w.+-]+);base64,([A-Za-z0-9+/=]+)$", data_url)
        if not match:
            raise ValueError("A reference image has an invalid data URL.")
        mime, encoded = match.groups()
        raw = base64.b64decode(encoded, validate=True)
        if len(raw) > 8 * 1024 * 1024:
            raise ValueError("A reference image exceeds 8 MB.")
        return mime, encoded

    def gemini(self, key, model, prompt, refs):
        if len(refs) > 3:
            raise ValueError("This Gemini integration currently supports up to 3 reference images.")
        parts = []
        for ref in refs:
            mime, encoded = self.image_part(ref)
            parts.append({"inline_data": {"mime_type": mime, "data": encoded}})
            parts.append({"text": "This is an approved visual reference for: " + str(ref.get("name", "asset")) + " (" + str(ref.get("type", "reference")) + "). Preserve its identity and details."})
        parts.append({"text": prompt + "\n\nGenerate one finished image. Return the image, not only a written description."})
        url = "https://generativelanguage.googleapis.com/v1beta/models/" + model + ":generateContent"
        payload = {"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}
        data = self.request_json(url, {"x-goog-api-key": key}, payload)
        candidates = data.get("candidates", [])
        for candidate in candidates:
            for part in candidate.get("content", {}).get("parts", []):
                inline = part.get("inlineData") or part.get("inline_data")
                if inline and inline.get("data"):
                    mime = inline.get("mimeType") or inline.get("mime_type") or "image/png"
                    return {"image": "data:" + mime + ";base64," + inline["data"], "provider": "gemini", "model": model}
        reason = data.get("promptFeedback", {}).get("blockReason")
        if reason:
            raise ValueError("Gemini blocked this request: " + str(reason))
        raise ValueError("Gemini returned no image. Check that your API key has access to this image model.")

    def openai(self, key, model, prompt, refs):
        if not refs:
            raise ValueError("Add at least one reference image.")
        images = []
        for ref in refs[:16]:
            mime, encoded = self.image_part(ref)
            images.append({"image_url": "data:" + mime + ";base64," + encoded})
        url = "https://api.openai.com/v1/images/edits"
        payload = {"model": model, "images": images, "prompt": prompt, "size": "1536x1024", "quality": "high", "output_format": "png"}
        data = self.request_json(url, {"Authorization": "Bearer " + key}, payload)
        items = data.get("data", [])
        if not items or not items[0].get("b64_json"):
            raise ValueError("OpenAI returned no image.")
        return {"image": "data:image/png;base64," + items[0]["b64_json"], "provider": "openai", "model": model}

    def request_json(self, url, headers, payload):
        request_headers = {"Content-Type": "application/json", **headers}
        req = Request(url, data=json.dumps(payload).encode("utf-8"), headers=request_headers, method="POST")
        try:
            with urlopen(req, timeout=240) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            try: details = json.loads(exc.read().decode("utf-8"))
            except Exception: details = {}
            message = details.get("error", {}).get("message") or details.get("message") or ("Provider HTTP " + str(exc.code))
            raise ValueError(message)
        except URLError as exc:
            raise ValueError("Could not reach the image provider: " + str(exc.reason))

    def reply(self, status, payload):
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

if __name__ == "__main__":
    import webbrowser
    from threading import Timer
    port = int(os.environ.get("SAG_VCE_PORT", "8765"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"SAG VCE running at http://127.0.0.1:{port}/")
    print("Local only. Keep this terminal open. Press Ctrl+C to stop.")
    Timer(1, lambda: webbrowser.open(f"http://127.0.0.1:{port}/")).start()
    try: server.serve_forever()
    except KeyboardInterrupt: print("\nStopping SAG VCE.")
    finally: server.server_close()
