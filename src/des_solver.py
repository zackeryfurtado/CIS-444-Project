import base64
import binascii
import time
from Crypto.Cipher import DES
from scorer import score_text
from key_generator import generate_des_keys


def decode_ciphertext(ciphertext):
    ciphertext = ciphertext.strip()

    # Try hex first
    try:
        return bytes.fromhex(ciphertext)
    except ValueError:
        pass

    # Try base64
    try:
        return base64.b64decode(ciphertext)
    except binascii.Error:
        pass

    # Fallback: raw text bytes
    return ciphertext.encode("utf-8")


def clean_plaintext(raw_bytes):
    try:
        text = raw_bytes.decode("utf-8", errors="ignore")
    except Exception:
        text = ""

    return text.replace("\x00", "").strip()


def solve_des(ciphertext, dictionary):
    cipher_bytes = decode_ciphertext(ciphertext)

    best_key = None
    best_text = ""
    best_score = -1

    total_key_time = 0
    total_verify_time = 0
    total_keys = 0

    for year, key in generate_des_keys():
        total_keys += 1

        try:
            start_key_time = time.perf_counter()
            cipher = DES.new(key, DES.MODE_ECB)
            decrypted_bytes = cipher.decrypt(cipher_bytes)
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