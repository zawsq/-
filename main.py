import os
import logging
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED

logging.basicConfig(format='%(name)s - %(levelname)s: \n %(message)s', level=logging.INFO)

DEBUG_MODE = False

class mustard_leaf:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.logger = logging.getLogger(__name__)

    def _job_listener(self, event) -> None:
        if event.exception:
            self.logger.error(f"Job FAILED [{event.job_id}]: {event.exception}")
        else:
            self.logger.info(f"Job executed OK [{event.job_id}]")

    def tuna(self) -> None:
        self.scheduler.add_listener(self._job_listener, EVENT_JOB_ERROR | EVENT_JOB_EXECUTED)
        self.scheduler.start()

        mode = "DEBUG (30s test)" if DEBUG_MODE else "PRODUCTION (midnight UTC)"
        self.logger.info(f"Scheduler started — mode: {mode}")


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        mode = "DEBUG" if DEBUG_MODE else "PRODUCTION"
        self.wfile.write(
            f"<h1>> made with sushi</h1><p>Space is running. Mode: {mode}</p>".encode()
        )

    def log_message(self, format, *args):
        return


def main() -> None:
    salmon = mustard_leaf()
    salmon.tuna()
    logging.info('VOID START')

    port = int(os.getenv("PORT", 7860))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logging.info(f"HTTP server running on port {port}")

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        salmon.scheduler.shutdown()
        server.shutdown()
        logging.info("Stopped")


if __name__ == "__main__":
    print(f"Debug mode: {DEBUG_MODE}")
    main()