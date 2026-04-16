# ============================================================
# HIT137 - Assignment 2 | S1 2026
# Question 1: Text Encryption
# File: encrypt.py
# Author: Jenish
# ============================================================


def encrypt_char(char, shift1, shift2):
    """
    Encrypts a single character.

    Lowercase:
      a-m: shift FORWARD  by shift1 * shift2
      n-z: shift BACKWARD by shift1 + shift2

    Uppercase:
      A-M: shift BACKWARD by shift1
      N-Z: shift FORWARD  by shift2 ** 2

    Other characters: unchanged
    """
    if char.islower():
        offset   = ord('a')
        position = ord(char) - offset

        if position <= 12:          # a-m
            new_position = (position + shift1 * shift2) % 26
        else:                       # n-z
            new_position = (position - (shift1 + shift2)) % 26

        return chr(new_position + offset)

    elif char.isupper():
        offset   = ord('A')
        position = ord(char) - offset

        if position <= 12:          # A-M
            new_position = (position - shift1) % 26
        else:                       # N-Z
            new_position = (position + shift2 ** 2) % 26

        return chr(new_position + offset)

    else:
        return char                 # spaces, numbers, symbols unchanged


def encrypt(text, shift1, shift2):
    """Encrypts full text string character by character."""
    return ''.join(encrypt_char(ch, shift1, shift2) for ch in text)


def encrypt_file(input_path, output_path, shift1, shift2):
    """
    Reads raw_text.txt, encrypts contents,
    writes result to encrypted_text.txt.
    """
    with open(input_path, 'r') as f:
        original_text = f.read()

    encrypted_text = encrypt(original_text, shift1, shift2)

    with open(output_path, 'w') as f:
        f.write(encrypted_text)

    print(f"Encryption complete. Written to: {output_path}")
