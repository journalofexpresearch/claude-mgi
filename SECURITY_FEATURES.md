# Security Features - Login Monitoring System

## 🛡️ Anti-Tampering Protection (CRITICAL)

### The Problem This Solves

**Without protection:**
1. You start monitoring
2. Intruder logs in
3. Intruder finds the log files
4. Intruder deletes logs
5. **You have NO evidence**

**With protection:**
1. You start monitoring
2. Intruder logs in (logged)
3. Intruder tries to view logs
4. **INSTANT EMAIL TRIGGERED**
5. Logs emailed to you
6. Logs cleared locally
7. **You have evidence, they have nothing**

---

## How It Works

### Real-Time File Monitoring

The system monitors these files **every 2 seconds**:
- `login_details.log` - Main activity log
- `login_details_summary.txt` - Summary report
- `scripts/email_config.json` - Email credentials
- `scripts/login_logger.py` - The logger itself
- `scripts/file_access_monitor.py` - The protection system

### What Triggers Immediate Email

**ANY** of these actions:

1. **Viewing files:**
   ```bash
   cat login_details.log           # TRIGGERS
   less login_details.log          # TRIGGERS
   nano login_details.log          # TRIGGERS
   vim login_details.log           # TRIGGERS
   ```

2. **Modifying files:**
   ```bash
   echo "" > login_details.log     # TRIGGERS
   rm login_details.log            # TRIGGERS
   mv login_details.log backup.log # TRIGGERS
   ```

3. **Git operations:**
   ```bash
   git status                      # TRIGGERS
   git diff                        # TRIGGERS
   git log                         # TRIGGERS
   git add login_details.log       # TRIGGERS
   ```

4. **GitHub web interface:**
   - Viewing file in browser        # TRIGGERS
   - Downloading file               # TRIGGERS
   - Editing via web UI             # TRIGGERS

### Response Chain (< 5 seconds)

```
File Accessed
    ↓
Security Alert Logged
    ↓
Email Created (with all current logs + git diffs)
    ↓
Email Sent to iseeyouiswatching@gmail.com
    ↓
Logs Cleared Locally
    ↓
Monitoring Continues
```

**Total time from access to cleared logs: ~5 seconds**

---

## Two Email Scenarios

### Scenario 1: Scheduled Email (7am)

**When:** Clock hits 7:00 AM
**Contains:**
- All login activity from session
- Git diffs
- Summary report
**Then:** Logs cleared, monitoring can restart

### Scenario 2: Emergency Email (Tampering Detected)

**When:** Someone accesses monitored files
**Contains:**
- All login activity up to that moment
- Git diffs
- **SECURITY ALERT** in logs
- Details of which file was accessed
**Then:** Logs cleared immediately, monitoring continues

---

## Why "Clear After Email" is Critical

### Traditional Logging Problem:
```
Logs accumulate → Intruder finds them → Deletes them → No evidence
```

### Our Approach:
```
Evidence generated → Immediately emailed → Logs cleared → Intruder finds nothing
```

**Key Insight:** Local logs are a **liability** if someone has access to the system.

**Solution:** Treat email as the **source of truth**, local logs as **volatile evidence**.

---

## Defense Against Sophisticated Attackers

### Attack: "I'll just disable the monitor"

**Attempt:**
```bash
pkill -f login_logger.py
```

**Result:**
- Process killed
- But logs already exist
- Next time they try to check if it worked...
- They read the log file to see if monitoring stopped
- **TRIGGER!** Email sent with evidence

### Attack: "I'll delete the email config so it can't send"

**Attempt:**
```bash
rm scripts/email_config.json
```

**Result:**
- File deletion triggers file access alert
- Email sent **before** deletion completes
- Config file used **during** the email send
- Evidence preserved

### Attack: "I'll modify the logger to disable this feature"

**Attempt:**
```bash
nano scripts/login_logger.py
```

**Result:**
- Opening file triggers access alert
- Email sent with current logs
- Even if they modify the code, evidence is already emailed
- Modification itself is logged in git diffs

### Attack: "I'll use GitHub API to read files without triggering filesystem alerts"

**Result:**
- Git index changes when files are accessed via API
- Monitor checks `.git/index` modification time
- Still triggers alert (may have short delay)

---

## What You Should Expect

### Normal Operation

**Your inbox at 7am:**
- One email with subject "Login Monitoring Report - [timestamp]"
- Contains your login activity
- No security alerts

### Intrusion Detected

**Your inbox anytime:**
- Email with subject "Login Monitoring Report - [timestamp]"
- Contains login activity **plus**
- Security alert in logs: `"event": "SECURITY_BREACH"`
- Details which file was accessed
- **This means someone discovered the monitoring**

**What to do:**
1. Review the logs for unfamiliar IPs
2. Change your password immediately
3. Enable 2FA if not already enabled
4. Check for unauthorized changes
5. Consider the account compromised

---

## Limitations and Considerations

### What This Does NOT Protect Against

1. **Attacker with root access:**
   - Could kill process before file access
   - Could modify kernel to hide file access
   - **Mitigation:** Run on system where you control root

2. **Network-level blocking:**
   - Could block outbound SMTP
   - **Mitigation:** Use port 587 (often allowed), VPN

3. **Email account compromise:**
   - Could delete emails
   - **Mitigation:** Use dedicated email, enable email forwarding

4. **Kernel-level rootkits:**
   - Could hide file access from OS
   - **Mitigation:** This assumes non-root attacker

### Assumptions

This system assumes:
- ✅ Attacker has user-level access (your credentials)
- ✅ Attacker does NOT have root/admin access
- ✅ Network allows outbound SMTP (port 587)
- ✅ Your email account is secure
- ✅ Filesystem access times are accurate

**Target threat:** Stolen credentials, not compromised system

---

## Best Practices

### 1. Dedicated Email Account
```
✅ GOOD: monitoring-alerts@gmail.com (dedicated)
❌ BAD:  your-main-email@gmail.com (they could access this too)
```

### 2. Email Forwarding
```
Setup: monitoring-alerts@gmail.com → your-phone@sms-gateway.com
Result: Instant SMS alerts
```

### 3. Regular Checks
```
- Check email even if no alert (verify system is working)
- Test occasionally by manually reading a log
- Verify you receive the test alert email
```

### 4. Response Plan
```
IF (security alert email received):
    1. Assume credentials compromised
    2. Change password from DIFFERENT device
    3. Enable 2FA
    4. Review all account activity
    5. Check for data exfiltration
    6. Consider account fully compromised
```

---

## Testing the System

### Safe Test (Won't trigger alert)
```bash
# Check if monitoring is running
ps aux | grep login_logger

# View the process
top -p $(pgrep -f login_logger)
```

### Alert Test (WILL trigger alert)
```bash
# This will send you an email:
cat login_details.log
```

**Expected result:**
- Email arrives within ~10 seconds
- Contains current logs
- Security alert in JSON: `"event": "SECURITY_BREACH"`
- Local logs cleared

---

## Technical Details

### File Access Detection Method

Uses `os.stat()` to check:
- `st_atime` - Last access time (read)
- `st_mtime` - Last modification time (write)

**Check frequency:** Every 2 seconds

**Threshold:** If access time changed by >5 seconds, trigger

**Why 5 seconds?** Prevents our own logging from triggering alerts.

### Email Delivery

**Protocol:** SMTP over TLS (port 587)
**Timeout:** 30 seconds
**Retry:** None (fail-fast to prevent blocking)
**Size limit:** ~10MB (log files + attachments)

### Log Clearing

**Method:** Overwrite with timestamp, then delete summaries

**Content after clear:**
```
# Log cleared at 2026-01-11T08:30:15.123456
# Previous logs have been emailed
```

**Purpose:**
- Not completely empty (less suspicious)
- Timestamp shows when cleared
- Prevents old logs from lingering

---

## Summary

**This system operates on a simple principle:**

> "Evidence that reaches your email is safe. Evidence on the system is at risk."

**Every piece of evidence is immediately exfiltrated and the local copy destroyed.**

**You depend ONLY on email. Trust nothing on the monitored system.**

This is **intentional** and **critical** to the security model.
