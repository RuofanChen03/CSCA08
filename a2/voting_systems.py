"""CSC108/A08: Fall 2021 -- Assignment 2: voting

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Sophia Huynh, Sadia Sharmin,
Elizabeth Patitsas, Anya Tafliovich.

"""

from typing import List

from constants import (COL_RIDING, COL_VOTER, COL_RANK, COL_RANGE,
                       COL_APPROVAL, APPROVAL_TRUE, APPROVAL_FALSE,
                       SEPARATOR)

# In the following docstrings, 'VoteData' refers to a list of 5
# elements of the following types:
#
# at index COL_RIDING: int         (this is the riding number)
# at index COL_VOTER: int         (this is the voter number)
# at index COL_RANK: List[str]   (this is the rank ballot)
# at index COL_RANGE: List[int]   (this is the range ballot)
# at index COL_APPROVAL: List[bool]  (this is the approval ballot)

###############################################################################
# Task 0: Creating example data
###############################################################################

SAMPLE_DATA_1 = [[0, 1, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [1, 4, 2, 3],
                  [False, True, False, False]],
                 [1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
                  [False, False, True, True]],
                 [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
                  [False, True, False, True]],
                 [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
                  [True, False, True, True]]]
SAMPLE_ORDER_1 = ['CPC', 'GREEN', 'LIBERAL', 'NDP']


SAMPLE_DATA_2 = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [4, 0, 5, 0],
                  [True, False, True, False]],
                 [117, 21, ['GREEN', 'LIBERAL', 'NDP', 'CPC'], [4, 5, 5, 5],
                  [True, True, True, True]],
                 [72, 12, ['NDP', 'LIBERAL', 'GREEN', 'CPC'], [0, 1, 1, 5],
                  [False, True, True, True]]]


###############################################################################
# Task 1: Data cleaning
###############################################################################

def clean_data(data: List[List[str]]) -> None:
    """Modify data so that the applicable string values are converted to
    their appropriate type, making data of type List['VoteType'].

    Pre: Each item in data is in the format
     at index COL_RIDING: a str that can be converted to an integer (riding)
     at index COL_VOTER: a str that can be converted to an integer (voter ID)
     at index COL_RANK: a SEPARATOR-separated non-empty string (rank ballot)
     at index COL_RANGE: a SEPARATOR-separated non-empty string of ints
                         (range ballot)
     at index COL_APPROVAL: a SEPARATOR-separated non-empty string of
                         APPROVAL_TRUE's and APPROVAL_FALSE's (approval ballot)

    >>> data = [['0', '1', 'NDP;Liberal;Green;CPC', '1;4;2;3', 'NO;YES;NO;NO']]
    >>> expected = [[0, 1, ['NDP', 'Liberal', 'Green', 'CPC'], [1, 4, 2, 3],
    ...              [False, True, False, False]]]
    >>> clean_data(data)
    >>> data == expected
    True
    >>> data = [['117', '12', 'Liberal;CPC;NDP;Green', '4;0;5;0',
    ...          'YES;NO;YES;NO']]
    >>> expected = [[117, 12, ['Liberal', 'CPC', 'NDP', 'Green'], [4, 0, 5, 0],
    ...              [True, False, True, False]]]
    >>> clean_data(data)
    >>> data == expected
    True
    >>> data = []
    >>> expected = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [4, 0, 5, 0],
    ...              [True, False, True, False]]]
    >>> clean_data(data)
    >>> data == expected
    False
    """

    # Cleans the imported data for each specific column
    # (e.g., data[i][COL_RANGE] list elements converted str -> int).
    for i in range(len(data)):
        data[i][COL_RIDING] = int(data[i][COL_RIDING])
        data[i][COL_VOTER] = int(data[i][COL_VOTER])
        data[i][COL_RANK] = data[i][COL_RANK].split(SEPARATOR)
        data[i][COL_RANGE] = [int(j) for j in
                              data[i][COL_RANGE].split(SEPARATOR)]
        data[i][COL_APPROVAL] = [j == APPROVAL_TRUE for j in
                                 data[i][COL_APPROVAL].split(SEPARATOR)]


###############################################################################
# Task 2: Data extraction
###############################################################################

def extract_column(data: List[list], column: int) -> list:
    """Return a list containing only the elements at index column for each
    sublist in data.

    Pre: each sublist of data has an item at index column.

    >>> extract_column([[1, 2, 3], [4, 5, 6]], 2)
    [3, 6]
    >>> extract_column(SAMPLE_DATA_2, COL_RIDING)
    [117, 117, 72]
    >>> extract_column([], 1)
    []
    """

    # Extracting & returning all elements in the desired column.
    items_in_column = [sublst[column] for sublst in data]
    return items_in_column


def extract_single_ballots(data: List['VoteData']) -> List[str]:
    """Return a list containing only the highest ranked candidate from
    each rank ballot in voting data data.

    Pre: data is a list of valid 'VoteData's
         The rank ballot is at index COL_RANK for each voter.

    >>> extract_single_ballots(SAMPLE_DATA_1)
    ['NDP', 'LIBERAL', 'GREEN', 'LIBERAL']
    >>> extract_single_ballots(SAMPLE_DATA_2)
    ['LIBERAL', 'GREEN', 'NDP']
    >>> extract_single_ballots([])
    []
    """

    # Extracting all lists in data's column COL_RANK (people's rank ballots).
    rank_ballots = extract_column(data, COL_RANK)
    # The first party (i = 0) of each rank ballot is then extracted & returned.
    highest_ranked_parties = extract_column(rank_ballots, 0)
    return highest_ranked_parties


def get_votes_in_riding(data: List['VoteData'],
                        riding: int) -> List['VoteData']:
    """Return a list containing only voting data for riding riding from
    voting data data.

    Pre: data is a list of valid 'VoteData's
         riding is stored at index COL_RIDING for each voter

    >>> expected = [[1, 2, ['LIBERAL', 'NDP', 'GREEN', 'CPC'], [2, 1, 4, 2],
    ...              [False, False, True, True]],
    ...             [1, 3, ['GREEN', 'NDP', 'CPC', 'LIBERAL'], [1, 5, 1, 2],
    ...              [False, True, False, True]],
    ...             [1, 4, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [3, 0, 5, 2],
    ...              [True, False, True, True]]]
    >>> get_votes_in_riding(SAMPLE_DATA_1, 1) == expected
    True
    >>> expected = [[117, 12, ['LIBERAL', 'CPC', 'NDP', 'GREEN'], [4, 0, 5, 0],
    ...              [True, False, True, False]],
    ...             [117, 21, ['GREEN', 'LIBERAL', 'NDP', 'CPC'], [4, 5, 5, 5],
    ...              [True, True, True, True]]]
    >>> get_votes_in_riding(SAMPLE_DATA_2, 117) == expected
    True
    >>> expected = []
    >>> get_votes_in_riding(SAMPLE_DATA_2, 1) == expected
    True
    """

    # Votes (in data) from the desired riding are appended & returned.
    riding_votes = []
    for vote in data:
        if vote[COL_RIDING] == riding:
            riding_votes.append(vote)
    return riding_votes


###############################################################################
# Task 3.1: Plurality Voting System
###############################################################################

def voting_plurality(single_ballots: List[str],
                     party_order: List[str]) -> List[int]:
    """Return the total number of ballots cast for each party in
    single-candidate ballots single_ballots, in the order specified in
    party_order.

    Pre: each item in single_ballots appears in party_order

    >>> voting_plurality(['GREEN', 'GREEN', 'NDP', 'GREEN', 'CPC'],
    ...                  SAMPLE_ORDER_1)
    [1, 3, 0, 1]
    >>> voting_plurality(['LIBERAL', 'GREEN', 'NDP'], SAMPLE_ORDER_1)
    [0, 1, 1, 1]
    >>> voting_plurality([], SAMPLE_ORDER_1)
    [0, 0, 0, 0]
    """

    # Initializing the summary of votes to be 0 for each party.
    vote_summary = []
    for i in party_order:
        vote_summary.append(0)
    # The sum of votes for each party is then modified & returned.
    for vote in single_ballots:
        for i in range(len(party_order)):
            if vote == party_order[i]:
                vote_summary[i] += 1
                break
    return vote_summary


###############################################################################
# Task 3.2: Approval Voting System
###############################################################################

# Note: even though the only thing we need from party_order in this
# function is its length, we still design all voting functions to
# receive party_order, for consistency and readability.
def voting_approval(approval_ballots: List[List[bool]],
                    party_order: List[str]) -> List[int]:
    """Return the total number of approvals for each party in approval
    ballots approval_ballots, in the order specified in party_order.

    Pre: len of each sublist of approval_ballots is len(party_order)
         the approvals in each ballot are specified in the order of party_order

    >>> voting_approval([[True, True, False, False],
    ...                  [False, False, False, True],
    ...                  [False, True, False, False]], SAMPLE_ORDER_1)
    [1, 2, 0, 1]
    >>> voting_approval([[True, False, True, False], [True, True, True, True],
    ...                  [False, True, True, True]], SAMPLE_ORDER_1)
    [2, 2, 3, 2]
    >>> voting_approval([], SAMPLE_ORDER_1)
    [0, 0, 0, 0]
    """

    # Initializing the summary of votes to be 0 for each party.
    vote_summary = []
    for i in party_order:
        vote_summary.append(0)
    # The sum of votes of the parties is then modified & returned.
    for vote in approval_ballots:
        for i in range(len(party_order)):
            if vote[i]:
                vote_summary[i] += 1
    return vote_summary


###############################################################################
# Task 3.3: Range Voting System
###############################################################################

def voting_range(range_ballots: List[List[int]],
                 party_order: List[str]) -> List[int]:
    """Return the total score for each party in range ballots
    range_ballots, in the order specified in party_order.

    Pre: len of each sublist of range_ballots is len(party_order)
         the scores in each ballot are specified in the order of party_order

    >>> voting_range([[1, 3, 4, 5], [5, 5, 1, 2], [1, 4, 1, 1]],
    ...              SAMPLE_ORDER_1)
    [7, 12, 6, 8]
    >>> voting_range([[4, 0, 5, 0], [4, 5, 5, 5],
    ...                  [0, 1, 1, 5]], SAMPLE_ORDER_1)
    [8, 6, 11, 10]
    >>> voting_range([], SAMPLE_ORDER_1)
    [0, 0, 0, 0]
    """

    # Initializing the summary of votes to be 0 for each party.
    vote_summary = []
    for i in party_order:
        vote_summary.append(0)
    # The votes sum of the parties is then modified & returned.
    for vote in range_ballots:
        for i in range(len(party_order)):
            vote_summary[i] += vote[i]
    return vote_summary


###############################################################################
# Task 3.4: Borda Count Voting System
###############################################################################

def voting_borda(rank_ballots: List[List[str]],
                 party_order: List[str]) -> List[int]:
    """Return the Borda count for each party in rank ballots rank_ballots,
    in the order specified in party_order.

    Pre: each ballot contains all and only elements of party_order

    >>> voting_borda([['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...               ['CPC', 'LIBERAL', 'GREEN', 'NDP'],
    ...               ['LIBERAL', 'NDP', 'GREEN', 'CPC']], SAMPLE_ORDER_1)
    [4, 4, 8, 2]
    >>> voting_borda([['LIBERAL', 'CPC', 'NDP', 'GREEN'],
    ...               ['GREEN', 'LIBERAL', 'NDP', 'CPC'],
    ...               ['NDP', 'LIBERAL', 'GREEN', 'CPC']], SAMPLE_ORDER_1)
    [2, 4, 7, 5]
    >>> voting_borda([], SAMPLE_ORDER_1)
    [0, 0, 0, 0]
    """

    # Initializing the summary of votes to be 0 for each party.
    vote_summary = []
    for i in party_order:
        vote_summary.append(0)
    # The votes sum of the parties is then modified, later returned.
    for vote in rank_ballots:
        for i in range(len(party_order)):
            # Assuming that each party only appears once per rank ballot,
            # combined with the fact that its point value is (len(party_order)
            # -1 - party's index in party_order), the indicies of each party
            # of the ballots in party_order were found to calculate the points
            # of the parties for each ballot.
            vote_summary[party_order.index(vote[i])] += len(party_order) - 1 - i
    return vote_summary


###############################################################################
# Task 3.5: Instant Run-off Voting System
###############################################################################

def remove_party(rank_ballots: List[List[str]], party_to_remove: str) -> None:
    """Change rank ballots rank_ballots by removing the party
    party_to_remove from each ballot.

    Pre: party_to_remove is in all of the ballots in rank_ballots.

    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> remove_party(ballots, 'NDP')
    >>> ballots == [['LIBERAL', 'GREEN', 'CPC'],
    ...             ['CPC', 'LIBERAL', 'GREEN'],
    ...             ['CPC', 'GREEN', 'LIBERAL']]
    True
    >>> ballots = [['LIBERAL', 'CPC', 'NDP', 'GREEN'],
    ...            ['GREEN', 'LIBERAL', 'NDP', 'CPC'],
    ...            ['NDP', 'LIBERAL', 'GREEN', 'CPC']]
    >>> remove_party(ballots, 'NDP')
    >>> ballots == [['LIBERAL', 'CPC', 'GREEN'],
    ...             ['GREEN', 'LIBERAL', 'CPC'],
    ...             ['LIBERAL', 'GREEN', 'CPC']]
    True
    >>> ballots = []
    >>> remove_party(ballots, 'CPC')
    >>> ballots == []
    True
    """

    # For each rank ballot, the specific party party_to_remove is removed.
    for i in range(len(rank_ballots)):
        rank_ballots[i].remove(party_to_remove)

def get_lowest(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the lowest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_lowest([16, 100, 4, 200], SAMPLE_ORDER_1)
    'LIBERAL'
    >>> get_lowest([1, 1, 2, 3], SAMPLE_ORDER_1)
    'CPC'
    >>> get_lowest([0, 0, 0, 0], SAMPLE_ORDER_1)
    'CPC'
    """

    # The lowest votes & party are set to those of the first party by default.
    lowest_votes = party_tallies[0]
    lowest_party = party_order[0]
    # The lowest number of votes with the associated party is determined &
    # later returned as the list is traversed.
    for i in party_tallies:
        if i < lowest_votes:
            lowest_votes = i
            lowest_party = party_order[party_tallies.index(i)]
    return lowest_party


def get_winner(party_tallies: List[int], party_order: List[str]) -> str:
    """Return the name of the party with the highest number of votes in the
    list of vote counts per party party_tallies. In case of a tie,
    return the party that occurs earlier in party_order. Totals in
    party_tallies are ordered by party_order.

    Pre: len(party_tallies) == len(party_order) > 0

    >>> get_winner([16, 100, 4, 200], SAMPLE_ORDER_1)
    'NDP'
    >>> get_winner([1, 3, 2, 3], SAMPLE_ORDER_1)
    'GREEN'
    >>> get_winner([0, 0, 0, 0], SAMPLE_ORDER_1)
    'CPC'
    """

    # The highest votes & party are set to those of the first party by default.
    highest_votes = party_tallies[0]
    winning_party = party_order[0]
    # The highest number of votes with the associated party is determined &
    # later returned as the list is traversed.
    for i in party_tallies:
        if i > highest_votes:
            highest_votes = i
            winning_party = party_order[party_tallies.index(i)]
    return winning_party


def voting_irv(rank_ballots: List[List[str]], party_order: List[str]) -> str:
    """Return the party which wins when IRV is performed on the list of
    rank ballots rank_ballots. Change rank_ballots and party_order as
    needed in IRV, removing parties that are eliminated in the
    process. Each ballot in rank_ballots is ordered by party_order.

    Pre: each ballot contains all and only elements of party_order
         len(rank_ballots) > 0

    >>> order = ['CPC', 'GREEN', 'LIBERAL', 'NDP']
    >>> ballots = [['LIBERAL', 'GREEN', 'CPC', 'NDP'],
    ...            ['CPC', 'NDP', 'LIBERAL', 'GREEN'],
    ...            ['NDP', 'CPC', 'GREEN', 'LIBERAL']]
    >>> voting_irv(ballots, order)
    'NDP'
    >>> ballots == [['LIBERAL', 'NDP'],
    ...             ['NDP', 'LIBERAL'],
    ...             ['NDP', 'LIBERAL']]
    True
    >>> order
    ['LIBERAL', 'NDP']
    >>> order = ['CPC', 'GREEN', 'LIBERAL', 'NDP']
    >>> ballots = [['LIBERAL', 'CPC', 'NDP', 'GREEN'],
    ...            ['GREEN', 'LIBERAL', 'NDP', 'CPC'],
    ...            ['NDP', 'LIBERAL', 'GREEN', 'CPC']]
    >>> voting_irv(ballots, order)
    'LIBERAL'
    >>> ballots == [['LIBERAL', 'NDP'],
    ...             ['LIBERAL', 'NDP'],
    ...             ['NDP', 'LIBERAL']]
    True
    >>> order
    ['LIBERAL', 'NDP']
    >>> order = ['CPC', 'GREEN', 'LIBERAL', 'NDP']
    >>> ballots = []
    >>> voting_irv(ballots, order)
    'NDP'
    >>> ballots == []
    True
    >>> order
    ['NDP']
    """

    # Calculating the minimum number of votes needed to win (over 50%).
    minimum_winner_votes = len(rank_ballots) // 2 + 1
    while len(party_order) > 1: 
        # Extracting and computing the number of times each party placed first.
        first_choices = extract_column(rank_ballots, 0)
        ranked_first_summary = voting_plurality(first_choices, party_order)
        # If a party has already won, the winning party's name is returned.
        for j in ranked_first_summary:
            if j >= minimum_winner_votes:
                return party_order[ranked_first_summary.index(j)]
        # If no party has yet to win, least scoring party is found & removed
        # from both the rank ballots and the list party_order.
        losing_party = get_lowest(ranked_first_summary, party_order)
        remove_party(rank_ballots, losing_party)
        party_order.remove(losing_party)
    # The first/remaining party in list party_order is returned as the winner.
    return party_order[0]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
