import bcrypt


def gen_salt(length: int = 12):
    """Generate a random salt."""
    if length <= 0:
        raise ValueError("length must be positive(>0)")
    salt = ''
    while len(salt < length):
        salt += bcrypt.gensalt().decode[7:]
    return salt[:length]
