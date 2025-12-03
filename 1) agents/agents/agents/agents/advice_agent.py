# agents/advice_agent.py
from typing import Tuple, List

class AdviceAgent:
    """
    Generates human-readable advice based on risk score and flags.
    """
    def generate_advice(self, score: int, legality_flags: List[str], predator_flags: List[str]) -> dict:
        category = "SAFE"
        if score <= 30:
            category = "SAFE"
        elif 31 <= score <= 60:
            category = "RISKY"
        elif 61 <= score <= 80:
            category = "HIGH RISK"
        else:
            category = "DANGEROUS / SCAM"

        advice_lines = []
        if legality_flags:
            advice_lines += legality_flags
        if predator_flags:
            advice_lines += predator_flags

        # general action recommendations
        actions = []
        if category in ["DANGEROUS / SCAM", "HIGH RISK"]:
            actions.append("Do NOT accept this loan.")
            actions.append("Avoid sharing sensitive permissions (contacts, SMS, photos).")
            actions.append("Prefer RBI-registered lenders or verified banks.")
            actions.append("Report suspicious apps to cyber cell / consumer forum.")
        elif category == "RISKY":
            actions.append("Terms look suspicious — negotiate or request full T&C in writing.")
            actions.append("Check total repayment and interest in writing.")
        else:
            actions.append("Looks generally safe, but confirm lender credentials before proceeding.")

        return {
            "category": category,
            "score": score,
            "reasons": advice_lines,
            "actions": actions
        }
