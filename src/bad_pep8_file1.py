def calculate_and_compare(a: int, b: int, c: int) -> int:
    """
    Adds a and b, then compares the result to b + c.
    
    Args:
        a (int): The first number to add.
        b (int): The second number to add.
        c (int): The number to compare to.
    
    Returns:
        int: The sum of a, b, and c.
    """
    sum_ab = a + b
    sum_bc = b + c
    if sum_ab == sum_bc:
        print("equals")
    else:
        print("not equals")
    return sum_ab + sum_bc