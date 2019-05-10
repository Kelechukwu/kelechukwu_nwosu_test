def tokenize_version_string(version_string, delimiter="."):
    """The function breaks down version strings in singular characters
    Returns:
        List(string)
    """
    
    # remove prefixes if any
    version_string = version_string.split(" ")[-1]

    tokens = []

    for value in version_string.split(delimiter):
        
        if len(value) > 1:
            # check if is a digit or a combination of 
            # digits and numbers like 2b
            if not value.isdigit():
                for char in value:
                    tokens.append(char)
            else:
               tokens.append(value)
        else:
            tokens.append(value)

    return tokens

def add_filler(version_string_token_a, version_string_token_b, filler="0"):
    """Say you want to compare two version strings of different lengths
    this function will make both have equal length by adding fillers to the
    shorter one. Default filler is 0

    Returns:
        Tuple(string, string)
    """


    a_length = len(version_string_token_a)
    b_length = len(version_string_token_b)

    if a_length == b_length:
        return version_string_token_a, version_string_token_b

    if a_length < b_length:
        diff = b_length - a_length
        version_string_token_a += [filler] * diff

    else:
        diff = a_length - b_length
        version_string_token_b += [filler] * diff

    return version_string_token_a, version_string_token_b