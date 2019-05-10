#  Question 1: Overlapping Lines

def overlap(line_one, line_two):
    """This function receives two lines and determines if they overlap
    or not.
    Args:
        line_one (tuple): The (x1,x2) co-ordinates of the first line.
        line_two (tuple): The (x1,x2) co-ordinates of the second line.

    Returns:
        bool: The return value. True for when line_one and line_two overlap,
        False otherwise.
    """

    # Ensure that line_one starts before line_two
    if line_one[0] > line_two[0]:
        line_one, line_two = line_two, line_one
    
    # if line_two x1 is not between line_one x1 and x2
    # then there isn't an overlap
    if line_two[0] not in range(line_one[0], line_one[1]):
        return False
    
    # Following from the if statement above, if Line_two x2 is
    # after line_one x2 then there is an overlap
    if line_two[1] > line_one[1]:
        return True

    return False