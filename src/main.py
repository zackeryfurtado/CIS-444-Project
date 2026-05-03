import csv
from scorer import load_dictionary
from caesar import solve_caesar
from des_solver import solve_des

INPUT_FILE = "data/input.csv"
OUTPUT_FILE = "data/output.csv"
DICTIONARY_FILE = "data/dictionary.txt"

def main():
    # Load the dictionary
    print("Loading dictionary...")
    dictionary = load_dictionary(DICTIONARY_FILE)

    results = []

    print("Reading input.csv...\n")

    with open(INPUT_FILE, "r") as f:
        reader = csv.reader(f)

        for row in reader:
            sender, receiver, algorithim, chipertext = row

            print(f"Processing: {sender} -> {receiver} ({algorithim})")

            if algorithim == "DES":
                result = solve_des(chipertext, dictionary)

                print(f" DES Key: {result['key']}")
                print(f" Message: {result['plaintext']}")
                print(f" Keys Tested: {result['keys_tested']}")

                # Add the result to the results list
                results.append([
                    sender,
                    receiver,
                    algorithim,
                    result['key'],
                    result['plaintext'],
                ])

            elif algorithim == "CS":
                plaintext, key = solve_caesar(chipertext, dictionary)

                print(f" Caesar Key: {key}")
                print(f" Message: {plaintext}")

                results.append([
                    sender,
                    receiver,
                    algorithim,
                    key,
                    plaintext,
                ])

            else:
                print(" Unkown algorithim, skipping...\n")

    print("Writing output.csv...")

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(results)

    print("Done!")

if __name__ == "__main__":
    main()