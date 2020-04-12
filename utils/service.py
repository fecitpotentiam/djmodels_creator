MAX_INTEGER = 2147483647


def roundup(x: int):
    """
    Round to the next hundred
    :param x: raw value
    :return: rounded value
    """
    return x if x % 100 == 0 else x + 100 - x % 100


def is_max_int(values: list) -> bool:
    """
    :param values: list of values in dataframe's column
    :return: Is max value larger then IntegerField
    """
    if max(values) > MAX_INTEGER or min(values) < -MAX_INTEGER:
        return True