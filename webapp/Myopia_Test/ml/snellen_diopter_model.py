def line_to_logmar(line_number: int) -> float:
    return (10 - line_number) * 0.1

def predict_diopters(line_number: int) -> float:
    """
    Estimate diopters based on the line number using a rounded logMAR-based formula.
    """
    logmar = line_to_logmar(line_number)
    raw_diopters = -3.3 * logmar

    # Round to nearest 0.5 D
    rounded_diopters = round(raw_diopters * 2) / 2.0
    return rounded_diopters
