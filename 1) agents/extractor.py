import re
from typing import Dict, Any

class LoanExtractionAgent:
    """
    Extracts numeric loan details from raw text using regex.
    For screenshots, integrate OCR in tools/ocr_reader.py and pass text here.
    """
    def extract(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()

        # Loan amount (first big number with optional ₹)
        amount_match = re.search(r"₹\s?([\d,]{3,})|(?:loan|amount)[^\d\r\n]*([\d,]{3,})", text_lower)
        loan_amount = None
        if amount_match:
            grp = amount_match.group(1) or amount_match.group(2)
            loan_amount = int(grp.replace(',', ''))

        # Interest rate: find patterns like '9%', '9 %', '9 percent', '9% per day'
        interest_match = re.search(r"(\d{1,2}(?:\.\d+)?)\s?%(\s?per\s?(day|month|year))?", text_lower)
        interest_rate = interest_match.group(1) + "%" if interest_match else None

        # Tenure (days / months)
        tenure_match = re.search(r"(\d{1,3})\s?(days|day|months|month|yrs|years)", text_lower)
        tenure = (int(tenure_match.group(1)), tenure_match.group(2)) if tenure_match else None

        # Processing fee
        pf_match = re.search(r"(processing fee|charges|fees)[^\d\r\n]*₹?\s?([\d,]{2,})", text_lower)
        processing_fee = int(pf_match.group(2).replace(',', '')) if pf_match else 0

        # EMI (if present)
        emi_match = re.search(r"emi[^\d\r\n]*₹?\s?([\d,]{2,})", text_lower)
        emi = int(emi_match.group(1).replace(',', '')) if emi_match else None

        # Permissions requested (contacts, gallery, sms)
        permissions = []
        for p in ["contacts", "gallery", "photos", "sms", "messages", "camera", "storage"]:
            if p in text_lower:
                permissions.append(p)

        return {
            "raw_text": text,
            "loan_amount": loan_amount,
            "interest_rate": interest_rate,
            "tenure": tenure,
            "processing_fee": processing_fee,
            "emi": emi,
            "permissions": permissions
        }

