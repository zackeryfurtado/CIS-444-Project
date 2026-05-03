import re

def load_dictionary(filepath):
    with open(filepath, "r") as f:
        words = set(word.strip().lower() for word in f)
    return words


def score_text(text, dictionary):
    words = text.lower().split()
    if len(words) == 0:
        return 0
    
    cleaned = [re.sub(r'[^a-z]' , "", word) for word in words]
    cleaned = [word for word in cleaned if word]

    if len(cleaned) == 0:
        return 0

    valid_words = sum(1 for word in cleaned if word in dictionary)
    return valid_words / len(cleaned)
