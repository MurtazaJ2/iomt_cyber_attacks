from conf_file import VALUE_ONE, VALUE_TWO

def do_something_bad() -> int:
    """Returns the sum of two values."""
    x = VALUE_ONE
    y = VALUE_TWO
    return x + y

result = do_something_bad()
print(result)