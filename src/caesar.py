import time
from scorer import score_text

def caesar_decrypt(ciphertext, shift):
    result = ""

    for char in ciphertext:
        if char.isalpha():
            shifted = chr((ord(char.upper()) - 65 - shift) % 26 + 65)
            result += shifted
        else:
            result += char

    return result

def solve_caesar_with_stats(ciphertext, dictionary):
    best_score = -1
    best_text = ""
    best_key = 0

    total_key_time = 0
    total_verify_time = 0
    total_keys = 0

    for shift in range(26):
        total_keys += 1

        start_key_time = time.perf_counter()
        decrypted = caesar_decrypt(ciphertext, shift)
        end_key_time = time.perf_counter()

        start_verify_time = time.perf_counter()
        score = score_text(decrypted, dictionary)
        end_verify_time = time.perf_counter()

        total_key_time += end_key_time - start_key_time
        total_verify_time += end_verify_time - start_verify_time

        if score > best_score:
            best_score = score
            best_text = decrypted
            best_key = shift

    avg_key_time = total_key_time / total_keys if total_keys else 0
    avg_verify_time = total_verify_time / total_keys if total_keys else 0

    return {
        "key": best_key,
        "plaintext": best_text,
        "score": best_score,
        "keys_tested": total_keys,
        "avg_key_time": avg_key_time,
        "avg_verify_time": avg_verify_time,
    }

def solve_caesar(ciphertext, dictionary):
    result = solve_caesar_with_stats(ciphertext, dictionary)
    best_text = result["plaintext"]
    best_key = result["key"]

    return best_text, best_key
