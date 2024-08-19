def parse_tuples_from_db(string_data):
    if string_data == None:
        return string_data
    # Remove outer curly braces
    cleaned_string = string_data.strip('{}')
    
    # Remove quotes around tuples
    cleaned_string = cleaned_string.replace('"', '')
    
    # Split into individual tuple strings
    tuple_strings = cleaned_string.split('),(')
    
    # Remove any remaining parentheses from the first and last elements
    tuple_strings[0] = tuple_strings[0].strip('(')
    tuple_strings[-1] = tuple_strings[-1].strip(')')
    
    # Convert each string into a tuple of strings
    tuple_list = [tuple(item.split(',')) for item in tuple_strings]
    
    return tuple_list