"""CSC108/A08: Fall 2021 -- Assignment 3: arxiv.org

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Anya Tafliovich.

"""

import copy
from typing import Dict, List, TextIO, Union
from constants import (ID, TITLE, CREATED, MODIFIED, AUTHORS,
                       ABSTRACT, END, SEPARATOR, NameType,
                       ArticleValueType, ArticleType, ArxivType)

EXAMPLE_ARXIV = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
    '031': {
        'identifier': '031',
        'title': 'Calculus is the best course ever',
        'created': None,
        'modified': '2021-09-02',
        'authors': [('Breuss', 'Nataliya')],
        'abstract': '''We discuss the reasons why Calculus I
is the best course.'''},
    '067': {'identifier': '067',
            'title': 'Discrete Mathematics is the best course ever',
            'created': '2021-09-02',
            'modified': '2021-10-01',
            'authors': [('Bretscher', 'Anna'), ('Pancer', 'Richard')],
            'abstract': ('We explain why Discrete Mathematics is the best ' +
                         'course of all times.')},
    '827': {
        'identifier': '827',
        'title': 'University of Toronto is the best university',
        'created': '2021-08-20',
        'modified': '2021-10-02',
        'authors': [('Bretscher', 'Anna'), ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')],
        'abstract': '''We show a formal proof that the University of
Toronto is the best university.'''},
    '042': {
        'identifier': '042',
        'title': None,
        'created': '2021-05-04',
        'modified': '2021-05-05',
        'authors': [],
        'abstract': '''This is a very strange article with no title
and no authors.'''}
}


EXAMPLE_ARXIV_2 = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
    '031': {
        'identifier': '031',
        'title': 'Calculus is the best course ever',
        'created': None,
        'modified': '2021-09-02',
        'authors': [],
        'abstract': '''We discuss the reasons why Calculus I
is the best course.'''}}


EXAMPLE_BY_AUTHOR = {
    ('Ponce', 'Marcelo'): ['008', '827'],
    ('Tafliovich', 'Anya Y.'): ['008', '827'],
    ('Bretscher', 'Anna'): ['067', '827'],
    ('Breuss', 'Nataliya'): ['031'],
    ('Pancer', 'Richard'): ['067']
}


EXAMPLE_FILE_CONTENT = ['008', 'Intro to CS is the best course ever',
                        '2021-09-01', '', 'Ponce,Marcelo', 'Tafliovich,Anya Y.',
                        '', 'We present clear evidence that Introduction to',
                        'Computer Science is the best course.', 'END', '031',
                        'Calculus is the best course ever', '', '2021-09-02',
                        'Breuss,Nataliya', '',
                        'We discuss the reasons why Calculus I',
                        'is the best course.', 'END', '067',
                        'Discrete Mathematics is the best course ever',
                        '2021-09-02', '2021-10-01', 'Pancer,Richard',
                        'Bretscher,Anna', '',
                        ('We explain why Discrete Mathematics is the best' +
                         ' course of all times.'), 'END', '827',
                        'University of Toronto is the best university',
                        '2021-08-20', '2021-10-02', 'Ponce,Marcelo',
                        'Bretscher,Anna', 'Tafliovich,Anya Y.', '',
                        'We show a formal proof that the University of',
                        'Toronto is the best university.', 'END', '042', '',
                        '2021-05-04', '2021-05-05', '',
                        'This is a very strange article with no title',
                        'and no authors.', 'END']


EXAMPLE_ABSTRACTS = [('We present clear evidence that Introduction to\n' +
                      'Computer Science is the best course.'),
                     ('We discuss the reasons why Calculus I\n' +
                      'is the best course.'),
                     ('We explain why Discrete Mathematics is the best' +
                      ' course of all times.')]


EXAMPLE_AUTHORS = [[('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')],
                   [('Breuss', 'Nataliya')],
                   []]


EXAMPLE_DATA = ['008', '2021-09-01', None]


def make_author_to_articles(id_to_article: ArxivType) -> Dict[NameType,
                                                              List[str]]:
    """Return a dict that maps each author name to a list (sorted in
    lexicographic order) of IDs of articles written by that author,
    based on the information in id_to_article.

    >>> make_author_to_articles(EXAMPLE_ARXIV) == EXAMPLE_BY_AUTHOR
    True
    >>> make_author_to_articles({}) == {}
    True
    >>> make_author_to_articles(EXAMPLE_ARXIV_2) == {}
    True

    """

    # For each of the articles, the authors are recorded as keys and articles by
    # the authors are added to the corresponding author(s)'s list(s).
    author_to_atcls = {}
    for key in id_to_article:
        for i in id_to_article[key][AUTHORS]:
            if i in author_to_atcls:
                author_to_atcls[i].append(key)
            else:
                author_to_atcls[i] = [key]
    # The lists of articles by each author is then sorted and stored.
    for i in author_to_atcls:
        author_to_atcls[i] = sorted(author_to_atcls[i])
    return author_to_atcls


def get_coauthors(id_to_article: ArxivType, author: NameType) -> List[NameType]:
    """Return a list (sorted in lexicographic order) of coauthors who published
    articles together with the given author, based on the information in
    id_to_article.

    >>> get_coauthors(EXAMPLE_ARXIV, ('Tafliovich', 'Anya Y.'))
    [('Bretscher', 'Anna'), ('Ponce', 'Marcelo')]
    >>> get_coauthors(EXAMPLE_ARXIV, ('Tafliovich', 'Anya'))
    []
    >>> get_coauthors({}, ())
    []
    >>> get_coauthors({}, ('Tafliovich', 'Anya Y.'))
    []
    >>> get_coauthors(EXAMPLE_ARXIV_2, ('Tafliovich', 'Anya Y.'))
    []

    """

    # For each of author's article, the list of authors is appended. Then, names
    # that are not duplicates nor the name of author are combined and returned.
    coauthors_all = []
    coauthors_modified = []
    for key in id_to_article:
        if author in id_to_article[key][AUTHORS]:
            coauthors_all += id_to_article[key][AUTHORS]
    coauthors_all = sorted(coauthors_all)
    for i in range(len(coauthors_all)):
        coauthor = coauthors_all[i]
        if not (coauthor in coauthors_modified or coauthor == author):
            coauthors_modified.append(coauthors_all[i])
    return coauthors_modified


def get_most_published_authors(id_to_article: ArxivType) -> List[NameType]:
    """Return a list of authors who published the most articles, based on the
    information in id_to_article.

    >>> get_most_published_authors(EXAMPLE_ARXIV)
    [('Bretscher', 'Anna'), ('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
    >>> get_most_published_authors({})
    []
    >>> get_most_published_authors(EXAMPLE_ARXIV_2)
    []

    """

    # A dictionary of author to articles is generated first using id_to_article.
    # Then, using this information, the dict is traversed and the maximum amount
    # of published articles is found and used to find authors who has published
    # this number of articles. This list of authors is then sorted and returned.
    most_published_authors = []
    author_to_atcls = make_author_to_articles(id_to_article)
    max_articles = -1
    for author in author_to_atcls:
        if max_articles < len(author_to_atcls[author]):
            max_articles = len(author_to_atcls[author])

    for author in author_to_atcls:
        if max_articles == len(author_to_atcls[author]):
            most_published_authors.append(author)
    return sorted(most_published_authors)


def suggest_collaborators(id_to_article: ArxivType,
                          author: NameType) -> List[NameType]:
    """Return a list of authors (sorted in lexicographic order) with whom the
    specified author is encouraged to collaborate with (including all authors
    who are coauthors of author's coauthors), based on the information in
    id_to_article.

    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Pancer', 'Richard'))
    [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Tafliovich', 'Anya Y.'))
    [('Pancer', 'Richard')]
    >>> suggest_collaborators(EXAMPLE_ARXIV, ('Bretscher', 'Anna'))
    []

    """

    suggested_authors_all = []
    suggested_modified = []
    coauthors_of_author = get_coauthors(id_to_article, author)
    for coauthor in coauthors_of_author:
        suggested_authors_all += get_coauthors(id_to_article, coauthor)
    suggested_authors_all = sorted(suggested_authors_all)
    for i in range(len(suggested_authors_all)):
        suggested_author = suggested_authors_all[i]
        if not (suggested_author in suggested_modified
                or suggested_author == author
                or suggested_author in coauthors_of_author):
            suggested_modified.append(suggested_authors_all[i])
    return suggested_modified


def has_prolific_authors(author_to_article: Dict[NameType, List[str]],
                         article: ArticleType, min_publications: int) -> bool:
    """Return True if and only if the specific article has at least one author
    who is considered prolific (has published at least min_publications articles
    or more).

    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, EXAMPLE_ARXIV["008"], 2)
    True
    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, EXAMPLE_ARXIV["008"], 3)
    False
    >>> has_prolific_authors(EXAMPLE_BY_AUTHOR, EXAMPLE_ARXIV["031"], 2)
    False

    """

    has_pro_author = False
    for author in article[AUTHORS]:
        if len(author_to_article[author]) >= min_publications:
            has_pro_author = True
            break
    return has_pro_author


def keep_prolific_authors(id_to_article: ArxivType,
                          min_publications: int) -> None:
    """Update id_to_article so that it contains only articles published by
    authors with min_publications or more articles published. As long
    as at least one of the authors has min_publications, the article
    is kept.

    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
    >>> keep_prolific_authors(arxiv_copy, 2)
    >>> len(arxiv_copy)
    3
    >>> '008' in arxiv_copy and '067' in arxiv_copy and '827' in arxiv_copy
    True
    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
    >>> keep_prolific_authors(arxiv_copy, 3)
    >>> len(arxiv_copy)
    0
    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV_2)
    >>> keep_prolific_authors(arxiv_copy, 2)
    >>> len(arxiv_copy)
    0

    """

    articles_to_delete = []
    author_to_atcl = make_author_to_articles(id_to_article)
    for key in id_to_article:
        if not has_prolific_authors(author_to_atcl,
                                    id_to_article[key], min_publications):
            articles_to_delete.append(key)
    for i in articles_to_delete:
        del id_to_article[i]


def read_arxiv_file(afile: TextIO) -> ArxivType:
    """Return a dict containing all arxiv information in afile.

    Precondition: afile is open for reading
                  afile is in the format described in the handout

    """

    arxiv_data = {}
    atcl_data = {} # atcl = article
    file_contents = afile.read().strip().split("\n")
    i = 0
    while i < len(file_contents):
        atcl_data[ID] = read_data(file_contents, i)
        atcl_data[TITLE] = read_data(file_contents, i + 1)
        atcl_data[CREATED] = read_data(file_contents, i + 2)
        atcl_data[MODIFIED] = read_data(file_contents, i + 3)
        i += 4
        atcl_data[AUTHORS] = read_authors(file_contents, i)
        i += len(atcl_data[AUTHORS]) + 1
        atcl_data[ABSTRACT] = read_abstract(file_contents, i)
        if atcl_data[ABSTRACT] is not None:
            i += atcl_data[ABSTRACT].count('\n') + 2
        else:
            i += 2
        arxiv_data[atcl_data[ID]] = copy.deepcopy(atcl_data)
        atcl_data.clear()
    return arxiv_data


def read_abstract(file_contents: List[str], i: int) -> str:
    """Return the abstract of the current article or None if the abstract does
    not exist, based on the given line number i and given file_contents.

    Precondition: afile was open for reading
                  afile is in the format described in the handout
                  file_contents contains all lines of the file
                  4 < i < len(file_contents)

    >>> read_abstract(EXAMPLE_FILE_CONTENT, 7) == EXAMPLE_ABSTRACTS[0]
    True
    >>> read_abstract(EXAMPLE_FILE_CONTENT, 16) == EXAMPLE_ABSTRACTS[1]
    True
    >>> read_abstract(EXAMPLE_FILE_CONTENT, 26) == EXAMPLE_ABSTRACTS[2]
    True

    """

    # Concatenates lines of the abstract or none, if the line is already END.
    line = file_contents[i]
    abstract_lines = ''
    if line == END:
        abstract_lines = None
    else:
        while line != END:
            line = file_contents[i]
            abstract_lines += line + '\n'
            i += 1
            line = file_contents[i]
        abstract_lines = abstract_lines[:-1]
    return abstract_lines


def read_authors(file_contents: List[str], i: int) -> List[NameType]:
    """Return the authors of the current article, based on the given line
    number i and given file_contents.

    Precondition: afile was open for reading
                  afile is in the format described in the handout
                  file_contents contains all lines of the file
                  3 < i < len(file_contents)

    >>> read_authors(EXAMPLE_FILE_CONTENT, 4) == EXAMPLE_AUTHORS[0]
    True
    >>> read_authors(EXAMPLE_FILE_CONTENT, 14) == EXAMPLE_AUTHORS[1]
    True
    >>> read_authors(EXAMPLE_FILE_CONTENT, 43) == EXAMPLE_AUTHORS[2]
    True

    """

    # For each line before the newline character, the name is split into a tuple
    # and added to the list of names.
    line = file_contents[i]
    names = []
    if line != "":
        while line != "":
            line = file_contents[i]
            name = tuple(line.split(","))
            names.append(name)
            i += 1
            line = file_contents[i]
    return sorted(names)


def read_data(file_contents: List[str], i: int) -> str:
    """Return the current line of data or None if the abstract does
    not exist, based on the given line number i and given file_contents.

    Precondition: afile was open for reading
                  afile is in the format described in the handout
                  file_contents contains all lines of the file
                  0 <= i < len(file_contents)

    >>> read_data(EXAMPLE_FILE_CONTENT, 0) == EXAMPLE_DATA[0]
    True
    >>> read_data(EXAMPLE_FILE_CONTENT, 2) == EXAMPLE_DATA[1]
    True
    >>> read_data(EXAMPLE_FILE_CONTENT, 3) == EXAMPLE_DATA[2]
    True

    """

    # Return the contents of the line or none, if the line is empty.
    line = file_contents[i]
    if line == "":
        line = None
    return line


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open('example_data.txt') as example_data:
        example_arxiv = read_arxiv_file(example_data)
        print('Did we produce a correct dict? ',
              example_arxiv == EXAMPLE_ARXIV)

    with open('data.txt') as data:
        arxiv = read_arxiv_file(data)

    author_to_articles = make_author_to_articles(arxiv)
    most_published = get_most_published_authors(arxiv)
    print(most_published)
    print(get_coauthors(arxiv, ('Varanasi', 'Mahesh K.')))  # one
    print(get_coauthors(arxiv, ('Chablat', 'Damien')))  # many
