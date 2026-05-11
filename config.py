"""
Configuration file for Email Verification Tool
Adjust settings here for your deployment
"""

# SMTP Configuration
SMTP_TIMEOUT = 10  # seconds - timeout for connecting to mail servers
SMTP_PORT = 25     # Standard SMTP port (unencrypted)
SMTP_HELO_NAME = "mail.example.com"  # HELO greeting name

# Email Validation Settings
MAX_EMAIL_LENGTH = 254  # RFC 5321 max email length
MAX_LOCAL_PART_LENGTH = 64  # RFC 5321 max local part length

# Disposable Email Providers
# Add more domains here as needed
DISPOSABLE_DOMAINS = {
    # Temporary mail services
    'tempmail.com',
    '10minutemail.com',
    'guerrillamail.com',
    'mailinator.com',
    'temp-mail.org',
    'throwaway.email',
    'yopmail.com',
    'maildrop.cc',
    'temp-mail.io',
    'mail-temp.com',
    'sharklasers.com',
    'temp-mail.at',
    'tmpemail.com',
    'mytrashmail.com',
    'fakeinbox.com',
    'testmail.com',
    
    # Development/testing domains
    'test.com',
    'example.com',
    'example.org',
    'example.net',
    'localhost',
}

# DNS Configuration
DNS_TIMEOUT = 5  # seconds - timeout for DNS lookups
DNS_RETRY_COUNT = 2  # Number of retries for DNS queries

# Web Presence Checking
CHECK_GRAVATAR = True  # Check Gravatar profile
GRAVATAR_TIMEOUT = 5  # seconds - timeout for Gravatar check

# Server Response Codes
SMTP_CODES = {
    250: "OK",
    450: "Greylisted (Temporary Rejection)",
    451: "Greylisted (Service Unavailable)",
    500: "Syntax Error",
    501: "Argument Syntax Error",
    502: "Command Not Implemented",
    503: "Bad Sequence",
    504: "Parameter Not Implemented",
    550: "Mailbox Not Found",
    551: "User Not Local",
    552: "Mailbox Full",
    553: "Invalid Mailbox Name",
    554: "Transaction Failed",
}

# Flask Configuration (if using Flask)
FLASK_DEBUG = False
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_ENV = "production"

# Streamlit Configuration (if using Streamlit)
# These are set in ~/.streamlit/config.toml

# Logging Configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "email_verification.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Rate Limiting (future feature)
RATE_LIMIT_ENABLED = False
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 3600  # seconds (1 hour)

# Batch Processing (future feature)
BATCH_SIZE = 10
BATCH_TIMEOUT = 300  # seconds

# API Keys (for future integrations)
# Leave empty if not using any external services
HUNTER_API_KEY = ""
CLEARBIT_API_KEY = ""
