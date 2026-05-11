"""
Test script for Email Verification Tool
Tests various email addresses and displays results
"""

from email_verifier import verify_email
import json

def print_separator(title=""):
    """Print a formatted separator."""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'-'*60}\n")

def test_email(email: str, show_web_presence: bool = True):
    """Test a single email and display formatted results."""
    print(f"Testing: {email}")
    print("-" * 40)
    
    try:
        result = verify_email(email, check_web_presence=show_web_presence)
        
        # Overall Status
        status_emoji = {
            'valid': '✅',
            'invalid': '❌',
            'undetermined': '⚠️',
            'unknown': '❓',
            'error': '⚠️'
        }
        
        print(f"\n{status_emoji.get(result['overall_status'], '❓')} Overall Status: {result['overall_status'].upper()}")
        
        # Phase 1
        p1 = result['phase_1']
        emoji = "✅" if p1['status'] == 'passed' else "❌" if p1['status'] == 'failed' else "⏳"
        print(f"\n{emoji} Phase 1 (Syntax Validation): {p1['status'].upper()}")
        print(f"   {p1['message']}")
        
        # Phase 2
        p2 = result['phase_2']
        emoji = "✅" if p2['status'] == 'passed' else "❌" if p2['status'] == 'failed' else "⏳"
        print(f"\n{emoji} Phase 2 (Domain/MX Check): {p2['status'].upper()}")
        print(f"   {p2['message']}")
        if p2['mx_records']:
            print(f"   MX Records:")
            for mx in p2['mx_records']:
                print(f"      - {mx['host']} (Priority: {mx['priority']})")
        
        # Phase 3
        p3 = result['phase_3']
        if p3['status'] == 'passed':
            emoji = "✅"
        elif p3['status'] == 'greylisted':
            emoji = "⚠️"
        elif p3['status'] == 'failed':
            emoji = "❌"
        else:
            emoji = "⏳"
        print(f"\n{emoji} Phase 3 (SMTP Handshake): {p3['status'].upper()}")
        print(f"   {p3['message']}")
        if p3['server']:
            print(f"   Server: {p3['server']}")
        
        # Phase 4 (if checked)
        if show_web_presence:
            p4 = result['phase_4']
            emoji = "✅" if p4['status'] == 'found' else "❌" if p4['status'] == 'not_found' else "⏳"
            print(f"\n{emoji} Phase 4 (Web Presence): {p4['status'].upper()}")
            print(f"   {p4['message']}")
        
        print("\n")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")

def main():
    """Run test suite."""
    print_separator("EMAIL VERIFICATION TOOL - TEST SUITE")
    
    # Test cases
    test_cases = [
        # Valid emails (you should replace with real emails)
        ("user@gmail.com", True),
        ("support@github.com", True),
        
        # Invalid formats
        ("invalid-email", False),
        ("@example.com", False),
        ("user@", False),
        
        # Disposable emails
        ("test@tempmail.com", False),
        ("user@mailinator.com", False),
        
        # Non-existent domain
        ("user@thisdoesnotexistexample12345.com", False),
    ]
    
    print("\n📧 RUNNING EMAIL VERIFICATION TESTS\n")
    print(f"Total test cases: {len(test_cases)}\n")
    
    passed = 0
    failed = 0
    
    for email, show_web in test_cases:
        try:
            test_email(email, show_web)
            passed += 1
        except Exception as e:
            print(f"❌ Test failed for {email}: {str(e)}\n")
            failed += 1
    
    # Summary
    print_separator("TEST SUMMARY")
    print(f"Total Tests: {len(test_cases)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"\nCompletion Rate: {(passed/len(test_cases)*100):.1f}%\n")
    
    # Notes
    print("📝 NOTES:\n")
    print("1. Replace gmail.com and github.com test emails with real email addresses")
    print("2. Some servers may timeout or reject connections - this is normal")
    print("3. Greylisting may occur on first verification attempts")
    print("4. Disposable email providers are automatically rejected in Phase 2")
    print("5. Web presence check (Phase 4) requires internet connection")

if __name__ == "__main__":
    main()
