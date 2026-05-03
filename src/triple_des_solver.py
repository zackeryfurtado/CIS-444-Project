import time
from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad
from scorer import score_text
from key_generator import generate_3des_keys
from des_solver import decode_ciphertext, clean_plaintext


def solve_3des(ciphertext, dictionary):
    cipher_bytes = decode_ciphertext(ciphertext)

    best_key = None
    best_text = ""
    best_score = -1

    total_key_time = 0
    total_verify_time = 0
    total_keys = 0

    for year, key in generate_3des_keys():
        total_keys += 1

        try:
            key_bytes = DES3.adjust_key_parity(key)

            start_key_time = time.perf_counter()
            cipher = DES3.new(key_bytes, DES3.MODE_ECB)
            decrypted_bytes = cipher.decrypt(cipher_bytes)

            try:
                decrypted_bytes = unpad(decrypted_bytes, DES3.block_size)
            except ValueError:
                pass

            plaintext = clean_plaintext(decrypted_bytes)
            end_key_time = time.perf_counter()

            start_verify_time = time.perf_counter()
            score = score_text(plaintext, dictionary)
            end_verify_time = time.perf_counter()

            total_key_time += end_key_time - start_key_time
            total_verify_time += end_verify_time - start_verify_time

            if score > best_score:
                best_score = score
                best_key = key
                best_text = plaintext

        except Exception:
            continue

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
