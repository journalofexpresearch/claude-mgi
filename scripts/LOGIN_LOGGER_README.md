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
4. Create a summary report

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
