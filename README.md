# CIS 444 Crypto Project

This project decrypts intercepted messages encrypted with Caesar Cipher, DES, and 3DES. It brute-forces the possible keys, scores each decrypted result against an English dictionary, and writes the best plaintext result for each input row.

## Requirements

- Python 3
- pycryptodome

Install dependencies from the repo root:

```bash
pip install -r requirements.txt
```

## Run

Run the program from the repo root:

```bash
python src/main.py
```

The program reads:

```text
data/input.csv
data/dictionary.txt
```

and writes:

```text
data/output.csv
```

## Input Format

`data/input.csv` should not include a header. Each row must have exactly four columns:

```text
sender, receiver, algorithm, ciphertext
```

Supported algorithm values are:

```text
CS
DES
3DES
```

Example:

```csv
A,B,CS,KHOOR
A,B,DES,533EEFDCFECB565BBC150E6BF4C526CA
A,B,3DES,0E4CF5D7F29ADA2EC345E61760CE5586FDB95D0F7CAA92C35B4ABD0921B196018CD71D58F2999465
```

## Output Format

`data/output.csv` is written without a header. Each row uses this exact column order:

```text
sender, receiver, algorithm, key, plaintext
```

Example:

```csv
A,B,CS,3,HELLO
```

After processing all rows, the program also prints a timing summary with the algorithm, keys tested, average decryption time per key, average intelligibility verification time per key, and best score.

## Error Handling

The program reports and stops if `data/input.csv` or `data/dictionary.txt` is missing. Malformed CSV rows and unknown algorithms are reported and skipped.
