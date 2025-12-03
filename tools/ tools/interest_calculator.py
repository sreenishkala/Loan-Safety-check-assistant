# tools/interest_calculator.py
def calculate_effective_rate(principal: float, repayment: float, days: int):
    """
    Returns daily interest percentage. Example use when repayment schedule is known.
    """
    try:
        diff = float(repayment) - float(principal)
        daily_rate = (diff / float(principal)) / float(days) * 100
        return round(daily_rate, 3)
    except:
        return None
