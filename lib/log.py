def stdout(message=None):
    print(message)


def debug(message=None):
    return stdout(f"DEBUG: {message}")


def info(message=None):
    return stdout(f"INFO: {message}")


def error(message=None):
    return stdout(f"ERROR: {message}")
