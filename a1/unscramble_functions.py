"""CSC108/A08: Fall 2021 -- Assignment 1: unscramble

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as state_str
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Anya Tafliovich.

"""

# Valid moves in the game.
SHIFT = 'S'
SWAP = 'W'
CHECK = 'C'


# We provide a full solution to this function as an example.
def is_valid_move(move: str) -> bool:
    """Return True if and only if move is a valid move. Valid moves are
    SHIFT, SWAP, and CHECK.

    >>> is_valid_move('C')
    True
    >>> is_valid_move('S')
    True
    >>> is_valid_move('W')
    True
    >>> is_valid_move('R')
    False
    >>> is_valid_move('')
    False
    >>> is_valid_move('NOT')
    False

    """

    return move == CHECK or move == SHIFT or move == SWAP

# Your turn! Provide full solutions to the rest of the required functions.
def get_section_start(s_num: int, s_len: int) -> int:
    """Return the index of the first character in the specified section,
    section s_num, which has a length of s_len characters.

    Precondition: s_num >= 1
                  s_len >= 1 (s_len is valid)

    >>> get_section_start(1, 4)
    0
    >>> get_section_start(2, 4)
    4
    >>> get_section_start(1, 3)
    0
    >>> get_section_start(2, 3)
    3

    """

    # The starting index is returned.
    return (s_num - 1) * s_len

def get_section(state_str: str, s_num: int, s_len: int) -> str:
    """Return the section of the given state string state_str that corresponds
    to the given section number s_num and section length s_len.

    Precondition: len(state_str) >= 1
                  s_num is valid for state_str
                  s_len is valid for state_str

    >>> get_section('csca08fun', 2, 3)
    'a08'
    >>> get_section('computerscience', 2, 5)
    'tersc'

    """

    # Slicing & returning the section with calculated starting & endng indices.
    start = get_section_start(s_num, s_len)
    return state_str[start:(start + s_len)]

def is_valid_section(state_str: str, s_num: int, s_len: int) -> bool:
    """Return True if and only if it is possible to divide up the given state
    string state_str into sections of given length s_len and the given section
    number s_num refers to one of the resulting sections after division.

    Precondition: len(state_str) >= 1
                  s_len >= 1

    >>> is_valid_section('csca08fall2021', 2, 3)
    False
    >>> is_valid_section('csca08fall2021', 4, 2)
    True
    >>> is_valid_section('csca08fall2021', 8, 2)
    False

    """

    # Checking if state_str can be evenly divided into sections of s_len
    # characters and if s_num refers to a section after division.
    return len(state_str) % s_len == 0 and len(state_str) // s_len >= s_num

def swap(state_str: str, start: int, end: int) -> str:
    """Return a string which is the result of applying a SWAP operation to
    the given state string state_str between the indices start (inclusive) and
    end (exclusive).

    Precondition: len(state_str) >= 2
                  0 <= start < end <= len(state_str)
                  start < end - 1

    >>> swap('computerscience', 0, 8)
    'romputecscience'
    >>> swap('computerscience', 6, 10)
    'computcrseience'

    """

    # Swapped characters (characters at indices start and (end - 1)) are placed
    # in the original position of other character; other characters (characters
    # before, between, and after the swapping pair) are not affected and
    # "remain" in their original positions.
    return (state_str[:start] + state_str[(end - 1)] +
            state_str[(start + 1):(end - 1)] + state_str[start] +
            state_str[end:])

def shift(state_str: str, start: int, end: int) -> str:
    """Return a string which is the result of applying a SHIFT operation to the
    section of the given state string state_str between the indices start
    (inclusive) and end (exclusive).

    Precondition: len(state_str) >= 2
                  0 <= start < end <= len(state_str)
                  start < end - 1

    >>> shift('computerscience', 0, 8)
    'omputercscience'
    >>> shift('computerscience', 6, 10)
    'computrsceience'

    """

    # Shifted characters' (characters between start and end, both exclusive)
    # indices are decreased by 1 while the first character of the shifted
    # section goes to the end of the section (going from index start (end - 1));
    # other character not affected (before and after the shifted section) are
    # not affected and "remain" in their original positions.
    return (state_str[:start] + state_str[(start + 1):end] + state_str[start] +
            state_str[end:])

def check(state_str: str, start: int, end: int, corr: str) -> bool:
    """Return True if and only if the part/substring of the state string
    state_str between the indices start (inclusive) and end (exclusive) is
    "correct" (equal to the part/substring of the string corr).

    Precondition: 0 <= start <= end <= len(state_str)
                  corr is a valid answer for state_str

    >>> check('ccsa80fun', 6, 9, 'csca08fun')
    True
    >>> check('ccsa80fun', 0, 3, 'csca08fun')
    False

    """

    # Checking if the substrings of state_str and corr, sliced with the same
    # indices, are equal to each other.
    return state_str[start:end] == corr[start:end]

def check_section(state_str: str, s_num: int, s_len: int, corr: str) -> bool:
    """Return True if and only if the section of length s_len and number s_num
    in the given state string state_str is correct/unscrambled correctly (equal
    to the section of length s_len and number s_num in the string corr).

    Precondition: len(state_str) >= 1
                  s_num is valid
                  s_len is valid
                  corr is a valid answer for state_str

    >>> check_section('ccsa80fun', 3, 3, 'csca08fun')
    True
    >>> check_section('ccsa80fun', 1, 3, 'csca08fun')
    False

    """

    # Checking if the sections of state_str and corr, with the same length
    # s_len and number s_num, are equal to each other.
    return (get_section(state_str, s_num, s_len) ==
            get_section(corr, s_num, s_len))

def change_section(state_str: str, move: str, s_num: int, s_len: int) -> str:
    """Return a new game state which results from applying the given move on the
    section with length s_len and number s_num in the state string state_str.

    Precondition: len(state_str) >= 2
                  s_num is valid
                  s_len is valid
                  move is a valid game move that specifies either SWAP or SHIFT

    >>> change_section('computerscience', 'W', 2, 5)
    'compucerstience'
    >>> change_section('computerscience', 'S', 2, 5)
    'compuersctience'

    """

    # Performing a SHIFT or SWAP operation on the substring of state_str,
    # deternmined by the section length s_len and number s_num (used
    # to determine the indices start and end of the section).
    start = get_section_start(s_num, s_len)
    end = get_section_start(s_num, s_len) + s_len
    if move == SHIFT:
        return shift(state_str, start, end)
    return swap(state_str, start, end)

def get_move_hint(state_str: str, s_num: int, s_len: int, corr: str) -> str:
    """Return a suggestion on which game move to perform next based on the
    given state string state_str, the section number s_num, the section length
    s_len, and the correct string corr.

    Precondition: len(state_str) >= 2
                  s_num is valid
                  s_len is valid
                  corr is a valid answer for state_str

    >>> get_move_hint('compucerstience', 2, 5, 'computerscience')
    'W'
    >>> get_move_hint('pucomterscience', 1, 5, 'computerscience')
    'S'
    >>> get_move_hint('TCADOGFOXEMU', 1, 3, 'CATDGOXOFEMU')
    'S'
    >>> get_move_hint('TACDOGFOXEMU', 1, 3, 'CATDOGXOFEMU')
    'W'

    """

    # The results of shifting state_str's section s_num with length s_len are
    # stored in variables.
    start = get_section_start(s_num, s_len)
    end = get_section_start(s_num, s_len) + s_len
    shift_1 = shift(state_str, start, end)
    shift_2 = shift(shift_1, start, end)

    # If one of the shifted results match corr's section s_num, SHIFT is
    # suggested; else, a SWAP is suggested.
    if check_section(shift_1, s_num, s_len, corr) or check_section(shift_2,
                                                                   s_num, s_len,
                                                                   corr):
        return SHIFT
    return SWAP

if __name__ == '__main__':
    import doctest
    doctest.testmod()
