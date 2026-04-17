# ============================================================
# HIT137 - Assignment 2 | Question 1
# File: encryption.py
# Description: Encrypt, Decrypt and Verify a text file
#              using a custom two-shift cipher.
#
# Encryption Rules (from assignment):
#   Lowercase a-m : shift FORWARD  by shift1 * shift2
#   Lowercase n-z : shift BACKWARD by shift1 + shift2
#   Uppercase A-M : shift BACKWARD by shift1
#   Uppercase N-Z : shift FORWARD  by shift2 squared
#   Others        : unchanged (spaces, numbers, symbols)
# ============================================================


def encrypt_char(ch, shift1, shift2):
    """
    Encrypt a single character using the assignment rules.
    Uses % 13 per half so first-half letters always encrypt
    to first-half results (0-12) and second-half letters always
    encrypt to second-half results (13-25). This guarantees
    decryption works correctly for ANY shift values.
    """
    if ch.islower():
        idx = ord(ch) - ord('a')          # convert letter to 0-25 number
        if idx <= 12:
            # a-m: shift FORWARD by shift1 * shift2, stay in 0-12
            new_idx = (idx + shift1 * shift2) % 13
        else:
            # n-z: shift BACKWARD by shift1 + shift2, stay in 13-25
            new_idx = 13 + (idx - 13 - (shift1 + shift2)) % 13
        return chr(new_idx + ord('a'))

    elif ch.isupper():
        idx = ord(ch) - ord('A')          # convert letter to 0-25 number
        if idx <= 12:
            # A-M: shift BACKWARD by shift1, stay in 0-12
            new_idx = (idx - shift1) % 13
        else:
            # N-Z: shift FORWARD by shift2 squared, stay in 13-25
            new_idx = 13 + (idx - 13 + shift2 ** 2) % 13
        return chr(new_idx + ord('A'))

    else:
        return ch                          # spaces, numbers, symbols unchanged


def decrypt_char(ch, shift1, shift2):
    """
    Decrypt a single character by reversing the encryption rules.
    Because encrypt_char keeps each half in its own zone (0-12 or 13-25),
    we can read which half the character belongs to directly from its
    encrypted position — no guessing needed.
    """
    if ch.islower():
        idx = ord(ch) - ord('a')
        if idx <= 12:
            # Was first half (a-m): reverse → subtract shift1 * shift2
            orig = (idx - shift1 * shift2) % 13
            return chr(orig + ord('a'))
        else:
            # Was second half (n-z): reverse → add shift1 + shift2
            orig = 13 + (idx - 13 + (shift1 + shift2)) % 13
            return chr(orig + ord('a'))

    elif ch.isupper():
        idx = ord(ch) - ord('A')
        if idx <= 12:
            # Was first half (A-M): reverse → add shift1
            orig = (idx + shift1) % 13
            return chr(orig + ord('A'))
        else:
            # Was second half (N-Z): reverse → subtract shift2 squared
            orig = 13 + (idx - 13 - shift2 ** 2) % 13
            return chr(orig + ord('A'))

    else:
        return ch                          # spaces, numbers, symbols unchanged


def encrypt(shift1, shift2):
    """
    Read raw_text.txt, encrypt its contents using shift1 and shift2,
    and write the result to encrypted_text.txt.
    """
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        content = f.read()

    encrypted = "".join(encrypt_char(ch, shift1, shift2) for ch in content)

    with open("encrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(encrypted)

    print("Encryption complete. Written to encrypted_text.txt")


def decrypt(shift1, shift2):
    """
    Read encrypted_text.txt, decrypt its contents using shift1 and shift2,
    and write the result to decrypted_text.txt.
    """
    with open("encrypted_text.txt", "r", encoding="utf-8") as f:
        content = f.read()

    decrypted = "".join(decrypt_char(ch, shift1, shift2) for ch in content)

    with open("decrypted_text.txt", "w", encoding="utf-8") as f:
        f.write(decrypted)

    print("Decryption complete. Written to decrypted_text.txt")


def verify():
    """
    Compare raw_text.txt with decrypted_text.txt.
    Print whether the decryption was successful or not.
    """
    with open("raw_text.txt", "r", encoding="utf-8") as f:
        original = f.read()

    with open("decrypted_text.txt", "r", encoding="utf-8") as f:
        decrypted = f.read()

    if original == decrypted:
        print("Verification SUCCESSFUL: Decrypted text matches the original.")
    else:
        print("Verification FAILED: Decrypted text does NOT match the original.")
        for i, (a, b) in enumerate(zip(original, decrypted)):
            if a != b:
                print(f"  First mismatch at position {i}: "
                      f"original={repr(a)}, decrypted={repr(b)}")
                break


# ── Main Program ───────────────────────────────────────────
if __name__ == "__main__":
    try:
        shift1 = int(input("Enter shift1: "))
        shift2 = int(input("Enter shift2: "))
    except ValueError:
        print("Error: Please enter whole numbers for shift1 and shift2.")
    else:
        encrypt(shift1, shift2)
        decrypt(shift1, shift2)
        verify()