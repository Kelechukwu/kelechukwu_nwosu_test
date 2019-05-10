#  Question 2: Version Comparison
from version.helpers import tokenize_version_string, add_filler

def compare(version_a, version_b):
    """This function receives two version strings and returns a string
    indicating the inequality/equality between version_a and version_b
    Args:
        version_a (string): the first version string 
        version_b (string): the second version string

    Returns:
        string: this is a string indicating the relationship between
        version_a and version_b
        Example:
            version_a is greater than version_b
    """

    sign = "=="

    # first case if both strings are the same then they are equal
    if version_a == version_b:
        return f"{version_a} {sign} {version_b}"
    
    version_a_chars = tokenize_version_string(version_a)
    version_b_chars = tokenize_version_string(version_b)

    version_a_chars, version_b_chars = add_filler(version_a_chars, version_b_chars)

    for x in range(len(version_a_chars)):
        if version_a_chars[x] > version_b_chars[x]:
            sign = ">"
            break
        elif version_a_chars[x] < version_b_chars[x]:
            sign = "<"
            break

    return f"{version_a} {sign} {version_b}"