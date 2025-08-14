import json
import logging
import os
from typing import List, Optional

import httpx

from book import Book

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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

    def add_book(self, isbn: str) -> Optional[Book]:
        """
        ISBN numarası kullanarak Open Library API'sinden kitap bilgilerini çeker ve kütüphaneye ekler.

        Args:
            isbn (str): Eklenecek kitabın ISBN numarası

        Returns:
            Optional[Book]: İşlem başarılıysa Book nesnesi, başarısızsa None
        """
        if self.find_book(isbn):
            logging.warning(f"ISBN {isbn} numaralı kitap zaten kütüphanede mevcut.")
            return None

        try:
            url = f"https://openlibrary.org/isbn/{isbn}.json"
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url)

                if response.status_code == 404:
                    logging.warning(f"ISBN {isbn} ile kitap bulunamadı.")
                    return None

                response.raise_for_status()
                book_data = response.json()

                title = book_data.get("title", "Bilinmeyen Başlık")
                author = "Bilinmeyen Yazar"
                authors = book_data.get("authors", [])
                if authors:
                    author_key = authors[0].get("key")
                    if author_key:
                        author_url = f"https://openlibrary.org{author_key}.json"
                        author_response = client.get(author_url)
                        if author_response.status_code == 200:
                            author_data = author_response.json()
                            author = author_data.get("name", "Bilinmeyen Yazar")

                book = Book(title=title, author=author, isbn=isbn)
                self.books.append(book)
                self.save_books()
                logging.info(f"Kitap başarıyla eklendi: {book}")
                return book

        except httpx.RequestError as e:
            logging.error(f"API isteğinde hata oluştu: {e}")
            return None
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP hatası: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            logging.error(f"Beklenmeyen hata oluştu: {e}", exc_info=True)
            return None

    def add_book_manual(self, book: Book) -> Optional[Book]:
        """
        Manuel olarak Book nesnesi ekler (test amaçlı).

        Args:
            book (Book): Eklenecek Book nesnesi

        Returns:
            Optional[Book]: İşlem başarılıysa Book nesnesi, başarısızsa None
        """
        if self.find_book(book.isbn):
            logging.warning(f"ISBN {book.isbn} numaralı kitap zaten mevcut.")
            return None

        self.books.append(book)
        self.save_books()
        logging.info(f"Kitap başarıyla eklendi: {book}")
        return book

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
            logging.info(f"Kitap başarıyla silindi: {book}")
            return True
        else:
            logging.warning(f"Silinecek kitap bulunamadı: ISBN {isbn}")
            return False

    def list_books(self) -> List[Book]:
        """
        Kütüphanedeki tüm kitapları listeler.

        Returns:
            List[Book]: Kütüphanedeki tüm kitapların listesi
        """
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
        Dosya yoksa veya bozuksa boş liste ile başlar.
        """
        if not os.path.exists(self.filename):
            logging.info("Kütüphane dosyası bulunamadı. Yeni bir kütüphane oluşturuluyor.")
            self.books = []
            return

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.books = [Book.from_dict(book_data) for book_data in data]
            logging.info(f"{len(self.books)} kitap başarıyla yüklendi.")
        except json.JSONDecodeError as e:
            logging.error(f"Kütüphane dosyası ({self.filename}) bozuk veya yanlış formatta: {e}")
            self.books = []
        except Exception as e:
            logging.error(f"Kitaplar yüklenirken beklenmedik bir hata oluştu: {e}", exc_info=True)
            self.books = []

    def save_books(self) -> None:
        """
        Kütüphanedeki kitapları JSON dosyasına kaydeder.
        """
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                book_dicts = [book.to_dict() for book in self.books]
                json.dump(book_dicts, file, ensure_ascii=False, indent=4)
        except IOError as e:
            logging.error(f"Kitaplar kaydedilirken dosya hatası oluştu ({self.filename}): {e}")
        except Exception as e:
            logging.error(f"Kitaplar kaydedilirken beklenmedik bir hata oluştu: {e}", exc_info=True)

    def get_book_count(self) -> int:
        """
        Kütüphanedeki toplam kitap sayısını döndürür.
        
        Returns:
            int: Toplam kitap sayısı
        """
        return len(self.books)