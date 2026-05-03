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

def solve_caesar(ciphertext, dictionary):
    best_score = -1
    best_text = ""
    best_key = 0

    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        score = score_text(decrypted, dictionary)

        if score > best_score:
            best_score = score
            best_text = decrypted
            best_key = shift

    return best_text, best_key