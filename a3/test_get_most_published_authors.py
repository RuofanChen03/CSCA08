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
import unittest
from arxiv_functions import get_most_published_authors as get_mpas
from arxiv_functions import EXAMPLE_ARXIV


DATA0 = {}


DATA1 = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''}}


DATA2 = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''}}


DATA3 = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Tafliovich', 'Anya Y.'), ('Ponce', 'Marcelo')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''}}


DATA4 = {
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


DATA5 = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
    '009': {
        'identifier': '009',
        'title': 'Intro to CS is the best course ever2',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course2.'''},
    '067': {
        'identifier': '067',
        'title': 'Discrete Mathematics is the best course ever',
        'created': '2021-09-02',
        'modified': '2021-10-01',
        'authors': [],
        'abstract': '''We explain why Discrete Mathematics is the best
course of all times.'''}}


DATA6 = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
    '009': {
        'identifier': '009',
        'title': 'Intro to CS is the best course ever2',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course2.'''},
    '067': {
        'identifier': '067',
        'title': 'Discrete Mathematics is the best course ever',
        'created': '2021-09-02',
        'modified': '2021-10-01',
        'authors': [('Bretscher', 'Anna'), ('Pancer', 'Richard')],
        'abstract': '''We explain why Discrete Mathematics is the best
course of all times.'''}}


DATA7 = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Tafliovich', 'Anya Y.'), ('Ponce', 'Marcelo')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
    '009': {
        'identifier': '009',
        'title': 'Intro to CS is the best course ever2',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Tafliovich', 'Anya Y.'), ('Ponce', 'Marcelo')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course2.'''},
    '067': {
        'identifier': '067',
        'title': 'Discrete Mathematics is the best course ever',
        'created': '2021-09-02',
        'modified': '2021-10-01',
        'authors': [('Bretscher', 'Anna'), ('Pancer', 'Richard')],
        'abstract': '''We explain why Discrete Mathematics is the best
course of all times.'''}}


DATA8 = {
    '008': {
        'identifier': '008',
        'title': 'Intro to CS is the best course ever',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo'), ('Ponce', 'Anya Y.')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course.'''},
    '009': {
        'identifier': '009',
        'title': 'Intro to CS is the best course ever2',
        'created': '2021-09-01',
        'modified': None,
        'authors': [('Ponce', 'Marcelo')],
        'abstract': '''We present clear evidence that Introduction to
Computer Science is the best course2.'''},
    '067': {
        'identifier': '067',
        'title': 'Discrete Mathematics is the best course ever',
        'created': '2021-09-02',
        'modified': '2021-10-01',
        'authors': [('Bretscher', 'Anna'), ('Pancer', 'Richard'), 
                    ('Ponce', 'Anya Y.')],
        'abstract': '''We explain why Discrete Mathematics is the best
course of all times.'''}}


class TestGetMostPublishedAuthors(unittest.TestCase):
    """Test the function get_most_published_authors."""

    def test_handout_example(self):
        """Test get_most_published_authors with the handout example, which
        includes having 3 authors with the highest number of articles (a tie),
        authors not in lexicographic order, and articles with no authors.
        
        """

        arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
        expected = [('Bretscher', 'Anna'),
                    ('Ponce', 'Marcelo'),
                    ('Tafliovich', 'Anya Y.')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_empty_dict(self):
        """Test get_most_published_authors with an empty Arxiv dictionary.
        """

        arxiv_copy = DATA0
        expected = []
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_1_article_with_no_author(self):
        """Test get_most_published_authors with an Arxiv dict containing only
        1 article, where data regarding its authors does not exists.
        """

        arxiv_copy = DATA1
        expected = []
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_1_article_with_1_author(self):
        """Test get_most_published_authors with an Arxiv dict containing only
        1 article, where the article only has 1 author.
        """

        arxiv_copy = DATA2
        expected = [('Ponce', 'Marcelo')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_1_article_with_multiple_authors(self):
        """Test get_most_published_authors with an Arxiv dict containing only
        1 article, where the article has multiple authors.
        """

        arxiv_copy = DATA3
        expected = [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_multiple_article_with_no_authors(self):
        """Test get_most_published_authors with an Arxiv dict containing
        multiple articles, where data regarding authors of the articles does not
        exist.
        """

        arxiv_copy = DATA4
        expected = []
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_multiple_article_with_only_1_unique_author(self):
        """Test get_most_published_authors with an Arxiv dict containing only
        1 author for the different articles.
        """

        arxiv_copy = DATA5
        expected = [('Ponce', 'Marcelo')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_multiple_article_with_1_most_published_author(self):
        """Test get_most_published_authors with an Arxiv dict containing
        multiple articles, where only 1 author has published the most articles
        (no ties).
        """

        arxiv_copy = DATA6
        expected = [('Ponce', 'Marcelo')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_multiple_article_with_multiple_most_published_authors(self):
        """Test get_most_published_authors with an Arxiv dict containing
        multiple articles, where multiple author have published the same amount,
        which is the max number of articles for this dict, of articles
        (has a tie and should have all authors with the max number of articles).
        """

        arxiv_copy = DATA7
        expected = [('Ponce', 'Marcelo'), ('Tafliovich', 'Anya Y.')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_multiple_article_with_multiple_mpa_with_same_last_name(self):
        """Test get_most_published_authors with an Arxiv dict containing
        multiple articles, where multiple author have published the same amount,
        which is the max number of articles for this dict, of articles
        (has a tie and should have all authors with the max number of articles).
        Of the most published authors, some share the same last name.
        """

        arxiv_copy = DATA8
        expected = [('Ponce', 'Anya Y.'), ('Ponce', 'Marcelo')]
        actual = get_mpas(arxiv_copy)
        msg = message(arxiv_copy, expected, actual)
        self.assertEqual(actual, expected, msg)

    def test_no_mutation(self):
        """Test get_most_published_authors with an Arxiv dict containing
        multiple articles, where multiple author have published the same amount,
        which is the max number of articles for this dict, of articles
        (has a tie and should have all authors with the max number of articles).
        Of the most published authors, some share the same last name.
        """

        arxiv_copy = DATA8
        actual = get_mpas(arxiv_copy)
        expected = DATA8
        msg = ("We expected the input to not be modified and stay "
               + str(expected) + ", but it got changed to " + str(arxiv_copy))
        self.assertEqual(arxiv_copy, expected, msg)


def message(test_case: dict, expected: list, actual: object) -> str:
    """Return an error message saying the function call
    get_most_published_authors(test_case) resulted in the value
    actual, when the correct value is expected.

    """

    return ("When we called get_most_published_authors(" + str(test_case) +
            ") we expected " + str(expected) +
            ", but got " + str(actual))


if __name__ == '__main__':
    unittest.main(exit=False)
