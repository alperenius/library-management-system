#!/usr/bin/env python3
"""
Kütüphane Yönetim Sistemi - Örnek Kullanım
Bu dosya sistemin nasıl kullanılacağını gösteren örnekler içerir.
"""

from book import Book
from library import Library


def example_manual_operations():
    """Manuel kitap işlemleri örneği."""
    print("=== Manuel Kitap İşlemleri Örneği ===")
    
    # Library instance'ı oluştur
    library = Library("example_library.json")
    
    # Manuel kitap ekleme
    book1 = Book("1984", "George Orwell", "978-0451524935")
    book2 = Book("Animal Farm", "George Orwell", "978-0451526342")
    book3 = Book("Brave New World", "Aldous Huxley", "978-0060850524")
    
    print("\n1. Kitapları ekliyoruz...")
    library.add_book_manual(book1)
    library.add_book_manual(book2)
    library.add_book_manual(book3)
    
    print("\n2. Tüm kitapları listeliyoruz:")
    library.list_books()
    
    print(f"\n3. Toplam kitap sayısı: {library.get_book_count()}")
    
    print("\n4. Belirli bir kitap arıyoruz:")
    found_book = library.find_book("978-0451524935")
    if found_book:
        print(f"Bulunan kitap: {found_book}")
    
    print("\n5. Bir kitabı siliyoruz:")
    library.remove_book("978-0451526342")
    
    print("\n6. Güncel kitap listesi:")
    library.list_books()


def example_api_operations():
    """API ile kitap işlemleri örneği."""
    print("\n\n=== API ile Kitap İşlemleri Örneği ===")
    
    # Library instance'ı oluştur
    library = Library("api_example_library.json")
    
    # Bazı popüler kitapların ISBN'leri
    popular_books = [
        "9780451524935",  # 1984 - George Orwell
        "9780061120084",  # To Kill a Mockingbird - Harper Lee
        "9780743273565",  # The Great Gatsby - F. Scott Fitzgerald
    ]
    
    print("\n1. API'den kitap bilgilerini çekiyoruz...")
    for isbn in popular_books:
        print(f"\nISBN {isbn} için kitap ekleniyor...")
        success = library.add_book(isbn)
        if success:
            print("✅ Başarıyla eklendi!")
        else:
            print("❌ Eklenemedi.")
    
    print("\n2. API'den eklenen kitapları listeliyoruz:")
    library.list_books()


def example_book_class():
    """Book sınıfı kullanım örneği."""
    print("\n\n=== Book Sınıfı Kullanım Örneği ===")
    
    # Book nesnesi oluşturma
    book = Book(
        title="Suç ve Ceza",
        author="Fyodor Dostoyevski", 
        isbn="978-9750718656"
    )
    
    print(f"1. Kitap nesnesi: {book}")
    
    # Dictionary'ye dönüştürme
    book_dict = book.to_dict()
    print(f"2. Dictionary formatı: {book_dict}")
    
    # Dictionary'den nesne oluşturma
    new_book = Book.from_dict(book_dict)
    print(f"3. Dictionary'den oluşturulan nesne: {new_book}")
    
    # Eşitlik kontrolü
    print(f"4. Kitaplar eşit mi? {book == new_book}")
    
    # Farklı kitap ile karşılaştırma
    other_book = Book("1984", "George Orwell", "978-0451524935")
    print(f"5. Farklı kitap ile eşit mi? {book == other_book}")


def example_error_handling():
    """Hata yönetimi örnekleri."""
    print("\n\n=== Hata Yönetimi Örnekleri ===")
    
    library = Library("error_example_library.json")
    
    print("1. Geçersiz ISBN ile kitap ekleme:")
    library.add_book("invalid-isbn")
    
    print("\n2. Olmayan kitap silme:")
    library.remove_book("978-0000000000")
    
    print("\n3. Olmayan kitap arama:")
    result = library.find_book("978-0000000000")
    print(f"Arama sonucu: {result}")
    
    print("\n4. Aynı kitabı iki kez ekleme:")
    book = Book("Test Book", "Test Author", "978-1234567890")
    library.add_book_manual(book)
    library.add_book_manual(book)  # Bu başarısız olmalı


def cleanup_example_files():
    """Örnek dosyaları temizle."""
    import os
    
    example_files = [
        "example_library.json",
        "api_example_library.json", 
        "error_example_library.json"
    ]
    
    for filename in example_files:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"✅ {filename} temizlendi.")


if __name__ == "__main__":
    print("Kütüphane Yönetim Sistemi - Örnek Kullanım Senaryoları")
    print("=" * 60)
    
    try:
        # Örnekleri çalıştır
        example_book_class()
        example_manual_operations()
        example_api_operations()
        example_error_handling()
        
    except KeyboardInterrupt:
        print("\n\nÖrnekler kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\n\nBeklenmeyen hata: {e}")
    finally:
        print("\n" + "=" * 60)
        print("Örnek dosyalar temizleniyor...")
        cleanup_example_files()
        print("Örnekler tamamlandı!")