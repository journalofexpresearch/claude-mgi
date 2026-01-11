#!/usr/bin/env python3
"""
Web Login Logger - Track web-based login attempts
For monitoring web application logins to detect unauthorized access
"""

import json
import logging
from datetime import datetime, time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class LoginLogHandler(BaseHTTPRequestHandler):
    """HTTP request handler that logs login attempts"""

    def do_POST(self):
        """Handle POST requests (login attempts)"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Parse the POST data
        try:
            data = json.loads(post_data) if post_data.startswith('{') else parse_qs(post_data)
        except:
            data = {"raw": post_data}

        # Log the login attempt
        login_info = {
            "timestamp": datetime.now().isoformat(),
            "client_ip": self.client_address[0],
            "client_port": self.client_address[1],
            "user_agent": self.headers.get('User-Agent', 'Unknown'),
            "referer": self.headers.get('Referer', 'Unknown'),
            "method": "POST",
            "path": self.path,
            "data": data,
            "headers": dict(self.headers)
        }

        self.server.log_login(login_info)

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "logged"}).encode())

    def do_GET(self):
        """Handle GET requests"""
        login_info = {
            "timestamp": datetime.now().isoformat(),
            "client_ip": self.client_address[0],
            "client_port": self.client_address[1],
            "user_agent": self.headers.get('User-Agent', 'Unknown'),
            "referer": self.headers.get('Referer', 'Unknown'),
            "method": "GET",
            "path": self.path,
            "query": urlparse(self.path).query,
            "headers": dict(self.headers)
        }

        self.server.log_login(login_info)

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "logged"}).encode())

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


class WebLoginLogger(HTTPServer):
    """HTTP server that logs login attempts"""

    def __init__(self, server_address, RequestHandlerClass, log_file="web_login_details.log"):
        super().__init__(server_address, RequestHandlerClass)
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("="*60)
        self.logger.info("Web Login Logger Started")
        self.logger.info(f"Logging to: {os.path.abspath(self.log_file)}")
        self.logger.info("="*60)

    def should_continue_logging(self):
        """Check if current time is before 7am"""
        current_time = datetime.now().time()
        target_time = time(7, 0)  # 7:00 AM
        return current_time < target_time

    def log_login(self, login_info):
        """Log a login attempt"""
        if not self.should_continue_logging():
            self.logger.info("Reached 7am cutoff time. Stopping logging.")
            self.shutdown()
            return

        self.logger.info(f"WEB LOGIN ATTEMPT: {json.dumps(login_info, indent=2)}")


def main():
    """Main function to run the web login logger"""
    PORT = 8888
    log_file = "web_login_details.log"

    print(f"Starting Web Login Logger on port {PORT}")
    print(f"Logs will be saved to: {os.path.abspath(log_file)}")
    print(f"Monitoring will stop at 7:00 AM")
    print("\nTo log a login attempt, send POST/GET request to:")
    print(f"  http://localhost:{PORT}/login")
    print("\nPress Ctrl+C to stop\n")

    try:
        server = WebLoginLogger(('0.0.0.0', PORT), LoginLogHandler, log_file)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
