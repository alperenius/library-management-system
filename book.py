class Book:
    """
    Bir kitabı temsil eden sınıf.
    """
    
    def __init__(self, title: str, author: str, isbn: str):
        """
        Book sınıfının constructor'ı.
        
        Args:
            title (str): Kitabın başlığı
            author (str): Kitabın yazarı
            isbn (str): Kitabın ISBN numarası (benzersiz kimlik)
        """
        self.title = title
        self.author = author
        self.isbn = isbn
    
    def __str__(self) -> str:
        """
        Kitap nesnesinin string reprezentasyonu.
        
        Returns:
            str: Kitap bilgilerini okunaklı formatta döndürür
        """
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
    def __eq__(self, other) -> bool:
        """
        İki kitap nesnesinin eşit olup olmadığını kontrol eder.
        ISBN numarasına göre karşılaştırma yapar.
        
        Args:
            other: Karşılaştırılacak diğer nesne
            
        Returns:
            bool: Kitaplar eşitse True, değilse False
        """
        if not isinstance(other, Book):
            return False
        return self.isbn == other.isbn
    
    def to_dict(self) -> dict:
        """
        Kitap nesnesini dictionary'ye dönüştürür.
        JSON serialization için kullanılır.
        
        Returns:
            dict: Kitap bilgilerini içeren dictionary
        """
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """
        Dictionary'den Book nesnesi oluşturur.
        JSON deserialization için kullanılır.
        
        Args:
            data (dict): Kitap bilgilerini içeren dictionary
            
        Returns:
            Book: Oluşturulan Book nesnesi
        """
        return cls(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"]
        )