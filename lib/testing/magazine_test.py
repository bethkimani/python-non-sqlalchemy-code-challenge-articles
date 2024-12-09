# classes/many_to_many.py

class Author:
    """Author class to represent authors in the system"""
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Article:
    """Article class to represent articles written by authors in magazines"""

    all = []

    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        self.title = title
        Article.all.append(self)

    def __repr__(self):
        return self.title


class Magazine:
    """Magazine class representing a magazine with many articles and many contributors"""
    
    all = []

    def __init__(self, name, category):
        if not isinstance(name, str) or not isinstance(category, str):
            raise Exception("Name and Category must be strings")
        if len(name) < 2 or len(name) > 16:
            raise Exception("Magazine name must be between 2 and 16 characters")
        if len(category) == 0:
            raise Exception("Category cannot be an empty string")
        
        self.name = name
        self.category = category
        self.articles_list = []
        Magazine.all.append(self)

    def articles(self):
        """Returns all articles associated with the magazine"""
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        """Returns all unique authors who have written for the magazine"""
        contributors = {article.author for article in self.articles()}
        return list(contributors)

    def article_titles(self):
        """Returns a list of titles of articles in the magazine"""
        articles = self.articles()
        return [article.title for article in articles] if articles else None

    def contributing_authors(self):
        """Returns authors who have written more than 2 articles for the magazine"""
        authors = {}
        for article in self.articles():
            authors[article.author] = authors.get(article.author, 0) + 1
        return [author for author, count in authors.items() if count > 2]

    @classmethod
    def top_publisher(cls):
        """Returns the magazine with the most articles"""
        if not cls.all:
            return None
        return max(cls.all, key=lambda magazine: len(magazine.articles()))

    def __repr__(self):
        return self.name


# tests/magazine_test.py

import pytest
from classes.many_to_many import Article
from classes.many_to_many import Magazine
from classes.many_to_many import Author


class TestMagazine:
    """Magazine in many_to_many.py"""

    def test_has_name(self):
        """Magazine is initialized with a name"""
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")

        assert magazine_1.name == "Vogue"
        assert magazine_2.name == "AD"

    def test_name_is_mutable_string(self):
        """magazine name is of type str and can change"""
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")

        assert isinstance(magazine_1.name, str)
        assert isinstance(magazine_2.name, str)

        magazine_1.name = "New Yorker"
        assert magazine_1.name == "New Yorker"

        # comment out the next two lines if using Exceptions
        #magazine_2.name = 2
        #assert magazine_2.name == "AD"

        # uncomment the next two lines if using Exceptions
        with pytest.raises(Exception):
            Magazine(2, "Numbers")

    def test_name_len(self):
        """magazine name is between 2 and 16 characters, inclusive"""
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")

        assert 2 <= len(magazine_1.name) <= 16
        assert 2 <= len(magazine_2.name) <= 16

        # comment out the next two lines if using Exceptions
        #magazine_1.name = "New Yorker Plus X"
        #assert magazine_1.name == "Vogue"

        # comment out the next two lines if using Exceptions
        #magazine_2.name = "A"
        #assert magazine_2.name == "AD"

        # uncomment the next two lines if using Exceptions
        with pytest.raises(Exception):
            magazine_1.name = "New Yorker Plus X"

        # uncomment the next two lines if using Exceptions
        with pytest.raises(Exception):
            magazine_2.name = "A"

    def test_has_category(self):
        """Magazine is initialized with a category"""
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")

        assert magazine_1.category == "Fashion"
        assert magazine_2.category == "Architecture"

    def test_category_is_mutable_string(self):
        """magazine category is of type str and can change"""
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")

        assert isinstance(magazine_1.category, str)
        assert isinstance(magazine_2.category, str)

        magazine_1.category = "Life Style"
        assert magazine_1.category == "Life Style"

        assert isinstance(magazine_1.category, str)

        # comment out the next two lines if using Exceptions
        #magazine_2.category = 2
        #assert magazine_2.category == "Architecture"
        
        assert isinstance(magazine_2.category, str)

        # uncomment the next two lines if using Exceptions
        with pytest.raises(Exception):
            Magazine("GQ", 2)

    def test_category_len(self):
        """magazine category has length greater than 0"""
        magazine_1 = Magazine("Vogue", "Fashion")

        assert magazine_1.category != ""

        # comment out the next three lines if using Exceptions
        #magazine_1.category = ""
        # magazine_1.category == "Fashion"
        #assert magazine_1.category != ""

        # uncomment the next two lines if using Exceptions
        with pytest.raises(Exception):
            magazine_1.category = ""

    def test_has_many_articles(self):
        """magazine has many articles"""
        author_1 = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")
        article_1 = Article(author_1, magazine_1, "How to wear a tutu with style")
        article_2 = Article(author_1, magazine_1, "Dating life in NYC")
        article_3 = Article(author_1, magazine_2, "2023 Eccentric Design Trends")

        assert len(magazine_1.articles()) == 2
        assert len(magazine_2.articles()) == 1
        assert article_1 in magazine_1.articles()
        assert article_2 in magazine_1.articles()
        assert article_3 not in magazine_1.articles()
        assert article_3 in magazine_2.articles()

    def test_articles_of_type_articles(self):
        """magazine articles are of type Article"""
        author_1 = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")
        Article(author_1, magazine_1, "How to wear a tutu with style")
        Article(author_1, magazine_1, "Dating life in NYC")
        Article(author_1, magazine_2, "2023 Eccentric Design Trends")

        assert isinstance(magazine_1.articles()[0], Article)
        assert isinstance(magazine_1.articles()[1], Article)
        assert isinstance(magazine_2.articles()[0], Article)

    def test_has_many_contributors(self):
        """magazine has many contributors"""
        author_1 = Author("Carry Bradshaw")
        author_2 = Author("Nathaniel Hawthorne")
        magazine_1 = Magazine("Vogue", "Fashion")
        Article(author_1, magazine_1, "How to wear a tutu with style")
        Article(author_2, magazine_1, "Dating life in NYC")

        assert len(magazine_1.contributors()) == 2
        assert author_1 in magazine_1.contributors()
        assert author_2 in magazine_1.contributors()

    def test_contributors_of_type_author(self):
        """magazine contributors are of type Author"""
        author_1 = Author("Carry Bradshaw")
        author_2 = Author("Nathaniel Hawthorne")
        magazine_1 = Magazine("Vogue", "Fashion")
        Article(author_1, magazine_1, "How to wear a tutu with style")
        Article(author_2, magazine_1, "Dating life in NYC")

        assert isinstance(magazine_1.contributors()[0], Author)
        assert isinstance(magazine_1.contributors()[1], Author)

    def test_contributors_are_unique(self):
        """magazine contributors are unique"""
        author_1 = Author("Carry Bradshaw")
        author_2 = Author("Nathaniel Hawthorne")
        magazine_1 = Magazine("Vogue", "Fashion")
        Article(author_1, magazine_1, "How to wear a tutu with style")
        Article(author_1, magazine_1, "How to be single and happy")
        Article(author_2, magazine_1, "Dating life in NYC")

        assert len(set(magazine_1.contributors())) == len
