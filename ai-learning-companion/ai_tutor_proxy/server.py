"""
Simple HTTP server for AI Tutor Proxy.
"""
import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from .provider_router import TutorProviderRouter
from .privacy import PrivacyMode, normalize_privacy_mode

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = TutorProviderRouter()

class TutorProxyRequestHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        origin = self.headers.get("Origin", "")
        if not origin:
            self.send_header("Access-Control-Allow-Origin", "*")
        elif origin == "null" or "localhost" in origin or "127.0.0.1" in origin:
            self.send_header("Access-Control-Allow-Origin", origin)
        else:
            self.send_header("Access-Control-Allow-Origin", "http://127.0.0.1")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/tutor/ask":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            req_data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return

        question = req_data.get("question", "")
        raw_privacy_mode = req_data.get("privacy_mode", PrivacyMode.PUBLIC_CURRICULUM_ONLY.value)
        privacy_mode = normalize_privacy_mode(raw_privacy_mode)
        learner_context = req_data.get("learner_context", {})

        if not question:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing question")
            return

        # Route the request
        result = router.route_request(question, privacy_mode, learner_context)
        
        # Include privacy mode in result for transparency
        result["privacy_mode"] = privacy_mode
        result["used_provider"] = result.get("provider_id", "unknown")

        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))

def run_server(port=8080):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, TutorProxyRequestHandler)
    logging.info(f"Starting AI Tutor Proxy on 127.0.0.1:{port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info("Server stopped.")

if __name__ == "__main__":
    run_server()
