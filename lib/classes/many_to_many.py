
class Article:
    all = []
    def __init__(self, author, magazine, title):
        if not isinstance(title, str):  
            raise ValueError("Title must be a string")
        self._title = title  
        self.author = author
        self.magazine = magazine
        Article.all.append(self)
    
    @property
    def title(self):
       
        return self._title

    @title.setter
    def title(self, value):
     
        raise AttributeError("title is immutable and cannot be changed")

   

class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("name must be a non-empty string")
        self._name = name  

    @property
    def name(self):
        return self._name 
    
    def articles(self):
        from .many_to_many import Article
        return [article for article in Article.all if article.author == self]
    
    def magazines(self):
        return list({Article.magazine for Article in self.articles()})
    
    def add_article(self, magazine, title):
        from .many_to_many import Article  
      
        if not isinstance(magazine, Magazine):
            raise ValueError("magazine must be an instance of Magazine")
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("title must be a string between 5 and 50 characters")
       
        return Article(self, magazine, title)
    
    def topic_areas(self):
        if not self.articles():
            return None 
        return list({magazine.category for magazine in self.magazines()})
    
  



    

class Magazine:
    all = []  

    def __init__(self, name, category):
       
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("name must be a string between 2 and 16 characters")
        
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("category must be a non-empty string")

        self._name = name  
        self._category = category  
        self.__class__.all.append(self)  
    @property
    def name(self):
        """Getter for name."""
        return self._name

    @name.setter
    def name(self, value):
        """Setter for name with validation."""
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("name must be a string between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        """Getter for category."""
        return self._category

    @category.setter
    def category(self, value):
        """Setter for category with validation."""
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("category must be a non-empty string")
        self._category = value

    def articles(self):
        """Returns all articles associated with this magazine."""
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        """Returns a unique list of authors who have written for this magazine."""
        return list(set(article.author for article in self.articles()))

    def article_titles(self):
        """Returns the titles of all articles in this magazine."""
        return [article.title for article in self.articles()] or None

    def contributing_authors(self):
        """Returns authors with more than 2 articles in this magazine."""
        author_count = {}
        for article in self.articles():
            author = article.author
            author_count[author] = author_count.get(author, 0) + 1
        return [author for author, count in author_count.items() if count > 2] or None

    @classmethod
    def top_publisher(cls):
        """Returns the magazine with the most articles."""
        if not Article.all:
            return None
        return max(cls.all, key=lambda magazine: len(magazine.articles()), default=None)
