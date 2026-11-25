import json
from pathlib import Path
from server import Handler, ROOT

def test_app_entry_exists():
    assert (ROOT / "app" / "index.html").is_file()

def test_local_server_has_no_external_bind_default():
    source = (ROOT / "server.py").read_text(encoding="utf-8")
    assert 'ThreadingHTTPServer(("127.0.0.1", port), Handler)' in source

def test_server_does_not_write_keys_or_assets():
    source = (ROOT / "server.py").read_text(encoding="utf-8")
    assert "write_text(" not in source
    assert "write_bytes(" not in source
