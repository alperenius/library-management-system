#!/usr/bin/env python3
"""
Book sınıfı için unit testler.
"""

import pytest
from book import Book


class TestBook:
    """Book sınıfı test sınıfı."""
    
    def test_book_creation(self):
        """Book nesnesi oluşturma testı."""
        book = Book("1984", "George Orwell", "978-0451524935")
        
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.isbn == "978-0451524935"
    
    def test_book_str_representation(self):
        """Book nesnesinin string reprezentasyonu testı."""
        book = Book("1984", "George Orwell", "978-0451524935")
        expected = "1984 by George Orwell (ISBN: 978-0451524935)"
        
        assert str(book) == expected
    
    def test_book_equality(self):
        """Book nesnelerinin eşitlik karşılaştırması testı."""
        book1 = Book("1984", "George Orwell", "978-0451524935")
        book2 = Book("1984", "George Orwell", "978-0451524935")
        book3 = Book("Animal Farm", "George Orwell", "978-0451526342")
        
        assert book1 == book2
        assert book1 != book3
        assert book2 != book3
    
    def test_book_equality_with_different_types(self):
        """Book nesnesinin farklı tiplerle karşılaştırılması testı."""
        book = Book("1984", "George Orwell", "978-0451524935")
        
        assert book != "string"
        assert book != 123
        assert book != None
        assert book != []
    
    def test_to_dict(self):
        """Book nesnesinin dictionary'ye dönüştürülmesi testı."""
        book = Book("1984", "George Orwell", "978-0451524935")
        expected_dict = {
            "title": "1984",
            "author": "George Orwell",
            "isbn": "978-0451524935"
        }
        
        assert book.to_dict() == expected_dict
    
    def test_from_dict(self):
        """Dictionary'den Book nesnesi oluşturma testı."""
        book_dict = {
            "title": "1984",
            "author": "George Orwell",
            "isbn": "978-0451524935"
        }
        
        book = Book.from_dict(book_dict)
        
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.isbn == "978-0451524935"
    
    def test_from_dict_to_dict_roundtrip(self):
        """Dictionary -> Book -> Dictionary dönüşüm testı."""
        original_dict = {
            "title": "1984",
            "author": "George Orwell",
            "isbn": "978-0451524935"
        }
        
        book = Book.from_dict(original_dict)
        result_dict = book.to_dict()
        
        assert result_dict == original_dict
    
    def test_book_with_special_characters(self):
        """Özel karakterler içeren kitap bilgileri testı."""
        book = Book("Üç Kız Kardeş", "Elif Şafak", "978-9750738456")
        
        assert book.title == "Üç Kız Kardeş"
        assert book.author == "Elif Şafak"
        assert book.isbn == "978-9750738456"
        
        expected_str = "Üç Kız Kardeş by Elif Şafak (ISBN: 978-9750738456)"
        assert str(book) == expected_str
    
    def test_book_with_empty_strings(self):
        """Boş string değerlerle Book oluşturma testı."""
        book = Book("", "", "")
        
        assert book.title == ""
        assert book.author == ""
        assert book.isbn == ""
    
    def test_book_with_long_title_and_author(self):
        """Uzun başlık ve yazar adı ile Book oluşturma testı."""
        long_title = "A" * 200
        long_author = "B" * 100
        isbn = "978-0123456789"
        
        book = Book(long_title, long_author, isbn)
        
        assert book.title == long_title
        assert book.author == long_author
        assert book.isbn == isbn