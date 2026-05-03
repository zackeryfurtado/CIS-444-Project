import csv
from pathlib import Path

from caesar import solve_caesar_with_stats
from des_solver import solve_des
from scorer import load_dictionary
from triple_des_solver import solve_3des


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "input.csv"
OUTPUT_FILE = BASE_DIR / "data" / "output.csv"
DICTIONARY_FILE = BASE_DIR / "data" / "dictionary.txt"


def format_key(key):
    if key is None:
        return ""
    if isinstance(key, bytes):
        return key.hex().upper()
    return str(key)


def print_timing_summary(timing_results):
    print("\nTiming Summary (seconds per key)")

    if not timing_results:
        print("No valid rows were processed.")
        return

    print(
        f"{'Algorithm':<10}"
        f"{'Keys Tested':>14}"
        f"{'Avg Decrypt/Key':>20}"
        f"{'Avg Verification/Key':>24}"
        f"{'Best Score':>14}"
    )

    for result in timing_results:
        print(
            f"{result['algorithm']:<10}"
            f"{result['keys_tested']:>14}"
            f"{result['avg_key_time']:>20.8f}"
            f"{result['avg_verify_time']:>24.8f}"
            f"{result['score']:>14.4f}"
        )


def main():
    missing_files = False

    if not INPUT_FILE.exists():
        print(f"Error: missing input file: {INPUT_FILE}")
        missing_files = True

    if not DICTIONARY_FILE.exists():
        print(f"Error: missing dictionary file: {DICTIONARY_FILE}")
        missing_files = True

    if missing_files:
        return

    print("Loading dictionary...")
    dictionary = load_dictionary(DICTIONARY_FILE)

    results = []
    timing_results = []

    print("Reading input.csv...\n")

    with open(INPUT_FILE, "r", newline="") as f:
        reader = csv.reader(f)

        for row_number, row in enumerate(reader, start=1):
            if not row or all(not value.strip() for value in row):
                continue

            if len(row) != 4:
                print(f"Malformed CSV row {row_number}: expected 4 columns, got {len(row)}. Skipping.")
                continue

            sender, receiver, algorithm, ciphertext = row
            algorithm = algorithm.strip().upper()
            ciphertext = ciphertext.strip()

            print(f"Processing row {row_number}: {sender} -> {receiver} ({algorithm})")

            if algorithm == "CS":
                result = solve_caesar_with_stats(ciphertext, dictionary)
            elif algorithm == "DES":
                result = solve_des(ciphertext, dictionary)
            elif algorithm == "3DES":
                result = solve_3des(ciphertext, dictionary)
            else:
                print(f"Unknown algorithm '{algorithm}' on row {row_number}. Skipping.\n")
                continue

            key = format_key(result["key"])

            print(f" Key: {key}")
            print(f" Message: {result['plaintext']}")
            print(f" Keys Tested: {result['keys_tested']}\n")

            results.append([
                sender,
                receiver,
                algorithm,
                key,
                result["plaintext"],
            ])

            timing_results.append({
                "algorithm": algorithm,
                "keys_tested": result["keys_tested"],
                "avg_key_time": result["avg_key_time"],
                "avg_verify_time": result["avg_verify_time"],
                "score": result["score"],
            })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print("Writing output.csv...")

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(results)

    print_timing_summary(timing_results)
    print("\nDone!")


if __name__ == "__main__":
    main()
