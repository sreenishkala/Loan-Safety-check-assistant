# agents/legality_checker.py
from typing import List, Dict, Any
from tools.scam_database import scam_apps

class LegalityCheckerAgent:
    """
    Basic legality / compliance checks.
    Extend by adding RBI / NBFC dataset and real web lookups.
    """
    def check_legality(self, loan_data: Dict[str, Any], raw_text: str) -> List[str]:
        findings = []
        text = raw_text.lower()

        # Check against known scam app names
        for scam in scam_apps:
            if scam.lower() in text:
                findings.append(f"⚠ App/Service name matches known scam pattern: {scam}")

        # Check if daily interest is present and flag it (often predatory)
        if "per day" in (loan_data.get("interest_rate") or "").lower() or "per day" in text:
            findings.append("❌ Interest mentioned as 'per day' — suspicious/likely predatory")

        # Check numeric interest level if present
        ir = loan_data.get("interest_rate")
        if ir:
            try:
                ir_val = float(ir.replace("%", ""))
                # heuristic: > 30% monthly or none — but here we just flag high values
                if ir_val > 40:
                    findings.append(f"❌ Very high interest rate detected: {ir}")
                elif ir_val > 25:
                    findings.append(f"⚠ High interest rate detected: {ir}")
            except:
                pass

        # Check for suspicious permission requests
        if loan_data.get("permissions"):
            findings.append(f"⚠ App requests permissions: {', '.join(set(loan_data['permissions']))}")

        # Placeholder: check in RBI-approved lenders DB (not included). Add when available.
        # e.g., if not in_nbfc_list(lender) then findings.append(...)

        return findings
