hex_chars = '0123456789ABCDEF'

def year_to_hex(year):
    return format(year, "X")


def build_key_from_pattern(hex_year, key_length_bytes, extra_char):
    hex_key = (hex_year * ((key_length_bytes * 2 // len(hex_year)) + 1))[:key_length_bytes * 2 - 1]
    hex_key += extra_char
    return bytes.fromhex(hex_key)


def generate_des_keys(start_year=1935, end_year=1950):
    keys = []

    for year in range(start_year, end_year + 1):
        hex_year = year_to_hex(year)

        for extra_char in hex_chars:
            key = build_key_from_pattern(hex_year, 8, extra_char)
            keys.append((year, key))

    return keys


def generate_3des_keys(start_year=1935, end_year=1950):
    keys = []

    for year in range(start_year, end_year + 1):
        hex_year = year_to_hex(year)

        for extra_char in hex_chars:
            key = build_key_from_pattern(hex_year, 24, extra_char)
            keys.append((year, key))

    return keys