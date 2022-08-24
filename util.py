
def is_set(val) -> bool:
    if isinstance(val, int):
        return val is not None
    if isinstance(val, str):
        return val is not None and val != ""
    if isinstance(val, list):
        return val is not None and len(val) > 0
    return val is not None
