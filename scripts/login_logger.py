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
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class LoginLogger:
    def __init__(self, log_file="login_details.log", config_file="scripts/email_config.json"):
        self.log_file = log_file
        self.config_file = config_file
        self.email_config = None
        self.setup_logging()
        self.load_email_config()

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
        return summary_file

    def load_email_config(self):
        """Load email configuration from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.email_config = json.load(f)
                self.logger.info("Email configuration loaded successfully")
            else:
                self.logger.warning(f"Email config not found: {self.config_file}")
                self.logger.warning("Email functionality will be disabled")
                self.logger.warning("Copy email_config.json.example to email_config.json and configure it")
        except Exception as e:
            self.logger.error(f"Error loading email config: {str(e)}")
            self.email_config = None

    def get_git_diffs(self):
        """Collect git diffs from the repository"""
        try:
            # Get current working directory
            cwd = os.path.dirname(os.path.abspath(__file__))
            repo_root = os.path.dirname(cwd)  # Go up one level from scripts/

            # Check if we're in a git repo
            check_git = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=10
            )

            if check_git.returncode != 0:
                return "Not a git repository"

            # Get git status
            status = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=10
            )

            # Get diff of staged changes
            staged_diff = subprocess.run(
                ['git', 'diff', '--cached'],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=10
            )

            # Get diff of unstaged changes
            unstaged_diff = subprocess.run(
                ['git', 'diff'],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=10
            )

            # Get recent commits (last 10)
            recent_commits = subprocess.run(
                ['git', 'log', '--oneline', '-10'],
                cwd=repo_root,
                capture_output=True,
                text=True,
                timeout=10
            )

            diff_report = "="*60 + "\n"
            diff_report += "GIT REPOSITORY STATUS\n"
            diff_report += "="*60 + "\n\n"

            diff_report += "STATUS:\n"
            diff_report += status.stdout if status.stdout else "(clean working tree)\n"
            diff_report += "\n"

            diff_report += "="*60 + "\n"
            diff_report += "RECENT COMMITS:\n"
            diff_report += "="*60 + "\n"
            diff_report += recent_commits.stdout if recent_commits.stdout else "(no commits)\n"
            diff_report += "\n"

            if staged_diff.stdout:
                diff_report += "="*60 + "\n"
                diff_report += "STAGED CHANGES:\n"
                diff_report += "="*60 + "\n"
                diff_report += staged_diff.stdout + "\n"

            if unstaged_diff.stdout:
                diff_report += "="*60 + "\n"
                diff_report += "UNSTAGED CHANGES:\n"
                diff_report += "="*60 + "\n"
                diff_report += unstaged_diff.stdout + "\n"

            if not staged_diff.stdout and not unstaged_diff.stdout:
                diff_report += "\n(No file changes detected)\n"

            return diff_report

        except Exception as e:
            return f"Error getting git diffs: {str(e)}"

    def send_email_with_logs(self):
        """Send email with log files and git diffs"""
        if not self.email_config:
            self.logger.error("Cannot send email: No email configuration loaded")
            return False

        try:
            # Create summary report first
            summary_file = self.create_summary_report()

            # Get git diffs
            git_diffs = self.get_git_diffs()

            # Create email message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = self.email_config['recipient_email']
            msg['Subject'] = f"Login Monitoring Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Email body
            body = f"""
Login Monitoring Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This automated report contains:
1. Login activity logs
2. Summary report
3. Git repository changes

Please review the attached files for any suspicious activity.

{"="*60}
GIT REPOSITORY CHANGES
{"="*60}

{git_diffs}

{"="*60}
END OF REPORT
{"="*60}

This is an automated security monitoring email.
If you did not set up this monitoring, your credentials may be compromised.
"""

            msg.attach(MIMEText(body, 'plain'))

            # Attach log file
            if os.path.exists(self.log_file):
                with open(self.log_file, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(self.log_file)}"')
                    msg.attach(part)

            # Attach summary file
            if os.path.exists(summary_file):
                with open(summary_file, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(summary_file)}"')
                    msg.attach(part)

            # Connect to SMTP server and send email
            self.logger.info(f"Connecting to SMTP server: {self.email_config['smtp_server']}:{self.email_config['smtp_port']}")

            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])

            if self.email_config.get('use_tls', True):
                server.starttls()

            server.login(self.email_config['sender_email'], self.email_config['sender_password'])

            text = msg.as_string()
            server.sendmail(self.email_config['sender_email'], self.email_config['recipient_email'], text)
            server.quit()

            self.logger.info(f"Email sent successfully to {self.email_config['recipient_email']}")
            return True

        except Exception as e:
            self.logger.error(f"Error sending email: {str(e)}")
            return False

    def clear_logs(self):
        """Clear log files after successful email"""
        try:
            # Clear main log file
            if os.path.exists(self.log_file):
                with open(self.log_file, 'w') as f:
                    f.write(f"# Log cleared at {datetime.now().isoformat()}\n")
                    f.write("# Previous logs have been emailed\n")
                self.logger.info(f"Log file cleared: {self.log_file}")

            # Clear summary file
            summary_file = self.log_file.replace('.log', '_summary.txt')
            if os.path.exists(summary_file):
                os.remove(summary_file)
                self.logger.info(f"Summary file removed: {summary_file}")

            return True

        except Exception as e:
            self.logger.error(f"Error clearing logs: {str(e)}")
            return False


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

        # Send email with logs and git diffs
        logger.logger.info("Sending email with logs and git diffs...")
        if logger.send_email_with_logs():
            logger.logger.info("Email sent successfully. Clearing logs...")
            logger.clear_logs()
        else:
            logger.logger.error("Failed to send email. Logs will NOT be cleared.")
            logger.create_summary_report()

    except KeyboardInterrupt:
        logger.logger.info("\nMonitoring stopped by user")
        logger.logger.info("Sending email with logs and git diffs...")
        if logger.send_email_with_logs():
            logger.logger.info("Email sent successfully. Clearing logs...")
            logger.clear_logs()
        else:
            logger.logger.error("Failed to send email. Keeping logs for manual review.")
            logger.create_summary_report()
    except Exception as e:
        logger.logger.error(f"Error during monitoring: {str(e)}")
        logger.logger.info("Attempting to send email with logs...")
        if logger.send_email_with_logs():
            logger.logger.info("Email sent successfully. Clearing logs...")
            logger.clear_logs()
        else:
            logger.logger.error("Failed to send email. Keeping logs for manual review.")
            logger.create_summary_report()


if __name__ == "__main__":
    main()
