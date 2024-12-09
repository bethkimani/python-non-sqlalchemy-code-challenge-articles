class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not (5 <= len(title) <= 50):
            raise ValueError("Title length must be between 5 and 50 characters inclusive")
        self.author = author
        self.magazine = magazine
        self._title = title
        Article.all.append(self)

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
        # Ensure article is of type Article
        article = Article(self, magazine, title)
        self._articles.append(article)
        magazine.add_article(article)  # Ensure the magazine also has the article added
        return article

    def articles(self):
        return self._articles

    def magazines(self):
        # Ensure that the magazines list is unique
        return list({article.magazine for article in self._articles})

    def topic_areas(self):
        # Return unique categories of magazines (topic areas)
        return list({article.magazine.category for article in self._articles})


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
        self._contributors = []
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Cannot modify the name attribute")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        raise AttributeError("Cannot modify the category attribute")

    def add_article(self, article):
        self._articles.append(article)

    def articles(self):
        return self._articles

    def add_contributor(self, author):
        # Ensure that contributors are unique
        if author not in self._contributors:
            self._contributors.append(author)

    def contributors(self):
        return self._contributors

    def article_titles(self):
        return [article.title for article in self._articles]

    def contributing_authors(self):
        return [article.author for article in self._articles]


# Example usage
if __name__ == "__main__":
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
    print(f"Topic areas of {author1.name}: {[category for category in author1.topic_areas()]}")

    print(f"\nArticles in {magazine1.name}: {magazine1.article_titles()}")
    print(f"Contributing authors in {magazine1.name}: {[author.name for author in magazine1.contributors()]}")
    print(f"\nArticles in {magazine2.name}: {magazine2.article_titles()}")
    print(f"Contributing authors in {magazine2.name}: {[author.name for author in magazine2.contributors()]}")
