# Installation & Setup Guide

Complete step-by-step guide to set up and run the Email Verification Tool.

## Quick Start (5 minutes)

### 1. Install Python
- **Required:** Python 3.8 or higher
- **Download:** https://www.python.org/downloads/
- **Verify:** Open terminal/cmd and run:
  ```bash
  python --version
  ```

### 2. Clone/Download Project
```bash
# Navigate to your desired location
cd /path/to/Email

# Or download as ZIP and extract
```

### 3. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

### 4. Run the Tool

**Option A: Streamlit Interface (Recommended for Beginners)**
```bash
streamlit run app.py
```
- Opens automatically in browser at `http://localhost:8501`
- Beautiful, interactive interface
- Real-time phase updates

**Option B: Flask Interface (Lightweight & API)**
```bash
python flask_app.py
```
- Opens at `http://localhost:5000`
- Lightweight HTTP server
- REST API available

**Option C: Command Line / Python Script**
```bash
python test_emails.py
```
- Direct Python execution
- Good for scripting/automation
- No GUI required

## Detailed Setup

### Windows Users

#### 1. Using Command Prompt (cmd.exe)
```cmd
# Navigate to project folder
cd C:\Users\YourUsername\Desktop\Email

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run app.py
```

#### 2. Using PowerShell
```powershell
# Navigate to project folder
cd C:\Users\YourUsername\Desktop\Email

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run app.py
```

### macOS/Linux Users

```bash
# Navigate to project folder
cd ~/Desktop/Email

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run app.py
```

## Virtual Environment Setup (Recommended)

Virtual environments isolate project dependencies and prevent conflicts.

### Create Virtual Environment
```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows (cmd):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### You'll see `(venv)` prefix in terminal when active

### Deactivate When Done
```bash
deactivate
```

## Choosing Your Interface

### 1. Streamlit (`app.py`) - **RECOMMENDED**
**Pros:**
- Beautiful, modern UI
- Real-time phase updates
- Settings sidebar
- JSON export
- Mobile responsive

**Cons:**
- Requires Streamlit package
- Slightly heavier (~100MB)

**Run:**
```bash
streamlit run app.py
```

**Browser:** http://localhost:8501

### 2. Flask (`flask_app.py`) - **LIGHTWEIGHT**
**Pros:**
- Minimal dependencies
- REST API available
- Lightweight (~5MB)
- Good for embedding

**Cons:**
- More basic UI
- Requires manual API calls for automation

**Run:**
```bash
python flask_app.py
```

**Browser:** http://localhost:5000

### 3. Python Module - **FOR DEVELOPERS**
**Pros:**
- Direct control
- No UI overhead
- Great for scripting
- Easiest to integrate

**Cons:**
- No web interface
- Requires Python knowledge

**Usage:**
```python
from email_verifier import verify_email

result = verify_email("user@example.com")
print(result)
```

## Testing the Installation

### Quick Test
```bash
python -c "import dns.resolver, requests, smtplib; print('✅ All dependencies installed!')"
```

### Run Test Suite
```bash
python test_emails.py
```

Expected output:
- Shows verification status for multiple test emails
- Tests syntax validation, MX lookup, SMTP, web presence
- Displays summary statistics

## Configuration

### Customize Settings
Edit `config.py` to adjust:
- SMTP timeout (default: 10 seconds)
- Disposable email domains list
- DNS timeout
- Logging level
- Rate limiting (future)

### Example Configuration Change
```python
# config.py
SMTP_TIMEOUT = 15  # Increase timeout to 15 seconds
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install -r requirements.txt
```

### "Cannot connect to mail server"
**Causes:**
- Firewall blocking port 25
- ISP blocking outgoing SMTP
- Mail server temporarily unavailable

**Solution:**
- Check internet connection
- Try different email domains
- Check firewall settings

### "DNS resolution failed"
**Causes:**
- DNS server unavailable
- Network connectivity issue

**Solution:**
- Check internet connection
- Verify domain exists

### "Connection timeout"
**Cause:** Mail server too slow to respond

**Solution:**
- Increase `SMTP_TIMEOUT` in config.py
- Some mail servers are just slow
- Mark as "undetermined" if needed

### Port 5000/8501 Already in Use
**Solution:**
```bash
# Kill process using port
# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

## Upgrading Dependencies

Check for updates:
```bash
pip list --outdated
```

Update specific package:
```bash
pip install --upgrade streamlit
```

Update all:
```bash
pip install -r requirements.txt --upgrade
```

## Running Multiple Interfaces

You can run both simultaneously:

**Terminal 1 - Streamlit:**
```bash
streamlit run app.py
```

**Terminal 2 - Flask:**
```bash
python flask_app.py
```

Access at:
- Streamlit: http://localhost:8501
- Flask: http://localhost:5000

## Docker Setup (Optional)

If you have Docker installed:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t email-verifier .
docker run -p 8501:8501 email-verifier
```

## Deployment to Cloud

### Heroku Deployment
```bash
# Requires Heroku CLI
heroku create your-app-name
git push heroku main
```

### AWS Deployment
```bash
# Use EC2 or Elastic Beanstalk
# See official AWS documentation for details
```

### Railway Deployment
```bash
# Easy deployment with railway.app
# Connect GitHub repo and deploy
```

## Performance Optimization

### For Large Batch Processing
```bash
# Use test_emails.py with modifications
# Or create batch_verify.py for CSV processing
```

### Memory Usage
- Single verification: ~10MB
- Streamlit + Flask combined: ~150MB total
- Python overhead: ~30MB

### Speed Optimization
```python
# In config.py
SMTP_TIMEOUT = 5  # Reduce for faster timeouts
DNS_TIMEOUT = 3   # Faster DNS lookups
```

## Uninstalling

### Remove Virtual Environment
```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

### Uninstall Packages
```bash
pip uninstall -r requirements.txt -y
```

## Support & Help

1. Check **README.md** for feature documentation
2. Review **config.py** for configuration options
3. Run **test_emails.py** to verify setup
4. Check error messages in terminal output
5. Review code comments in `email_verifier.py`

## Next Steps

- [ ] Verify installation with `test_emails.py`
- [ ] Run Streamlit or Flask interface
- [ ] Test with your email address
- [ ] Configure settings as needed
- [ ] Integrate into your project
- [ ] Scale for batch processing
- [ ] Deploy to cloud if needed

---

**You're all set! 🎉 Start verifying emails now.**
