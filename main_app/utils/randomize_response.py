import random

def shuffle_and_return(lst: list, n: int) -> list:
    if n > len(lst):
        raise ValueError("n cannot be greater than the length of the list")
    return random.sample(lst, n)
