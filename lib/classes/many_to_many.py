class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not (5 <= len(title) <= 50):
            raise ValueError("Title length must be between 5 and 50 characters inclusive")
        self.author = author
        self.magazine = magazine
        self._title = title
        Article.all.append(self)

        # Automatically add the article to the author's and magazine's collections
        author._articles.append(self)
        magazine._articles.append(self)
        magazine.add_contributor(author)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        raise AttributeError("Title attribute is immutable")

    @title.deleter
    def title(self):
        raise AttributeError("Title attribute cannot be deleted")


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Cannot modify the name attribute")

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def articles(self):
        return self._articles

    def magazines(self):
        return list({article.magazine for article in self._articles})

    def topic_areas(self):
        if not self._articles:
            return None  # Return None when there are no articles
        return list({magazine._category for magazine in self.magazines()})

    # Override equality and hashing to ensure authors with the same name are considered equal
    def __eq__(self, other):
        if isinstance(other, Author):
            return self._name == other.name
        return False

    def __hash__(self):
        return hash(self._name)  # Hash based on the name, assuming it's unique enough


class Magazine:
    all = []

    def __init__(self, name, category):
        if not isinstance(name, str) or len(name) < 2 or len(name) > 16:
            raise ValueError("Name must be a string between 2 and 16 characters")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string")
        self._name = name
        self._category = category
        self._articles = []
        self._contributors = set()  # Use set to ensure uniqueness of contributors
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string between 2 and 16 characters")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string")

    def articles(self):
        return self._articles

    def add_contributor(self, author):
        """Ensure unique contributors"""
        self._contributors.add(author)  # Adds only unique authors

    def contributors(self):
        return list(self._contributors)  # Return list of unique authors

    def article_titles(self):
        return [article.title for article in self._articles]


# Example usage:

def test_contributors_are_unique():
    """magazine contributors are unique"""
    author_1 = Author("Carry Bradshaw")
    author_2 = Author("Nathaniel Hawthorne")
    magazine_1 = Magazine("Vogue", "Fashion")
    Article(author_1, magazine_1, "How to wear a tutu with style")
    Article(author_1, magazine_1, "How to be single and happy")
    Article(author_2, magazine_1, "Dating life in NYC")

    # Ensure contributors are unique
    contributors = magazine_1.contributors()
    assert len(set(contributors)) == 2  # Assert that the list of contributors has exactly two authors
    assert all(isinstance(contributor, Author) for contributor in contributors)  # Ensure all contributors are of type Author

    print(f"Contributors in {magazine_1.name}: {[author.name for author in contributors]}")

# Run the test
test_contributors_are_unique()

# Create authors
author1 = Author("John Doe")
author2 = Author("Jane Smith")

# Create magazines
magazine1 = Magazine("Tech Today", "Technology")
magazine2 = Magazine("Health Weekly", "Health")

# Create articles
article1 = author1.add_article(magazine1, "The Future of AI")
article2 = author2.add_article(magazine1, "The Impact of 5G")
article3 = author1.add_article(magazine2, "Mental Health in the Digital Age")

# Display information
print(f"Articles written by {author1.name}: {[article.title for article in author1.articles()]}")
print(f"Magazines written by {author1.name}: {[magazine.name for magazine in author1.magazines()]}")
print(f"Topic areas of {author1.name}: {author1.topic_areas()}")

print(f"\nArticles in {magazine1.name}: {magazine1.article_titles()}")
print(f"Contributing authors in {magazine1.name}: {[author.name for author in magazine1.contributors()]}")
print(f"\nArticles in {magazine2.name}: {magazine2.article_titles()}")
print(f"Contributing authors in {magazine2.name}: {[author.name for author in magazine2.contributors()]}")
