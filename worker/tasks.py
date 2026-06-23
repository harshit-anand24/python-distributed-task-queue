import time
import math

def compute_factorial(n):
    """Simulates a heavy CPU-bound mathematical operation."""
    print(f"[Computation] Executing factorial calculation for n={n}...")
    # Add a slight delay to mimic processing times
    time.sleep(1.5)
    result = math.factorial(n)
    return str(result)[:30] + "..." if len(str(result)) > 30 else str(result)

def transform_data_payload(data_string):
    """Simulates a memory/string heavy structural data manipulation."""
    print(f"[Computation] Cleaning and mutating raw string payload...")
    time.sleep(1.0)
    return data_string.strip().upper()[::-1]

# Expose a clean lookup map so our worker daemon can map text strings to functional pointers
TASK_REGISTRY = {
    "compute_factorial": compute_factorial,
    "transform_data_payload": transform_data_payload
}