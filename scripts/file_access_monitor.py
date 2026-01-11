#!/usr/bin/env python3
"""
File Access Monitor - Detect unauthorized access to monitoring files
Immediately sends email and clears logs if someone tries to view or tamper with the monitoring system.
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path

# Import the LoginLogger to use its email functionality
from login_logger import LoginLogger

class FileAccessMonitor:
    def __init__(self):
        self.logger = self.setup_logging()
        self.login_logger = LoginLogger()

        # Files to monitor
        self.monitored_files = [
            "login_details.log",
            "login_details_summary.txt",
            "scripts/email_config.json",
            "scripts/login_logger.py",
            "scripts/file_access_monitor.py",
            "scripts/LOGIN_LOGGER_README.md",
            "QUICK_START.md"
        ]

        # Track last access times
        self.last_access_times = {}
        self.initialize_access_times()

        # Flag to prevent recursive triggering
        self.sending_email = False

    def setup_logging(self):
        """Setup logging for file access monitor"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - SECURITY ALERT - %(message)s',
            handlers=[
                logging.FileHandler("access_monitor.log"),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def initialize_access_times(self):
        """Initialize tracking of file access times"""
        for filepath in self.monitored_files:
            if os.path.exists(filepath):
                stat = os.stat(filepath)
                self.last_access_times[filepath] = {
                    'atime': stat.st_atime,  # Last access time
                    'mtime': stat.st_mtime,  # Last modification time
                }

    def check_git_access(self):
        """Check if someone is accessing files via git"""
        try:
            # Check git reflog for recent activity
            result = subprocess.run(
                ['git', 'reflog', '-1'],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Check git log for very recent commits
            recent_log = subprocess.run(
                ['git', 'log', '-1', '--format=%ct'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if recent_log.returncode == 0 and recent_log.stdout.strip():
                last_commit_time = int(recent_log.stdout.strip())
                current_time = int(time.time())

                # If commit was within last 60 seconds, it's suspicious
                if current_time - last_commit_time < 60:
                    return True, "Recent git commit detected"

            # Check for git status being run (indicates someone is examining repo)
            # This is harder to detect, but we can check for .git/index changes
            git_index = ".git/index"
            if os.path.exists(git_index):
                index_stat = os.stat(git_index)
                index_mtime = index_stat.st_mtime

                # If index was modified in last 30 seconds
                if time.time() - index_mtime < 30:
                    return True, "Git index recently accessed"

            return False, None

        except Exception as e:
            self.logger.error(f"Error checking git access: {e}")
            return False, None

    def check_file_access(self):
        """Check if monitored files have been accessed"""
        for filepath in self.monitored_files:
            if not os.path.exists(filepath):
                continue

            try:
                stat = os.stat(filepath)
                current_atime = stat.st_atime
                current_mtime = stat.st_mtime

                if filepath not in self.last_access_times:
                    # File was created since we started monitoring
                    self.last_access_times[filepath] = {
                        'atime': current_atime,
                        'mtime': current_mtime
                    }
                    continue

                last_atime = self.last_access_times[filepath]['atime']
                last_mtime = self.last_access_times[filepath]['mtime']

                # Check if file was accessed (read)
                if current_atime > last_atime:
                    # File was accessed!
                    return True, f"File accessed: {filepath}"

                # Check if file was modified
                if current_mtime > last_mtime:
                    # File was modified!
                    return True, f"File modified: {filepath}"

            except Exception as e:
                self.logger.error(f"Error checking {filepath}: {e}")

        return False, None

    def trigger_emergency_send(self, reason):
        """Immediately send email and clear logs when tampering detected"""
        if self.sending_email:
            # Prevent recursive triggering
            return

        self.sending_email = True

        self.logger.critical("="*60)
        self.logger.critical("SECURITY ALERT: UNAUTHORIZED ACCESS DETECTED")
        self.logger.critical(f"Reason: {reason}")
        self.logger.critical("="*60)

        # Log the security event
        self.login_logger.log_login_attempt(additional_info={
            "event": "SECURITY_BREACH",
            "reason": reason,
            "alert": "Unauthorized access to monitoring files detected",
            "action": "Emergency email triggered, logs being cleared"
        })

        self.logger.warning("Immediately sending logs to email...")

        # Send email with current logs
        if self.login_logger.send_email_with_logs():
            self.logger.info("Emergency email sent successfully")

            # Clear all logs
            self.logger.info("Clearing all logs to prevent tampering...")
            self.login_logger.clear_logs()

            # Clear this monitor's log too
            if os.path.exists("access_monitor.log"):
                with open("access_monitor.log", 'w') as f:
                    f.write(f"# Access monitor log cleared after security alert at {time.ctime()}\n")
                    f.write(f"# Alert reason: {reason}\n")

            self.logger.info("Logs cleared successfully")
            self.logger.info("Monitoring will continue...")

        else:
            self.logger.error("Failed to send emergency email!")
            self.logger.error("Logs NOT cleared - manual intervention required")

        # Reset tracking after handling the alert
        time.sleep(5)  # Wait before resetting to prevent immediate re-trigger
        self.initialize_access_times()
        self.sending_email = False

    def monitor(self):
        """Main monitoring loop"""
        self.logger.info("="*60)
        self.logger.info("File Access Monitor Started")
        self.logger.info("Monitoring for unauthorized access to security files")
        self.logger.info("="*60)

        self.logger.info("Monitored files:")
        for filepath in self.monitored_files:
            if os.path.exists(filepath):
                self.logger.info(f"  ✓ {filepath}")
            else:
                self.logger.info(f"  ✗ {filepath} (not found)")

        self.logger.info("\nMonitoring active. Any access to these files will trigger emergency email.")

        try:
            while True:
                # Check for file access
                accessed, reason = self.check_file_access()
                if accessed:
                    self.trigger_emergency_send(reason)

                # Check for git operations
                git_access, git_reason = self.check_git_access()
                if git_access:
                    self.trigger_emergency_send(git_reason)

                # Check every 2 seconds for quick response
                time.sleep(2)

        except KeyboardInterrupt:
            self.logger.info("\nFile access monitor stopped by user")
        except Exception as e:
            self.logger.error(f"Monitor error: {e}")


def main():
    """Main function"""
    monitor = FileAccessMonitor()
    monitor.monitor()


if __name__ == "__main__":
    main()
