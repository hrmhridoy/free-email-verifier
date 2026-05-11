# Email Verification Tool - API Documentation

Complete API reference for developers integrating the Email Verification Tool.

## Overview

The Email Verification Tool provides three interfaces:
1. **Streamlit Web UI** - Interactive browser interface
2. **Flask REST API** - HTTP API endpoints
3. **Python Module** - Direct Python integration

---

## Python Module API

### Import

```python
from email_verifier import EmailVerifier, verify_email, EmailVerificationResult
```

### Quick Function

**Simplest way to verify an email:**

```python
from email_verifier import verify_email

result = verify_email("user@example.com")
print(result['overall_status'])  # "valid", "invalid", or "undetermined"
```

**Parameters:**
- `email` (str): Email address to verify
- `check_web_presence` (bool, optional): Check Gravatar/public records (default: True)

**Returns:** Dictionary with verification results

### EmailVerifier Class

For more control and reusability:

```python
from email_verifier import EmailVerifier

verifier = EmailVerifier()
result_obj = verifier.verify("user@example.com", check_web_presence=True)

# Access results
print(result_obj.overall_status)  # "valid", "invalid", "undetermined"
print(result_obj.to_dict())       # Convert to dictionary
```

### EmailVerificationResult Object

Contains all verification data:

```python
result = verifier.verify("user@example.com")

# Overall status
print(result.overall_status)  # "valid" | "invalid" | "undetermined" | "unknown"

# Phase results
print(result.phase_1)  # {"status": "passed", "valid": True, "message": "..."}
print(result.phase_2)  # {"status": "passed", "valid": True, "message": "...", "mx_records": [...]}
print(result.phase_3)  # {"status": "passed", "valid": True, "message": "...", "server": "..."}
print(result.phase_4)  # {"status": "found", "valid": True, "message": "..."}

# Convert to dictionary for JSON serialization
result_dict = result.to_dict()
```

### Result Structure

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
      {
        "host": "mail.example.com",
        "priority": 10
      }
    ]
  },
  "phase_3": {
    "status": "passed",
    "valid": true,
    "message": "✓ Inbox exists (server accepted recipient)",
    "server": "mail.example.com"
  },
  "phase_4": {
    "status": "not_found",
    "valid": false,
    "message": "No public profile found"
  }
}
```

### Usage Examples

#### Basic Verification
```python
from email_verifier import verify_email

# Verify single email
result = verify_email("alice@company.com")
if result['overall_status'] == 'valid':
    print("✅ Email is valid!")
else:
    print("❌ Email is invalid!")
```

#### Batch Verification
```python
from email_verifier import EmailVerifier

emails = [
    "user1@example.com",
    "user2@example.com",
    "user3@example.com",
]

verifier = EmailVerifier()
results = []

for email in emails:
    result = verifier.verify(email)
    results.append({
        'email': email,
        'status': result.overall_status
    })

for r in results:
    print(f"{r['email']}: {r['status']}")
```

#### Skip Web Presence Check (Faster)
```python
from email_verifier import verify_email

# Skip Phase 4 for faster verification
result = verify_email("user@example.com", check_web_presence=False)
print(f"Status: {result['overall_status']}")
```

#### Error Handling
```python
from email_verifier import EmailVerifier

verifier = EmailVerifier()

try:
    result = verifier.verify("user@example.com")
    print(f"Status: {result.overall_status}")
except Exception as e:
    print(f"Error: {str(e)}")
```

#### Filter by Phase
```python
from email_verifier import verify_email

result = verify_email("user@example.com")

# Only check Phase 1 & 2
if result['phase_1']['status'] == 'passed' and result['phase_2']['status'] == 'passed':
    print("✅ Email format and domain are valid")
else:
    print("❌ Email format or domain is invalid")
```

---

## Flask REST API

### Base URL
```
http://localhost:5000
```

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

#### Verify Email
```http
POST /api/verify
Content-Type: application/json

{
  "email": "user@example.com",
  "check_web_presence": true
}
```

**Parameters:**
- `email` (string, required): Email address to verify
- `check_web_presence` (boolean, optional): Check Gravatar/public records (default: true)

**Response (200 OK):**
```json
{
  "email": "user@example.com",
  "overall_status": "valid",
  "phase_1": { ... },
  "phase_2": { ... },
  "phase_3": { ... },
  "phase_4": { ... }
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Email is required"
}
```

### cURL Examples

#### Basic Verification
```bash
curl -X POST http://localhost:5000/api/verify \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

#### Skip Web Presence Check
```bash
curl -X POST http://localhost:5000/api/verify \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "check_web_presence": false
  }'
```

#### Health Check
```bash
curl http://localhost:5000/health
```

### Python Requests Example

```python
import requests
import json

# Verify email via Flask API
response = requests.post(
    'http://localhost:5000/api/verify',
    json={
        'email': 'user@example.com',
        'check_web_presence': True
    }
)

if response.status_code == 200:
    result = response.json()
    print(f"Status: {result['overall_status']}")
    print(json.dumps(result, indent=2))
else:
    print(f"Error: {response.text}")
```

### JavaScript Fetch Example

```javascript
// Verify email via Flask API
async function verifyEmail(email) {
    const response = await fetch('/api/verify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            check_web_presence: true
        })
    });
    
    if (response.ok) {
        const result = await response.json();
        console.log(`Status: ${result.overall_status}`);
        console.log(result);
    } else {
        console.error('Verification failed');
    }
}

// Usage
verifyEmail('user@example.com');
```

---

## Integration Examples

### Express.js Backend
```javascript
const express = require('express');
const fetch = require('node-fetch');
const app = express();

app.post('/api/check-email', async (req, res) => {
    const { email } = req.body;
    
    try {
        const response = await fetch('http://localhost:5000/api/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, check_web_presence: true })
        });
        
        const result = await response.json();
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

### Django Backend
```python
import requests
from django.http import JsonResponse
from django.views import View

class VerifyEmailView(View):
    def post(self, request):
        email = request.POST.get('email')
        
        response = requests.post(
            'http://localhost:5000/api/verify',
            json={'email': email, 'check_web_presence': True}
        )
        
        if response.status_code == 200:
            return JsonResponse(response.json())
        else:
            return JsonResponse({'error': 'Verification failed'}, status=500)
```

### HTML Form with Fetch
```html
<!DOCTYPE html>
<html>
<body>
    <form id="emailForm">
        <input type="email" id="emailInput" placeholder="Enter email" required>
        <button type="submit">Verify</button>
    </form>
    <div id="result"></div>

    <script>
        document.getElementById('emailForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('emailInput').value;
            
            const response = await fetch('/api/verify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });
            
            const result = await response.json();
            document.getElementById('result').innerHTML = 
                `<p>Status: ${result.overall_status}</p>`;
        });
    </script>
</body>
</html>
```

---

## Configuration for Integration

### Disable Web Presence Check (Faster)
```python
# In config.py
CHECK_GRAVATAR = False
```

### Increase SMTP Timeout
```python
# In config.py
SMTP_TIMEOUT = 20  # seconds
```

### Add Custom Disposable Domains
```python
# In config.py
DISPOSABLE_DOMAINS = {
    # ... existing ...
    'yourdomain.com',  # Add yours
}
```

---

## Error Handling

### Python Module Errors
```python
from email_verifier import EmailVerifier

verifier = EmailVerifier()

try:
    result = verifier.verify("user@example.com")
except Exception as e:
    # Handle error
    print(f"Verification error: {str(e)}")
```

### Flask API Errors

**400 Bad Request** - Missing required parameters
```json
{ "error": "Email is required" }
```

**500 Internal Server Error** - Server error
```json
{ "error": "Verification failed" }
```

---

## Performance Considerations

### Single Verification Time
- Phase 1 (Syntax): ~100ms
- Phase 2 (DNS): 200-800ms
- Phase 3 (SMTP): 1-5s (varies by server)
- Phase 4 (Web): 1-3s (optional)
- **Total: 2-10 seconds**

### Optimization Tips

1. **Skip Phase 4** for faster results
   ```python
   result = verify_email(email, check_web_presence=False)
   ```

2. **Reduce SMTP timeout** for quicker failures
   ```python
   EmailVerifier.SMTP_TIMEOUT = 5
   ```

3. **Cache results** for known emails
   ```python
   verified_cache = {}
   if email not in verified_cache:
       verified_cache[email] = verify_email(email)
   ```

4. **Batch process** for multiple emails

---

## Rate Limiting

When deploying to production, implement rate limiting:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/verify', methods=['POST'])
@limiter.limit("10 per minute")
def api_verify():
    # ... verification logic ...
    pass
```

---

## Debugging

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now run verification
result = verify_email("user@example.com")
```

### Check Individual Phases
```python
result = verify_email("user@example.com")

# Debug each phase
for phase_num in range(1, 5):
    phase = result[f'phase_{phase_num}']
    print(f"Phase {phase_num}:")
    print(f"  Status: {phase['status']}")
    print(f"  Message: {phase['message']}")
    print()
```

---

## Frequently Asked Questions

### Q: How do I increase the timeout?
A: Edit `config.py` or set `EmailVerifier.SMTP_TIMEOUT = 20`

### Q: Can I use this with async/await?
A: Current version is synchronous. For async, wrap in thread pool executor.

### Q: How do I batch verify emails?
A: Loop through list and call verify_email() for each.

### Q: Is there rate limiting?
A: Implement externally with Flask-Limiter or similar.

### Q: Can I store results in a database?
A: Yes, save `result.to_dict()` to your database.

---

## Support

For issues or questions:
1. Review the code comments
2. Check example implementations
3. Test with known valid/invalid emails
4. Enable debug logging for troubleshooting

---

**Ready to integrate? 🚀**
