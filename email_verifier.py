"""
Lightweight Email Verification Tool - Core Logic
Uses RFC 5322 regex, DNS MX records, SMTP handshake, and web presence checks.
"""

import re
import socket
import smtplib
import dns.resolver
import requests
from typing import Dict, Tuple, Optional
from urllib.parse import quote
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RFC 5322 compliant regex pattern (simplified but robust)
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
)

# Common disposable email providers
DISPOSABLE_DOMAINS = {
    'tempmail.com', '10minutemail.com', 'guerrillamail.com', 'mailinator.com',
    'temp-mail.org', 'throwaway.email', 'yopmail.com', 'maildrop.cc'
}


class EmailVerificationResult:
    """Stores comprehensive email verification results."""
    
    def __init__(self, email: str):
        self.email = email
        self.phase_1 = {"status": "pending", "valid": False, "message": ""}
        self.phase_2 = {"status": "pending", "valid": False, "message": "", "mx_records": []}
        self.phase_3 = {"status": "pending", "valid": False, "message": "", "server": ""}
        self.phase_4 = {"status": "pending", "valid": False, "message": ""}
        self.overall_status = "pending"
        
    def to_dict(self) -> Dict:
        """Convert results to dictionary for API/display."""
        return {
            "email": self.email,
            "phase_1": self.phase_1,
            "phase_2": self.phase_2,
            "phase_3": self.phase_3,
            "phase_4": self.phase_4,
            "overall_status": self.overall_status
        }


class EmailVerifier:
    """Main email verification orchestrator."""
    
    SMTP_TIMEOUT = 10  # seconds
    
    def __init__(self):
        self.result = None
        
    def verify(self, email: str, check_web_presence: bool = True) -> EmailVerificationResult:
        """
        Execute all verification phases.
        
        Args:
            email: Email address to verify
            check_web_presence: Whether to perform Phase 4 web presence check
            
        Returns:
            EmailVerificationResult object with detailed status
        """
        self.result = EmailVerificationResult(email)
        
        try:
            # Phase 1: Syntax Validation
            if not self._phase_1_syntax_validation():
                self.result.overall_status = "invalid"
                return self.result
                
            # Phase 2: Domain/MX Record Check
            if not self._phase_2_mx_check():
                self.result.overall_status = "invalid"
                return self.result
                
            # Phase 3: SMTP Handshake
            self._phase_3_smtp_handshake()
            
            # Phase 4: Web Presence Search (optional)
            if check_web_presence:
                self._phase_4_web_presence()
                
        except Exception as e:
            logger.error(f"Verification error: {str(e)}")
            self.result.overall_status = "error"
            
        # Determine overall status
        self._determine_overall_status()
        return self.result
        
    def _phase_1_syntax_validation(self) -> bool:
        """Phase 1: Validate email syntax against RFC 5322."""
        try:
            email = self.result.email.strip().lower()
            
            if not email:
                self.result.phase_1["message"] = "Email is empty"
                self.result.phase_1["status"] = "failed"
                return False
                
            if len(email) > 254:
                self.result.phase_1["message"] = "Email exceeds 254 characters"
                self.result.phase_1["status"] = "failed"
                return False
                
            if not EMAIL_REGEX.match(email):
                self.result.phase_1["message"] = "Email format does not match RFC 5322 standards"
                self.result.phase_1["status"] = "failed"
                return False
                
            local_part, domain = email.rsplit('@', 1)
            
            if len(local_part) > 64:
                self.result.phase_1["message"] = "Local part exceeds 64 characters"
                self.result.phase_1["status"] = "failed"
                return False
                
            self.result.phase_1["valid"] = True
            self.result.phase_1["message"] = "Email syntax is valid"
            self.result.phase_1["status"] = "passed"
            return True
            
        except Exception as e:
            self.result.phase_1["message"] = f"Syntax validation error: {str(e)}"
            self.result.phase_1["status"] = "error"
            return False
    
    def _phase_2_mx_check(self) -> bool:
        """Phase 2: Check domain's MX records."""
        try:
            email = self.result.email.strip().lower()
            domain = email.rsplit('@', 1)[1]
            
            # Check for disposable email
            if domain in DISPOSABLE_DOMAINS:
                self.result.phase_2["message"] = f"Domain '{domain}' is a known disposable email provider"
                self.result.phase_2["status"] = "failed"
                return False
            
            # Query MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                mx_hosts = []
                
                for mx in sorted(mx_records, key=lambda x: x.preference):
                    mx_host = str(mx.exchange).rstrip('.')
                    mx_hosts.append({"host": mx_host, "priority": mx.preference})
                
                if not mx_hosts:
                    self.result.phase_2["message"] = f"No MX records found for domain '{domain}'"
                    self.result.phase_2["status"] = "failed"
                    return False
                    
                self.result.phase_2["mx_records"] = mx_hosts
                self.result.phase_2["valid"] = True
                self.result.phase_2["message"] = f"Found {len(mx_hosts)} MX record(s)"
                self.result.phase_2["status"] = "passed"
                return True
                
            except dns.resolver.NXDOMAIN:
                self.result.phase_2["message"] = f"Domain '{domain}' does not exist"
                self.result.phase_2["status"] = "failed"
                return False
            except dns.resolver.NoAnswer:
                self.result.phase_2["message"] = f"No MX records for domain '{domain}'"
                self.result.phase_2["status"] = "failed"
                return False
                
        except Exception as e:
            self.result.phase_2["message"] = f"MX check error: {str(e)}"
            self.result.phase_2["status"] = "error"
            return False
    
    def _phase_3_smtp_handshake(self) -> bool:
        """Phase 3: Perform SMTP handshake on port 25."""
        try:
            email = self.result.email.strip().lower()
            domain = email.rsplit('@', 1)[1]
            
            if not self.result.phase_2["mx_records"]:
                self.result.phase_3["message"] = "No MX records available for SMTP check"
                self.result.phase_3["status"] = "skipped"
                return False
            
            # Try each MX record in priority order
            mx_hosts = self.result.phase_2["mx_records"]
            last_error = None
            
            for mx_record in mx_hosts:
                smtp_host = mx_record["host"]
                
                try:
                    # Create SMTP connection with timeout
                    smtp = smtplib.SMTP(timeout=self.SMTP_TIMEOUT)
                    smtp.connect(smtp_host, 25)
                    
                    try:
                        # HELO
                        smtp.helo(smtp.local_hostname)
                        
                        # MAIL FROM
                        smtp.mail("test@example.com")
                        
                        # RCPT TO - this is the crucial check
                        code, message = smtp.rcpt(email)
                        
                        if code == 250:
                            self.result.phase_3["valid"] = True
                            self.result.phase_3["message"] = f"✓ Inbox exists (server accepted recipient)"
                            self.result.phase_3["status"] = "passed"
                            self.result.phase_3["server"] = smtp_host
                            
                        elif code in (450, 451):
                            # Greylisting detected
                            self.result.phase_3["valid"] = False
                            self.result.phase_3["message"] = f"Greylisted (code {code}) - try again later"
                            self.result.phase_3["status"] = "greylisted"
                            self.result.phase_3["server"] = smtp_host
                            
                        elif code in (550, 551, 552, 553):
                            # Permanent rejection
                            self.result.phase_3["valid"] = False
                            self.result.phase_3["message"] = f"Server rejected recipient (code {code})"
                            self.result.phase_3["status"] = "failed"
                            self.result.phase_3["server"] = smtp_host
                            
                        else:
                            self.result.phase_3["valid"] = False
                            self.result.phase_3["message"] = f"Unexpected server response (code {code})"
                            self.result.phase_3["status"] = "unknown"
                            self.result.phase_3["server"] = smtp_host
                        
                        # IMPORTANT: Send QUIT to close connection properly
                        smtp.quit()
                        return True
                        
                    except smtplib.SMTPException as e:
                        last_error = str(e)
                        smtp.close()
                        
                except (socket.timeout, socket.error, smtplib.SMTPException) as e:
                    last_error = str(e)
                    logger.warning(f"Failed to connect to {smtp_host}: {str(e)}")
                    continue
            
            # If we get here, all MX servers failed
            if last_error:
                self.result.phase_3["message"] = f"Could not connect to any MX server: {last_error}"
            else:
                self.result.phase_3["message"] = "Could not connect to any MX server"
            self.result.phase_3["status"] = "failed"
            return False
            
        except Exception as e:
            self.result.phase_3["message"] = f"SMTP check error: {str(e)}"
            self.result.phase_3["status"] = "error"
            return False
    
    def _phase_4_web_presence(self) -> bool:
        """Phase 4: Check web presence (Gravatar, public records)."""
        try:
            email = self.result.email.strip().lower()
            import hashlib
            
            # Check Gravatar
            gravatar_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
            gravatar_url = f"https://www.gravatar.com/{gravatar_hash}.json"
            
            try:
                response = requests.get(gravatar_url, timeout=5)
                if response.status_code == 200:
                    self.result.phase_4["valid"] = True
                    self.result.phase_4["message"] = "✓ Email has Gravatar profile"
                    self.result.phase_4["status"] = "found"
                    return True
            except requests.RequestException:
                pass
            
            # Optional: Check Hunter.io free tier (no API key needed for basic info)
            # For now, we mark as "not found" if Gravatar check failed
            self.result.phase_4["valid"] = False
            self.result.phase_4["message"] = "No public profile found (Gravatar/public records)"
            self.result.phase_4["status"] = "not_found"
            return False
            
        except Exception as e:
            self.result.phase_4["message"] = f"Web presence check error: {str(e)}"
            self.result.phase_4["status"] = "error"
            return False
    
    def _determine_overall_status(self):
        """Determine overall verification status based on phase results."""
        # If Phase 1 or 2 failed, it's invalid
        if self.result.phase_1["status"] == "failed" or self.result.phase_2["status"] == "failed":
            self.result.overall_status = "invalid"
        
        # If Phase 3 passed, it's valid
        elif self.result.phase_3["status"] == "passed":
            self.result.overall_status = "valid"
        
        # If Phase 3 is greylisted, mark as undetermined
        elif self.result.phase_3["status"] == "greylisted":
            self.result.overall_status = "undetermined"
        
        # If Phase 3 failed or skipped, check Phase 2
        elif self.result.phase_2["status"] == "passed":
            self.result.overall_status = "undetermined"  # Domain exists but SMTP check failed
        
        else:
            self.result.overall_status = "unknown"


def verify_email(email: str, check_web_presence: bool = True) -> Dict:
    """
    Simple function to verify an email address.
    
    Args:
        email: Email address to verify
        check_web_presence: Whether to check web presence (Phase 4)
        
    Returns:
        Dictionary with verification results
    """
    verifier = EmailVerifier()
    result = verifier.verify(email, check_web_presence)
    return result.to_dict()


if __name__ == "__main__":
    # Example usage
    test_emails = [
        "user@gmail.com",
        "invalid.email",
        "test@example.com",
    ]
    
    for email in test_emails:
        print(f"\nVerifying: {email}")
        result = verify_email(email)
        print(f"Overall Status: {result['overall_status']}")
