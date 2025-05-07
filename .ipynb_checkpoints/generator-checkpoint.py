import math
from tabulate import tabulate

def compute_letter_size_logmar(distance_m=3.0, ppi=96):
    results = []
    for diopter in [round(d * 0.5, 1) for d in range(-14, 1)]:
        logmar = -diopter / 10
        height_mm = 0.291 * distance_m * (10 ** logmar)
        pixels = height_mm * (ppi / 25.4)
        
        # Approximate Snellen from logMAR
        snellen_denominator = round(6 * (10 ** logmar))
        snellen = f"6/{snellen_denominator}" if snellen_denominator <= 120 else "Worse than 6/120"
        
        results.append([diopter, round(logmar, 2), snellen, round(height_mm, 2), round(pixels, 2)])
    
    headers = ["Diopter (D)", "logMAR", "Snellen", "Height (mm)", "Pixels"]
    print(tabulate(results, headers=headers, tablefmt="github"))

if __name__ == "__main__":
    compute_letter_size_logmar()
