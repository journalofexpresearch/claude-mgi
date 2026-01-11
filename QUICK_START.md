# Quick Start Guide - Login Monitoring

## Setup (5 minutes)

### Step 1: Configure Email

```bash
cd /home/user/claude-mgi
cp scripts/email_config.json.example scripts/email_config.json
nano scripts/email_config.json
```

**Edit the file and fill in:**
- `sender_email`: Your Gmail address
- `sender_password`: Your Gmail App Password (NOT regular password)
- `recipient_email`: Already set to `iseeyouiswatching@gmail.com`

### Step 2: Get Gmail App Password

1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Other (Custom name)"
3. Name it "Login Logger"
4. Copy the 16-character password
5. Paste it in `email_config.json` as `sender_password`

### Step 3: Start Monitoring

```bash
# Run in foreground (see output)
python3 scripts/login_logger.py

# OR run in background (continues even if you close terminal)
nohup python3 scripts/login_logger.py > /dev/null 2>&1 &
```

## What Happens

**Now → 7am:**
- Logs every 5 minutes
- Records: IP, hostname, timestamp, system info

**At 7am:**
- ✅ Emails everything to iseeyouiswatching@gmail.com
- ✅ Includes all login logs
- ✅ Includes git diffs (any file changes)
- ✅ Clears logs after successful email

**Email contains:**
- Attached: `login_details.log`
- Attached: `login_details_summary.txt`
- In body: Git status, diffs, recent commits

## Stop Monitoring

```bash
# If running in foreground
Ctrl+C

# If running in background
pkill -f login_logger.py
```

## Troubleshooting

**"Email config not found"**
- Did you copy `email_config.json.example` to `email_config.json`?
- Is it in the `scripts/` folder?

**"Email send failed"**
- Are you using an App Password (not regular password)?
- Is 2FA enabled on your Gmail?
- Check your internet connection

**"Permission denied"**
```bash
chmod +x scripts/login_logger.py
```

## Security Notes

- Never commit `email_config.json` (already in .gitignore)
- Never commit `*.log` files (already in .gitignore)
- Use App Passwords, never regular passwords
- Email is sent over TLS (encrypted)

## Check If It's Running

```bash
# See if process is active
ps aux | grep login_logger

# View recent logs
tail -n 20 login_details.log
```

---

**IMPORTANT:** This monitors YOUR activity to detect if someone else is using your credentials. Review the emailed logs for unfamiliar IP addresses, timestamps, or locations.
