def add_and_compare(a: int, b: int, c: int) -> int:
    """
    This function adds two numbers and compares the result with the sum of the other two numbers.
    
    Args:
        a (int): The first number.
        b (int): The second number.
        c (int): The third number.
    
    Returns:
        int: The sum of the three numbers.
    """
    sum_ab = a + b
    sum_bc = b + c
    if sum_ab == sum_bc:
        print("equals")
    else:
        pass
    return sum_ab + sum_bc