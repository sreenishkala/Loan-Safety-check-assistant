# agents/risk_scorer.py
from typing import Dict, List
from tools.interest_calculator import calculate_effective_rate

class RiskScoringAgent:
    """
    Aggregates findings and computes a risk score 0-100.
    Uses simple heuristics; can be replaced/enhanced by an ML model.
    """
    def calculate_score(self, legality_flags: List[str], predator_flags: List[str], loan_data: Dict) -> int:
        score = 0

        # Each legality flag is serious
        score += len(legality_flags) * 20

        # Predator flags are also serious but slightly less each
        score += len(predator_flags) * 10

        # High interest numeric check if possible
        ir = loan_data.get("interest_rate")
        if ir:
            try:
                ir_val = float(ir.replace("%", ""))
                if ir_val > 40:
                    score += 20
                elif ir_val > 25:
                    score += 10
            except:
                pass

        # Processing fee relative to loan amount
        pf = loan_data.get("processing_fee") or 0
        amount = loan_data.get("loan_amount") or 0
        if amount > 0:
            pf_ratio = pf / amount
            if pf_ratio >= 0.2:
                score += 15
            elif pf_ratio >= 0.1:
                score += 7

        # If EMI and tenure present, compute a simple burden measure
        emi = loan_data.get("emi")
        income = loan_data.get("income", None)  # optional
        tenure = loan_data.get("tenure")
        if emi and income:
            try:
                emi_to_income = emi / income
                if emi_to_income > 0.5:
                    score += 20
                elif emi_to_income > 0.3:
                    score += 10
            except:
                pass
        else:
            # attempt to compute effective daily rate if repayment numbers present in raw text
            # (placeholder) - calculate_effective_rate can be used when repayment & principal known
            pass

        return min(100, int(score))
