from conf_file import NUMBERS

def another_bad_function() -> list[int]:
    """
    Returns a list of numbers.
    
    Returns:
        list[int]: A list of numbers.
    """
    numbers = NUMBERS
    return [i for i in numbers]