#!/usr/bin/env python3
"""
Kütüphane Yönetim Sistemi - Ana Uygulama
Python 202 Bootcamp Bitirme Projesi

Bu modül kütüphane yönetim sisteminin komut satırı arayüzünü sağlar.
Kullanıcılar kitap ekleme, silme, listeleme ve arama işlemlerini yapabilir.
"""

from library import Library


def display_menu():
    """Ana menüyü gösterir."""
    print("\n" + "="*40)
    print("    KÜTÜPHANE YÖNETİM SİSTEMİ")
    print("="*40)
    print("1. Kitap Ekle")
    print("2. Kitap Sil") 
    print("3. Kitapları Listele")
    print("4. Kitap Ara")
    print("5. Çıkış")
    print("="*40)


def add_book(library: Library):
    """Kullanıcıdan ISBN alarak kitap ekler."""
    print("\n--- Kitap Ekleme ---")
    isbn = input("Kitabın ISBN numarasını girin: ").strip()
    
    if not isbn:
        print("Hata: ISBN numarası boş olamaz.")
        return
    
    print("Kitap bilgileri getiriliyor...")
    library.add_book(isbn)


def remove_book(library: Library):
    """Kullanıcıdan ISBN alarak kitap siler."""
    print("\n--- Kitap Silme ---")
    
    # Önce mevcut kitapları göster
    if library.get_book_count() == 0:
        print("Kütüphanede silinecek kitap bulunmuyor.")
        return
    
    library.list_books()
    
    isbn = input("\nSilmek istediğiniz kitabın ISBN numarasını girin: ").strip()
    
    if not isbn:
        print("Hata: ISBN numarası boş olamaz.")
        return
    
    library.remove_book(isbn)


def list_books(library: Library):
    """Kütüphanedeki tüm kitapları listeler."""
    print("\n--- Kitap Listeleme ---")
    books = library.list_books()
    
    if books:
        print(f"\nToplam {len(books)} kitap bulunuyor.")


def search_book(library: Library):
    """ISBN ile kitap arar."""
    print("\n--- Kitap Arama ---")
    isbn = input("Aramak istediğiniz kitabın ISBN numarasını girin: ").strip()
    
    if not isbn:
        print("Hata: ISBN numarası boş olamaz.")
        return
    
    book = library.find_book(isbn)
    if book:
        print(f"\nKitap bulundu: {book}")
    else:
        print(f"ISBN {isbn} numaralı kitap bulunamadı.")


def get_user_choice() -> str:
    """Kullanıcıdan menü seçimi alır."""
    try:
        choice = input("\nSeçiminizi yapın (1-5): ").strip()
        return choice
    except KeyboardInterrupt:
        print("\n\nProgram kullanıcı tarafından sonlandırıldı.")
        return "5"
    except EOFError:
        return "5"


def main():
    """Ana program döngüsü."""
    print("Kütüphane Yönetim Sistemi başlatılıyor...")
    
    # Library nesnesini oluştur
    library = Library("library.json")
    
    print(f"Sistem hazır! Mevcut kitap sayısı: {library.get_book_count()}")
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        try:
            if choice == "1":
                add_book(library)
            elif choice == "2":
                remove_book(library)
            elif choice == "3":
                list_books(library)
            elif choice == "4":
                search_book(library)
            elif choice == "5":
                print("\nKütüphane Yönetim Sistemi kapatılıyor...")
                print("Tüm veriler kaydedildi. İyi günler!")
                break
            else:
                print("\nHata: Geçersiz seçim! Lütfen 1-5 arasında bir sayı girin.")
        
        except Exception as e:
            print(f"\nBeklenmeyen bir hata oluştu: {e}")
            print("Program devam ediyor...")
        
        # Kullanıcının devam etmek için bir tuşa basmasını bekle
        if choice != "5":
            input("\nDevam etmek için Enter tuşuna basın...")


if __name__ == "__main__":
    main()