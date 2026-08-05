#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地服务：托管当前目录静态文件，并提供「人审核 → 智能体调整判断」的反馈回路。

  GET  /api/feedback            返回当前 feedback.json
  POST /api/feedback            接收一次人工审核，落盘后重跑 build+sync，返回最新 DATA

审核提交体（JSON）：
  {
    "term": "设立AI组织",          # 与趋势 term 对应（范式趋势的 label）
    "decision": "confirm" | "reclass" | "reject",
    "sub": "组织改革",              # 仅 reclass 时需要，目标细分
    "note": "..."                   # 可选备注
  }

启动:  python3 server.py [port]     默认 8732
"""
import json
import os
import subprocess
import sys
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
VENV_PY = "/Users/zhengk/.workbuddy/binaries/python/envs/default/bin/python"
BUILD = os.path.join(HERE, "build_daily.py")
SYNC = os.path.join(HERE, "sync.py")
FEEDBACK = os.path.join(HERE, "feedback.json")
DATA = os.path.join(HERE, "daily-trends.json")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8732


def load_feedback():
    if not os.path.isfile(FEEDBACK):
        return {"paradigm": {}}
    try:
        with open(FEEDBACK, "r", encoding="utf-8") as f:
            d = json.load(f)
        d.setdefault("paradigm", {})
        return d
    except Exception:
        return {"paradigm": {}}


def save_feedback(d):
    tmp = FEEDBACK + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    os.replace(tmp, FEEDBACK)  # 原子写，避免半截文件


def run_build():
    """重跑数据管线，使人工反馈生效；失败也不影响已保存的 feedback。"""
    try:
        subprocess.run([VENV_PY, BUILD], cwd=HERE, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        subprocess.run([VENV_PY, SYNC], cwd=HERE, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        return True, ""
    except Exception as e:
        return False, str(e)


class Handler(SimpleHTTPRequestHandler):
    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0] == "/api/feedback":
            return self._json(load_feedback())
        return super().do_GET()

    def do_POST(self):
        try:
            return self._post_feedback()
        except Exception as e:
            return self._json({"ok": False, "error": f"server error: {e}"}, 500)

    def _post_feedback(self):
        if self.path.split("?")[0] != "/api/feedback":
            return self._json({"error": "unknown endpoint"}, 404)
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            body = json.loads(raw.decode("utf-8") or "{}")
        except Exception as e:
            return self._json({"error": f"bad body: {e}"}, 400)

        term = (body.get("term") or "").strip()
        decision = body.get("decision")
        if not term or decision not in ("confirm", "reclass", "reject"):
            return self._json({"error": "需要 term 与 decision(confirm|reclass|reject)"}, 400)
        if decision == "reclass" and not body.get("sub"):
            return self._json({"error": "reclass 需要 sub"}, 400)

        fb = load_feedback()
        fb["paradigm"][term] = {
            "decision": decision,
            "sub": body.get("sub"),
            "note": body.get("note", ""),
            "at": datetime.now().isoformat(timespec="seconds"),
            "by": "human",
        }
        save_feedback(fb)

        ok, err = run_build()
        # 返回最新 DATA（供前端直接重渲染），并附带 feedback 与 build 结果
        data = None
        if ok and os.path.isfile(DATA):
            try:
                data = json.load(open(DATA, encoding="utf-8"))
            except Exception:
                data = None
        return self._json({
            "ok": ok,
            "build_error": err or None,
            "feedback": fb,
            "data": data,
        }, 200 if ok else 500)

    def log_message(self, fmt, *args):
        sys.stderr.write("[" + self.address_string() + "] " + (fmt % args) + "\n")


def main():
    os.chdir(HERE)
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"日度三驾马车 · 审核服务已启动: http://localhost:{PORT}/  (Ctrl+C 退出)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()
        print("\n已停止。")


if __name__ == "__main__":
    main()
