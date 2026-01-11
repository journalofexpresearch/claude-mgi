#!/usr/bin/env python3
"""
Login Logger - Track login details until 7am
Logs all login attempts with timestamps, IP addresses, and other details
to detect unauthorized access to your account.
"""

import json
import logging
from datetime import datetime, time
import os
import socket
import platform
import getpass

class LoginLogger:
    def __init__(self, log_file="login_details.log"):
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

    def should_continue_logging(self):
        """Check if current time is before 7am"""
        current_time = datetime.now().time()
        target_time = time(7, 0)  # 7:00 AM

        # If current time is before 7am, continue logging
        return current_time < target_time

    def get_system_info(self):
        """Gather system information"""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
        except:
            hostname = "Unknown"
            ip_address = "Unknown"

        return {
            "hostname": hostname,
            "ip_address": ip_address,
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor()
        }

    def log_login_attempt(self, username=None, additional_info=None):
        """Log a login attempt with detailed information"""
        if not self.should_continue_logging():
            self.logger.info("Reached 7am cutoff time. Stopping logging.")
            return False

        timestamp = datetime.now().isoformat()

        if username is None:
            try:
                username = getpass.getuser()
            except:
                username = "Unknown"

        system_info = self.get_system_info()

        login_data = {
            "timestamp": timestamp,
            "username": username,
            "system_info": system_info,
            "additional_info": additional_info or {}
        }

        # Log as JSON for easy parsing
        self.logger.info(f"LOGIN ATTEMPT: {json.dumps(login_data, indent=2)}")

        return True

    def monitor_session(self):
        """Monitor and log the current session"""
        self.logger.info("="*60)
        self.logger.info("Starting login monitoring session")
        self.logger.info(f"Monitoring will stop at 7:00 AM")
        self.logger.info("="*60)

        # Log initial session start
        self.log_login_attempt(additional_info={
            "event": "session_start",
            "note": "Independent logging started for credential monitoring"
        })

        self.logger.info(f"Login details being saved to: {os.path.abspath(self.log_file)}")
        self.logger.info("Monitoring active. Press Ctrl+C to stop manually.")

    def create_summary_report(self):
        """Create a summary of logged sessions"""
        summary_file = self.log_file.replace('.log', '_summary.txt')

        with open(summary_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("LOGIN MONITORING SUMMARY\n")
            f.write("="*60 + "\n\n")
            f.write(f"Report generated: {datetime.now().isoformat()}\n")
            f.write(f"Log file: {os.path.abspath(self.log_file)}\n\n")
            f.write("This log contains all login details captured during monitoring.\n")
            f.write("Review this file to identify any unauthorized access attempts.\n\n")
            f.write("Things to look for:\n")
            f.write("- Unfamiliar IP addresses\n")
            f.write("- Login times when you weren't using the system\n")
            f.write("- Different hostnames or system information\n")
            f.write("- Geographic locations you didn't access from\n\n")

        self.logger.info(f"Summary report created: {os.path.abspath(summary_file)}")


def main():
    """Main function to run the login logger"""
    logger = LoginLogger(log_file="login_details.log")

    try:
        logger.monitor_session()

        # Keep monitoring until 7am or manual stop
        import time
        while logger.should_continue_logging():
            time.sleep(300)  # Check every 5 minutes
            logger.log_login_attempt(additional_info={
                "event": "periodic_check",
                "status": "monitoring_active"
            })

        logger.logger.info("Reached 7:00 AM. Stopping monitoring.")
        logger.create_summary_report()

    except KeyboardInterrupt:
        logger.logger.info("\nMonitoring stopped by user")
        logger.create_summary_report()
    except Exception as e:
        logger.logger.error(f"Error during monitoring: {str(e)}")
        logger.create_summary_report()


if __name__ == "__main__":
    main()
