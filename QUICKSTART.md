# Quick Start Guide 🚀

Get the Email Verification Tool running in 2 minutes.

## Step 1: Install Python
- Download from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- Verify: Open terminal/cmd and type `python --version`

## Step 2: Install Dependencies
Open terminal/cmd in this folder and run:

```bash
pip install -r requirements.txt
```

## Step 3: Choose Your Interface

### Option A: Beautiful Web Interface (RECOMMENDED) ⭐
```bash
streamlit run app.py
```
- Opens in browser automatically
- Beautiful, user-friendly UI
- Shows all 4 verification phases in real-time

### Option B: Lightweight API
```bash
python flask_app.py
```
- Lightweight HTTP server
- Good for integration with other apps
- Open at http://localhost:5000

### Option C: Command Line Testing
```bash
python test_emails.py
```
- Direct Python execution
- Good for scripting/automation
- No GUI

## That's It! 🎉

Now enter an email address and watch it get verified through all 4 phases:

1. **Syntax Validation** ✅ - Checks if email format is valid
2. **Domain/MX Check** ✅ - Verifies domain has mail servers
3. **SMTP Handshake** ✅ - Connects to mail server and validates inbox
4. **Web Presence** ✅ - Checks Gravatar and public records

## Troubleshooting

### "Command not found: python"
- Make sure Python is installed and added to PATH
- Restart terminal after installing Python
- Try `python3` instead of `python`

### "ModuleNotFoundError"
- Make sure you ran `pip install -r requirements.txt`
- Check that requirements.txt is in the same folder

### "Port already in use"
- Another app is using the port
- Close the other app or use a different interface
- Streamlit tries ports 8501-8505 automatically

## Next Steps

1. ✅ Test with your own email address
2. ✅ Read [README.md](README.md) for detailed documentation
3. ✅ Check [INSTALLATION.md](INSTALLATION.md) for advanced setup
4. ✅ Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for integration
5. ✅ Explore [config.py](config.py) for customization

## File Structure

```
Email/
├── email_verifier.py          # Core verification logic
├── app.py                     # Streamlit web interface
├── flask_app.py              # Flask API & web interface
├── templates/
│   └── index.html            # Flask HTML template
├── test_emails.py            # Test script
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── README.md                 # Full documentation
├── INSTALLATION.md           # Installation guide
└── API_DOCUMENTATION.md      # API reference
```

## What Each File Does

| File | Purpose |
|------|---------|
| `email_verifier.py` | Core verification logic (all 4 phases) |
| `app.py` | Streamlit web interface (recommended) |
| `flask_app.py` | Flask API server |
| `templates/index.html` | Web UI for Flask |
| `test_emails.py` | Test suite for verification |
| `config.py` | Configuration & settings |
| `requirements.txt` | Python package dependencies |

## Common Use Cases

### Just Want to Verify an Email?
```bash
streamlit run app.py
```
Type an email in the web interface and click "Verify"

### Want an API for Your App?
```bash
python flask_app.py
```
Then make POST requests to `http://localhost:5000/api/verify`

### Want to Process a List of Emails?
```python
from email_verifier import verify_email

emails = ["email1@example.com", "email2@example.com"]
for email in emails:
    result = verify_email(email)
    print(f"{email}: {result['overall_status']}")
```

### Want to Deploy to Cloud?
See [INSTALLATION.md](INSTALLATION.md) for Docker and cloud deployment options.

## Features

✅ **No Paid APIs** - Uses only free libraries
✅ **RFC 5322 Validation** - Checks email format
✅ **MX Record Lookup** - Verifies domain has mail servers
✅ **SMTP Connection** - Tests if inbox actually exists
✅ **Greylisting Detection** - Identifies temporary rejections
✅ **Web Presence Check** - Finds email in public records
✅ **Timeout Protection** - 10-second timeout prevents hanging
✅ **Beautiful UI** - Streamlit or Flask interface
✅ **Open Source** - Free to use and modify

## Results Meanings

| Status | Meaning |
|--------|---------|
| ✅ **VALID** | Email is correct, domain exists, inbox accepts mail |
| ❌ **INVALID** | Email format wrong, domain missing, or server rejected it |
| ⚠️ **UNDETERMINED** | Domain valid but SMTP test inconclusive (greylisted/timeout) |
| ❓ **UNKNOWN** | Unexpected result or error |

## Tips & Tricks

1. **Faster verification** - Disable "Check Web Presence" to skip Phase 4
2. **Test mode** - Run `python test_emails.py` to see example results
3. **Customize timeout** - Edit `config.py` to adjust SMTP timeout
4. **Add domains** - Edit `config.py` to add more disposable email providers
5. **Batch processing** - Use Python module for loops and file processing

## Getting Help

1. Check [README.md](README.md) for detailed features
2. Check [INSTALLATION.md](INSTALLATION.md) for setup issues
3. Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for integration
4. Review code comments in `email_verifier.py`
5. Run `python test_emails.py` to verify installation

## Need More Info?

📖 **[Full README](README.md)** - Complete feature documentation
🛠️ **[Installation Guide](INSTALLATION.md)** - Detailed setup instructions
💻 **[API Docs](API_DOCUMENTATION.md)** - For developers & integration

---

**That's it! You're ready to verify emails. Happy verifying! 🎉**
