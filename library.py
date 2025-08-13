import json
import os
from typing import List, Optional
import httpx
from book import Book


class Library:
    """
    Kütüphane operasyonlarını yöneten sınıf.
    Kitap ekleme, silme, listeleme ve dosya işlemlerini yönetir.
    """
    
    def __init__(self, filename: str = "library.json"):
        """
        Library sınıfının constructor'ı.
        
        Args:
            filename (str): Verilerin saklanacağı JSON dosyasının adı
        """
        self.filename = filename
        self.books: List[Book] = []
        self.load_books()
    
    def add_book(self, isbn: str) -> bool:
        """
        ISBN numarası kullanarak Open Library API'sinden kitap bilgilerini çeker ve kütüphaneye ekler.
        
        Args:
            isbn (str): Eklenecek kitabın ISBN numarası
            
        Returns:
            bool: İşlem başarılıysa True, başarısızsa False
        """
        try:
            # Önce kitabın zaten kütüphanede olup olmadığını kontrol et
            if self.find_book(isbn):
                print(f"ISBN {isbn} numaralı kitap zaten kütüphanede mevcut.")
                return False
            
            # Open Library API'sinden kitap bilgilerini çek
            url = f"https://openlibrary.org/isbn/{isbn}.json"
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url)
                
                if response.status_code == 404:
                    print(f"ISBN {isbn} ile kitap bulunamadı.")
                    return False
                
                response.raise_for_status()
                book_data = response.json()
                
                # Kitap bilgilerini ayıkla
                title = book_data.get("title", "Bilinmeyen Başlık")
                
                # Yazar bilgisini al
                authors = book_data.get("authors", [])
                if authors:
                    # İlk yazarın bilgilerini al
                    author_key = authors[0].get("key", "")
                    if author_key:
                        # Yazarın tam adını al
                        author_url = f"https://openlibrary.org{author_key}.json"
                        author_response = client.get(author_url)
                        if author_response.status_code == 200:
                            author_data = author_response.json()
                            author = author_data.get("name", "Bilinmeyen Yazar")
                        else:
                            author = "Bilinmeyen Yazar"
                    else:
                        author = "Bilinmeyen Yazar"
                else:
                    author = "Bilinmeyen Yazar"
                
                # Yeni kitap nesnesi oluştur ve ekle
                book = Book(title=title, author=author, isbn=isbn)
                self.books.append(book)
                self.save_books()
                
                print(f"Kitap başarıyla eklendi: {book}")
                return True
                
        except httpx.RequestError as e:
            print(f"API isteğinde hata oluştu: {e}")
            return False
        except httpx.HTTPStatusError as e:
            print(f"HTTP hatası: {e}")
            return False
        except Exception as e:
            print(f"Beklenmeyen hata oluştu: {e}")
            return False
    
    def add_book_manual(self, book: Book) -> bool:
        """
        Manuel olarak Book nesnesi ekler (test amaçlı).
        
        Args:
            book (Book): Eklenecek Book nesnesi
            
        Returns:
            bool: İşlem başarılıysa True, başarısızsa False
        """
        # Kitabın zaten var olup olmadığını kontrol et
        if self.find_book(book.isbn):
            print(f"ISBN {book.isbn} numaralı kitap zaten mevcut.")
            return False
        
        self.books.append(book)
        self.save_books()
        print(f"Kitap başarıyla eklendi: {book}")
        return True
    
    def remove_book(self, isbn: str) -> bool:
        """
        ISBN numarasına göre kitabı kütüphaneden siler.
        
        Args:
            isbn (str): Silinecek kitabın ISBN numarası
            
        Returns:
            bool: İşlem başarılıysa True, başarısızsa False
        """
        book = self.find_book(isbn)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Kitap başarıyla silindi: {book}")
            return True
        else:
            print(f"ISBN {isbn} numaralı kitap bulunamadı.")
            return False
    
    def list_books(self) -> List[Book]:
        """
        Kütüphanedeki tüm kitapları listeler.
        
        Returns:
            List[Book]: Kütüphanedeki tüm kitapların listesi
        """
        if not self.books:
            print("Kütüphanede hiç kitap bulunmuyor.")
            return []
        
        print("\n=== KÜTÜPHANE KİTAP LİSTESİ ===")
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")
        print("=" * 35)
        return self.books
    
    def find_book(self, isbn: str) -> Optional[Book]:
        """
        ISBN numarasına göre kitap arar.
        
        Args:
            isbn (str): Aranacak kitabın ISBN numarası
            
        Returns:
            Optional[Book]: Kitap bulunursa Book nesnesi, bulunamazsa None
        """
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def load_books(self) -> None:
        """
        JSON dosyasından kitapları yükler.
        Dosya yoksa boş liste ile başlar.
        """
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.books = [Book.from_dict(book_data) for book_data in data]
                print(f"{len(self.books)} kitap yüklendi.")
            else:
                self.books = []
                print("Yeni kütüphane oluşturuldu.")
        except Exception as e:
            print(f"Kitaplar yüklenirken hata oluştu: {e}")
            self.books = []
    
    def save_books(self) -> None:
        """
        Kütüphanedeki kitapları JSON dosyasına kaydeder.
        """
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                book_dicts = [book.to_dict() for book in self.books]
                json.dump(book_dicts, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Kitaplar kaydedilirken hata oluştu: {e}")
    
    def get_book_count(self) -> int:
        """
        Kütüphanedeki toplam kitap sayısını döndürür.
        
        Returns:
            int: Toplam kitap sayısı
        """
        return len(self.books)