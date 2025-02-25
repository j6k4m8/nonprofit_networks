def deep_dict_access(data: dict, key: str, default=None, raise_keyerror=False):
    """
    Access a nested dictionary using a dot-separated key.
    """
    keys = key.split(".")
    for k in keys:
        try:
            data = data[k]
        except KeyError:
            if raise_keyerror:
                raise KeyError(f"Key '{k}' not found in the dictionary.")
            return default
    return data


__all__ = ["deep_dict_access"]
