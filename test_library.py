#!/usr/bin/env python3
"""
Library sınıfı için unit testler.
"""

import pytest
import os
import json
import tempfile
from unittest.mock import patch, Mock
import httpx

from library import Library
from book import Book


class TestLibrary:
    """Library sınıfı test sınıfı."""
    
    @pytest.fixture
    def temp_library(self):
        """Geçici dosya ile Library instance'ı oluşturur."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_filename = f.name
        
        library = Library(temp_filename)
        yield library
        
        # Cleanup
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)
    
    def test_library_initialization(self, temp_library):
        """Library başlatma testı."""
        assert isinstance(temp_library.books, list)
        assert len(temp_library.books) == 0
        assert temp_library.get_book_count() == 0
    
    def test_add_book_manual(self, temp_library):
        """Manuel kitap ekleme testı."""
        book = Book("1984", "George Orwell", "978-0451524935")
        
        result = temp_library.add_book_manual(book)
        
        assert result is True
        assert len(temp_library.books) == 1
        assert temp_library.books[0] == book
    
    def test_add_duplicate_book_manual(self, temp_library):
        """Aynı kitabı iki kez ekleme testı."""
        book = Book("1984", "George Orwell", "978-0451524935")
        
        # İlk ekleme başarılı olmalı
        result1 = temp_library.add_book_manual(book)
        assert result1 is True
        
        # İkinci ekleme başarısız olmalı
        result2 = temp_library.add_book_manual(book)
        assert result2 is False
        assert len(temp_library.books) == 1
    
    def test_remove_book(self, temp_library):
        """Kitap silme testı."""
        book = Book("1984", "George Orwell", "978-0451524935")
        temp_library.add_book_manual(book)
        
        result = temp_library.remove_book("978-0451524935")
        
        assert result is True
        assert len(temp_library.books) == 0
    
    def test_remove_nonexistent_book(self, temp_library):
        """Olmayan kitap silme testı."""
        result = temp_library.remove_book("978-0000000000")
        
        assert result is False
        assert len(temp_library.books) == 0
    
    def test_find_book(self, temp_library):
        """Kitap bulma testı."""
        book = Book("1984", "George Orwell", "978-0451524935")
        temp_library.add_book_manual(book)
        
        found_book = temp_library.find_book("978-0451524935")
        
        assert found_book is not None
        assert found_book == book
    
    def test_find_nonexistent_book(self, temp_library):
        """Olmayan kitap arama testı."""
        found_book = temp_library.find_book("978-0000000000")
        
        assert found_book is None
    
    def test_list_books_empty(self, temp_library):
        """Boş kütüphane listeleme testı."""
        books = temp_library.list_books()
        
        assert books == []
        assert len(books) == 0
    
    def test_list_books_with_books(self, temp_library):
        """Kitapları listeleme testı."""
        book1 = Book("1984", "George Orwell", "978-0451524935")
        book2 = Book("Animal Farm", "George Orwell", "978-0451526342")
        
        temp_library.add_book_manual(book1)
        temp_library.add_book_manual(book2)
        
        books = temp_library.list_books()
        
        assert len(books) == 2
        assert book1 in books
        assert book2 in books
    
    def test_save_and_load_books(self, temp_library):
        """Kitapları kaydetme ve yükleme testı."""
        book1 = Book("1984", "George Orwell", "978-0451524935")
        book2 = Book("Animal Farm", "George Orwell", "978-0451526342")
        
        temp_library.add_book_manual(book1)
        temp_library.add_book_manual(book2)
        
        # Yeni library instance'ı oluştur (aynı dosya ile)
        new_library = Library(temp_library.filename)
        
        assert len(new_library.books) == 2
        assert new_library.find_book("978-0451524935") is not None
        assert new_library.find_book("978-0451526342") is not None
    
    @patch('httpx.Client')
    def test_add_book_api_success(self, mock_client, temp_library):
        """API'den başarılı kitap ekleme testı."""
        # Mock response'ları ayarla
        book_response = Mock()
        book_response.status_code = 200
        book_response.json.return_value = {
            "title": "1984",
            "authors": [{"key": "/authors/OL23919A"}]
        }
        
        author_response = Mock()
        author_response.status_code = 200
        author_response.json.return_value = {
            "name": "George Orwell"
        }
        
        mock_client_instance = Mock()
        mock_client_instance.get.side_effect = [book_response, author_response]
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        result = temp_library.add_book("978-0451524935")
        
        assert result is True
        assert len(temp_library.books) == 1
        assert temp_library.books[0].title == "1984"
        assert temp_library.books[0].author == "George Orwell"
        assert temp_library.books[0].isbn == "978-0451524935"
    
    @patch('httpx.Client')
    def test_add_book_api_not_found(self, mock_client, temp_library):
        """API'den kitap bulunamama testı."""
        response = Mock()
        response.status_code = 404
        
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = response
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        result = temp_library.add_book("978-0000000000")
        
        assert result is False
        assert len(temp_library.books) == 0
    
    @patch('httpx.Client')
    def test_add_book_api_connection_error(self, mock_client, temp_library):
        """API bağlantı hatası testı."""
        mock_client_instance = Mock()
        mock_client_instance.get.side_effect = httpx.RequestError("Connection failed")
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        result = temp_library.add_book("978-0451524935")
        
        assert result is False
        assert len(temp_library.books) == 0
    
    @patch('httpx.Client')
    def test_add_book_api_no_author(self, mock_client, temp_library):
        """API'den yazar bilgisi olmayan kitap testı."""
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "title": "Unknown Book",
            "authors": []
        }
        
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = response
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        result = temp_library.add_book("978-0451524935")
        
        assert result is True
        assert len(temp_library.books) == 1
        assert temp_library.books[0].author == "Bilinmeyen Yazar"
    
    def test_get_book_count(self, temp_library):
        """Kitap sayısı testı."""
        assert temp_library.get_book_count() == 0
        
        book = Book("1984", "George Orwell", "978-0451524935")
        temp_library.add_book_manual(book)
        
        assert temp_library.get_book_count() == 1