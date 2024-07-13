from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from utils.variables import kill_switch
import time
import threading


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        logging.info(
            "GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers)
        )
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

    def do_POST(self):
        content_length = int(
            self.headers["Content-Length"]
        )  # <--- Gets the size of data
        post_data = json.loads(
            self.rfile.read(content_length)
        )  # <--- Gets the data itself
        logging.info(
            "POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
            str(self.path),
            str(self.headers),
            post_data,
        )

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode("utf-8"))


def run(port=8080, server_class=HTTPServer, handler_class=S):
    global kill_switch

    server_address = ("0.0.0.0", port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n")

    def monitor_kill_switch():
        global kill_switch
        logging.debug("Kill switch manager started!")
        while not kill_switch:
            time.sleep(0.1)
        logging.info("Kill switch activated. Stopping httpd...\n")
        httpd.shutdown()

    monitor_thread = threading.Thread(target=monitor_kill_switch)
    monitor_thread.start()

    try:
        logging.info("httpd Started...\n")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")
