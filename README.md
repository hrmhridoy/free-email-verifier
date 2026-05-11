# Email Verification Tool 🔍

A **lightweight, open-source email verification tool** written in Python that requires **zero paid APIs** or external subscriptions. Verify emails through 4 comprehensive phases with a beautiful Streamlit web interface.

## Features ✨

- ✅ **RFC 5322 Syntax Validation** - Robust regex pattern for email format checking
- ✅ **DNS MX Record Lookup** - Verifies domain has mail servers (using dnspython)
- ✅ **SMTP Handshake** - Connects to mail servers on Port 25 to validate inbox exists
- ✅ **Greylisting Detection** - Identifies temporary server rejections (codes 450/451)
- ✅ **Web Presence Check** - Searches Gravatar and public records for email verification
- ✅ **Timeout Protection** - 10-second timeout on SMTP connections prevents hanging
- ✅ **Real-time UI** - Beautiful Streamlit interface with live feedback
- ✅ **Zero Paid APIs** - Uses only free libraries: dnspython, smtplib, requests

## Installation 🚀

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd Email
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage 📖

### Running the Streamlit Web Interface

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

**Interface:**
1. Enter an email address in the text field
2. Optional: Enable/disable "Check Web Presence" in the sidebar
3. Click "🔍 Verify" to start the verification process
4. See real-time results as each phase completes

### Using as a Python Module

```python
from email_verifier import verify_email

# Basic usage
result = verify_email("user@example.com")
print(result['overall_status'])  # "valid", "invalid", or "undetermined"

# With options
result = verify_email("user@example.com", check_web_presence=False)
print(result)
```

## Verification Phases 🔄

### Phase 1: Syntax Validation
- **Purpose:** Check if email format is valid according to RFC 5322 standards
- **Method:** Regular expression pattern matching
- **Checks:**
  - Email is not empty
  - Doesn't exceed 254 characters
  - Local part (before @) doesn't exceed 64 characters
  - Matches RFC 5322 pattern
- **Status Codes:** ✅ passed | ❌ failed

### Phase 2: Domain/MX Record Check
- **Purpose:** Verify domain exists and has mail servers
- **Method:** DNS MX record lookup using dnspython
- **Checks:**
  - Domain is not a known disposable email provider
  - Domain has valid MX records
  - Returns all MX records with priority levels
- **Status Codes:** ✅ passed | ❌ failed | ⚠️ error

### Phase 3: SMTP Handshake (Port 25)
- **Purpose:** Validate inbox exists on mail server
- **Method:** SMTP protocol handshake with timeout protection
- **Handshake Process:**
  1. Connect to MX server on Port 25 (10-second timeout)
  2. Send HELO greeting
  3. Send MAIL FROM (test@example.com)
  4. Send RCPT TO (target email)
  5. Send QUIT immediately (no email sent)
- **Server Response Codes:**
  - **250 OK** → ✅ Inbox exists
  - **450/451** → ⚠️ Greylisted (temporary rejection)
  - **550-553** → ❌ Permanent rejection
  - **Timeout/No Connection** → ❌ Failed
- **Status Codes:** ✅ passed | ❌ failed | ⚠️ greylisted | 🔄 skipped

### Phase 4: Web Presence Search
- **Purpose:** Find email in public records/profiles
- **Methods:**
  - Gravatar profile lookup (MD5 hash-based)
  - Checks if email has associated Gravatar profile
- **Status Codes:** ✅ found | ⚠️ not_found | ❌ error

## Overall Status Meanings 📊

| Status | Meaning |
|--------|---------|
| **✅ VALID** | Email syntax correct + domain exists + mail server accepted inbox |
| **❌ INVALID** | Email format wrong OR domain doesn't exist OR server rejected it |
| **⚠️ UNDETERMINED** | Domain valid but SMTP check was inconclusive (greylisted or connection timeout) |
| **❓ UNKNOWN** | Unexpected result or error during verification |

## Configuration Options ⚙️

### SMTP Timeout
```python
EmailVerifier.SMTP_TIMEOUT = 10  # seconds (default)
```

### Disposable Email Domains
Built-in list of known disposable providers. Easily extensible:
```python
DISPOSABLE_DOMAINS = {
    'tempmail.com', '10minutemail.com', ...
}
```

## Output Format 📋

JSON structure returned by `verify_email()`:

```json
{
  "email": "user@example.com",
  "overall_status": "valid",
  "phase_1": {
    "status": "passed",
    "valid": true,
    "message": "Email syntax is valid"
  },
  "phase_2": {
    "status": "passed",
    "valid": true,
    "message": "Found 5 MX record(s)",
    "mx_records": [
      {"host": "alt1.gmail-smtp-in.l.google.com", "priority": 5}
    ]
  },
  "phase_3": {
    "status": "passed",
    "valid": true,
    "message": "✓ Inbox exists (server accepted recipient)",
    "server": "gmail-smtp-in.l.google.com"
  },
  "phase_4": {
    "status": "not_found",
    "valid": false,
    "message": "No public profile found"
  }
}
```

## Important Notes ⚠️

### SMTP Connection Details
- **Port:** 25 (standard SMTP, no TLS/SSL for simplicity)
- **Timeout:** 10 seconds prevents hanging on slow/unresponsive servers
- **QUIT Command:** Ensures no email is actually sent; closes connection cleanly
- **Test Sender:** Uses "test@example.com" as MAIL FROM (not a real send)

### Greylisting
Some mail servers use greylisting (temporarily rejecting unfamiliar senders) to prevent spam:
- **Response Codes:** 450, 451
- **Tool Behavior:** Marks as "Undetermined/Greylisted"
- **Recommendation:** Retry after 30+ minutes for greylisted addresses

### Privacy & Security
- ✅ All processing is local (except DNS and SMTP connections)
- ✅ No data stored or logged
- ✅ Only connects to mail servers required for verification
- ✅ Immediately sends QUIT after RCPT TO (no email delivery)
- ✅ Open source - audit the code yourself

## Limitations 🚫

1. **Cannot verify inbox without SMTP** - Some servers may temporarily reject connections
2. **Greylisting uncertainty** - Can't distinguish between greylisting and invalid inbox
3. **Some servers may rate limit** - Many corporate servers limit SMTP verification attempts
4. **No authentication** - Only uses HELO (not authenticated connection)
5. **Free tier only** - No premium features from email validation APIs

## Troubleshooting 🔧

### "Could not connect to any MX server"
- **Cause:** Mail servers unreachable or rejecting connections
- **Solution:** Check your internet connection, verify domain exists, or try again later

### "Timeout" on SMTP check
- **Cause:** Mail server is slow to respond
- **Solution:** Increase `SMTP_TIMEOUT` value or mark as "undetermined"

### DNS resolution errors
- **Cause:** Network issues or invalid domain
- **Solution:** Verify domain exists, check internet connection

### "Greylisted" status
- **Cause:** Server temporarily rejected the verification attempt
- **Solution:** This is normal for first-time verification; retry after 30+ minutes

## Performance 📈

- **Phase 1:** < 100ms (regex check)
- **Phase 2:** 200-800ms (DNS lookup)
- **Phase 3:** 1-5 seconds (SMTP handshake, varies by server)
- **Phase 4:** 1-3 seconds (web presence check)
- **Total:** 2-10 seconds (depends on server responsiveness)

## Dependencies 📦

| Package | Purpose | License |
|---------|---------|---------|
| streamlit | Web UI framework | Apache 2.0 |
| dnspython | DNS MX record lookup | ISC |
| requests | HTTP requests for web presence | Apache 2.0 |

## Architecture 🏗️

```
email_verifier.py (Core Logic)
├── EmailVerifier class
│   ├── _phase_1_syntax_validation()
│   ├── _phase_2_mx_check()
│   ├── _phase_3_smtp_handshake()
│   ├── _phase_4_web_presence()
│   └── verify()
├── EmailVerificationResult class (data container)
└── verify_email() (simple API)

app.py (Streamlit Interface)
├── Layout & styling
├── Input handling
├── Results display
└── Phase visualization
```

## Example Workflow 🎯

```
User enters: alice@company.com
    ↓
Phase 1: ✅ Valid format
    ↓
Phase 2: ✅ MX records found
    ↓
Phase 3: ✅ Server accepted recipient
    ↓
Phase 4: ⚠️ No Gravatar profile
    ↓
Overall: ✅ VALID
```

## Contributing 🤝

This is an open-source project. To contribute:

1. Test different email providers
2. Add more web presence check methods
3. Improve regex pattern for edge cases
4. Add configuration UI
5. Report issues or suggest features

## License 📜

This project is open-source and free to use for personal and commercial purposes.

## Future Enhancements 🚀

- [ ] Flask API version
- [ ] Batch verification (CSV import)
- [ ] Email list validation
- [ ] Database storage of results
- [ ] More web presence sources (LinkedIn, Twitter, etc.)
- [ ] Rate limiting and retry logic
- [ ] Docker containerization
- [ ] REST API endpoint
- [ ] Scheduled verification jobs

## Support 💬

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting-🔧) section
2. Review the code comments in `email_verifier.py`
3. Test with known valid/invalid emails first

---

**Built with ❤️ using Python, dnspython, and Streamlit**
