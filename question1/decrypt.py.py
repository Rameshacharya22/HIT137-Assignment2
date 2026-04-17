# ============================================================
# HIT137 - Assignment 2 | S1 2026
# Question 1: Text Decryption + Verification
# File: decrypt.py
# Author: Ramesh
# ============================================================


def decrypt_char(char, shift1, shift2):
    """
    Decrypts a single character — exact reverse of encrypt_char().

    Lowercase:
      a-m: reverse forward shift  → shift BACKWARD by shift1 * shift2
      n-z: reverse backward shift → shift FORWARD  by shift1 + shift2

    Uppercase:
      A-M: reverse backward shift → shift FORWARD  by shift1
      N-Z: reverse forward shift  → shift BACKWARD by shift2 ** 2

    Other characters: unchanged
    """
    if char.islower():
        offset   = ord('a')
        position = ord(char) - offset

        if position <= 12:          # a-m
            new_position = (position - shift1 * shift2) % 26
        else:                       # n-z
            new_position = (position + (shift1 + shift2)) % 26

        return chr(new_position + offset)

    elif char.isupper():
        offset   = ord('A')
        position = ord(char) - offset

        if position <= 12:          # A-M
            new_position = (position + shift1) % 26
        else:                       # N-Z
            new_position = (position - shift2 ** 2) % 26

        return chr(new_position + offset)

    else:
        return char                 # unchanged


def decrypt(text, shift1, shift2):
    """Decrypts full encrypted string character by character."""
    return ''.join(decrypt_char(ch, shift1, shift2) for ch in text)


def decrypt_file(input_path, output_path, shift1, shift2):
    """
    Reads encrypted_text.txt, decrypts contents,
    writes result to decrypted_text.txt.
    """
    with open(input_path, 'r') as f:
        encrypted_text = f.read()

    decrypted_text = decrypt(encrypted_text, shift1, shift2)

    with open(output_path, 'w') as f:
        f.write(decrypted_text)

    print(f"Decryption complete. Written to: {output_path}")


def verify(original_path, decrypted_path):
    """
    Compares raw_text.txt with decrypted_text.txt.
    Prints SUCCESS if they match, FAIL with first difference if not.
    """
    with open(original_path, 'r') as f:
        original = f.read()

    with open(decrypted_path, 'r') as f:
        decrypted = f.read()

    if original == decrypted:
        print("Verification: SUCCESS — decrypted text matches the original!")
    else:
        print("Verification: FAIL — texts do not match.")
        for i, (a, b) in enumerate(zip(original, decrypted)):
            if a != b:
                print(f"  First difference at position {i}: "
                      f"original='{a}' decrypted='{b}'")
                break