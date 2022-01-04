def is_hexadecimal(text):
    try:
        int(text, 16)
        return True
    except ValueError:
        return False
