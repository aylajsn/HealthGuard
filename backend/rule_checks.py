def run_owasp_checks(spec: dict) -> list[dict]:
    """
    Checks a device/API spec against key OWASP IoT Top 10 (2018) issues.
    Reference: https://owasp.org/www-project-internet-of-things/
    """
    findings = []

    if spec.get("auth_type") in (None, "none", "hardcoded"):
        findings.append({
            "id": "I1",
            "name": "Weak, Guessable, or Hardcoded Passwords",
            "severity": "critical",
            "explanation": "No real authentication mechanism detected, or credentials are hardcoded."
        })

    if spec.get("uses_https") is False:
        findings.append({
            "id": "I2",
            "name": "Insecure Network Services",
            "severity": "high",
            "explanation": "Data is transmitted without HTTPS encryption, exposing it to interception."
        })

    if spec.get("rate_limiting") is False:
        findings.append({
            "id": "I3",
            "name": "Insecure Ecosystem Interfaces",
            "severity": "medium",
            "explanation": "No rate limiting means the API is vulnerable to brute-force or scraping abuse."
        })

    if spec.get("encryption_at_rest") is False:
        findings.append({
            "id": "I7",
            "name": "Insecure Data Transfer and Storage",
            "severity": "high",
            "explanation": "Sensitive data is stored without encryption at rest."
        })

    if spec.get("default_permissions") == "public":
        findings.append({
            "id": "I9",
            "name": "Insecure Default Settings",
            "severity": "high",
            "explanation": "The API defaults to public access instead of a secure default."
        })

    return findings

HIPAA_PHI_PATTERNS = {
    "name": ["name", "patient_name", "full_name"],
    "date": ["dob", "date_of_birth", "admission_date"],
    "geographic": ["address", "zip", "city", "gps", "location"],
    "phone": ["phone", "mobile"],
    "email": ["email"],
    "ssn": ["ssn", "social_security"],
    "medical_record_number": ["mrn", "patient_id", "medical_record"],
    "biometric": ["heart_rate", "glucose", "fingerprint", "biometric"],
    "device_id": ["device_id", "serial_number"],
}


def find_phi_fields(sample_data: dict) -> list[dict]:
    """
    Scans field NAMES in a sample API response for likely PHI,
    based on HIPAA's Safe Harbor identifier categories.
    """
    findings = []
    for field_name in sample_data.keys():
        field_lower = field_name.lower()
        for category, patterns in HIPAA_PHI_PATTERNS.items():
            if any(pattern in field_lower for pattern in patterns):
                findings.append({
                    "field": field_name,
                    "category": category,
                    "recommendation": f"'{field_name}' looks like it contains PHI ({category}). Verify it's encrypted and access-controlled."
                })
    return findings