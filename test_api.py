#!/usr/bin/env python3
"""
FastAPI uygulaması için integration testler.
"""

import pytest
import tempfile
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from api import app, library
from book import Book


class TestAPI:
    """API endpoint'leri test sınıfı."""
    
    @pytest.fixture(scope="function")
    def client(self):
        """Test client'ı oluşturur."""
        # Geçici dosya ile test
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_filename = f.name
        
        # Library instance'ını geçici dosya ile değiştir
        original_filename = library.filename
        library.filename = temp_filename
        library.books = []
        library.save_books()
        
        client = TestClient(app)
        yield client
        
        # Cleanup
        library.filename = original_filename
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)
    
    def test_root_endpoint(self, client):
        """Ana endpoint testı."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert data["success"] is True
        assert "Kütüphane Yönetim Sistemi API'sine hoş geldiniz" in data["message"]
    
    def test_get_books_empty(self, client):
        """Boş kütüphane listeleme testı."""
        response = client.get("/books")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    def test_get_books_with_data(self, client):
        """Kitapları listeleme testı."""
        # Manual olarak kitap ekle
        book = Book("1984", "George Orwell", "978-0451524935")
        library.add_book_manual(book)
        
        response = client.get("/books")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "1984"
        assert data[0]["author"] == "George Orwell"
        assert data[0]["isbn"] == "978-0451524935"
    
    @patch('library.httpx.Client')
    def test_post_book_success(self, mock_client, client):
        """Başarılı kitap ekleme testı."""
        # Mock API response
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
        
        response = client.post("/books", json={"isbn": "978-0451524935"})
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "1984"
        assert data["author"] == "George Orwell"
        assert data["isbn"] == "978-0451524935"
    
    def test_post_book_invalid_isbn(self, client):
        """Geçersiz ISBN ile kitap ekleme testı."""
        response = client.post("/books", json={"isbn": "123"})
        
        assert response.status_code == 422  # Validation error
    
    def test_post_book_duplicate(self, client):
        """Aynı kitabı iki kez ekleme testı."""
        # İlk kitabı ekle
        book = Book("1984", "George Orwell", "978-0451524935")
        library.add_book_manual(book)
        
        response = client.post("/books", json={"isbn": "978-0451524935"})
        
        assert response.status_code == 400
        data = response.json()
        assert "zaten kütüphanede mevcut" in data["detail"]
    
    @patch('library.httpx.Client')
    def test_post_book_not_found(self, mock_client, client):
        """Bulunamayan kitap ekleme testı."""
        response_mock = Mock()
        response_mock.status_code = 404
        
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = response_mock
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        response = client.post("/books", json={"isbn": "978-0000000000"})
        
        assert response.status_code == 404
        data = response.json()
        assert "bulunamadı" in data["detail"]
    
    def test_get_book_success(self, client):
        """Belirli kitap getirme testı."""
        # Kitap ekle
        book = Book("1984", "George Orwell", "978-0451524935")
        library.add_book_manual(book)
        
        response = client.get("/books/978-0451524935")
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "1984"
        assert data["author"] == "George Orwell"
        assert data["isbn"] == "978-0451524935"
    
    def test_get_book_not_found(self, client):
        """Olmayan kitap getirme testı."""
        response = client.get("/books/978-0000000000")
        
        assert response.status_code == 404
        data = response.json()
        assert "bulunamadı" in data["detail"]
    
    def test_delete_book_success(self, client):
        """Başarılı kitap silme testı."""
        # Kitap ekle
        book = Book("1984", "George Orwell", "978-0451524935")
        library.add_book_manual(book)
        
        response = client.delete("/books/978-0451524935")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "başarıyla silindi" in data["message"]
        
        # Kitabın silindiğini kontrol et
        assert library.find_book("978-0451524935") is None
    
    def test_delete_book_not_found(self, client):
        """Olmayan kitap silme testı."""
        response = client.delete("/books/978-0000000000")
        
        assert response.status_code == 404
        data = response.json()
        assert "bulunamadı" in data["detail"]
    
    def test_get_stats_empty(self, client):
        """Boş kütüphane istatistikleri testı."""
        response = client.get("/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_books"] == 0
        assert data["total_authors"] == 0
        assert data["most_common_authors"] == []
    
    def test_get_stats_with_books(self, client):
        """Kitaplar ile istatistikler testı."""
        # Kitaplar ekle
        book1 = Book("1984", "George Orwell", "978-0451524935")
        book2 = Book("Animal Farm", "George Orwell", "978-0451526342")
        book3 = Book("Brave New World", "Aldous Huxley", "978-0060850524")
        
        library.add_book_manual(book1)
        library.add_book_manual(book2)
        library.add_book_manual(book3)
        
        response = client.get("/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_books"] == 3
        assert data["total_authors"] == 2
        assert "George Orwell" in data["most_common_authors"]
        assert "Aldous Huxley" in data["most_common_authors"]
    
    def test_invalid_json_post(self, client):
        """Geçersiz JSON ile POST isteği testı."""
        response = client.post("/books", json={})
        
        assert response.status_code == 422  # Validation error
    
    def test_missing_isbn_post(self, client):
        """ISBN eksik POST isteği testı."""
        response = client.post("/books", json={"title": "Some Book"})
        
        assert response.status_code == 422  # Validation error