#!/usr/bin/env python3
"""
Kütüphane Yönetim Sistemi - FastAPI Web API
Python 202 Bootcamp Bitirme Projesi

Bu modül kütüphane yönetim sisteminin web API'sini sağlar.
REST API endpoint'leri ile kitap ekleme, silme ve listeleme işlemleri yapılabilir.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
import uvicorn

from library import Library
from book import Book


# Pydantic modelleri
class BookResponse(BaseModel):
    """API'nin döndüreceği kitap verisi modeli."""
    title: str = Field(..., description="Kitabın başlığı")
    author: str = Field(..., description="Kitabın yazarı")
    isbn: str = Field(..., description="Kitabın ISBN numarası")
    
    class Config:
        schema_extra = {
            "example": {
                "title": "1984",
                "author": "George Orwell",
                "isbn": "978-0451524935"
            }
        }


class ISBNRequest(BaseModel):
    """POST isteğinde alınacak ISBN verisi modeli."""
    isbn: str = Field(..., min_length=10, max_length=17, 
                      description="Kitabın ISBN numarası (10-17 karakter)")
    
    class Config:
        schema_extra = {
            "example": {
                "isbn": "978-0451524935"
            }
        }


class MessageResponse(BaseModel):
    """API'nin döndüreceği mesaj modeli."""
    message: str = Field(..., description="İşlem sonucu mesajı")
    success: bool = Field(..., description="İşlem başarı durumu")


# FastAPI uygulaması
app = FastAPI(
    title="Kütüphane Yönetim Sistemi API",
    description="Python 202 Bootcamp bitirme projesi - Kütüphane yönetimi için REST API",
    version="1.0.0",
    contact={
        "name": "Python 202 Bootcamp Projesi",
        "url": "https://github.com/username/library-management-system",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Library instance'ı oluştur
library = Library("library.json")


@app.get("/", response_model=MessageResponse)
async def root():
    """API'nin ana endpoint'i - sistem durumu döndürür."""
    return MessageResponse(
        message=f"Kütüphane Yönetim Sistemi API'sine hoş geldiniz! "
                f"Mevcut kitap sayısı: {library.get_book_count()}",
        success=True
    )


@app.get("/books", 
         response_model=List[BookResponse],
         summary="Tüm kitapları listele",
         description="Kütüphanedeki tüm kitapların listesini JSON formatında döndürür.")
async def get_books():
    """
    Kütüphanedeki tüm kitapları listeler.
    
    Returns:
        List[BookResponse]: Kütüphanedeki tüm kitapların listesi
    """
    books = library.list_books()
    return [
        BookResponse(
            title=book.title,
            author=book.author, 
            isbn=book.isbn
        ) for book in books
    ]


@app.post("/books",
          response_model=BookResponse,
          status_code=status.HTTP_201_CREATED,
          summary="Yeni kitap ekle",
          description="ISBN numarası kullanarak Open Library API'sinden kitap bilgilerini çeker ve kütüphaneye ekler.")
async def add_book(isbn_request: ISBNRequest):
    """
    Yeni bir kitap ekler.

    Args:
        isbn_request (ISBNRequest): ISBN numarası içeren request body

    Returns:
        BookResponse: Eklenen kitabın bilgileri

    Raises:
        HTTPException: Kitap zaten mevcutsa 400, bulunamazsa 404 hatası döner.
    """
    isbn = isbn_request.isbn.strip()

    # Kitabın zaten var olup olmadığını kontrol et
    if library.find_book(isbn):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ISBN {isbn} numaralı kitap zaten kütüphanede mevcut."
        )

    # Kitabı eklemeyi dene
    new_book = library.add_book(isbn)

    if not new_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ISBN {isbn} ile Open Library'de kitap bulunamadı veya bir API hatası oluştu."
        )

    # Başarılı yanıtı döndür
    return BookResponse(
        title=new_book.title,
        author=new_book.author,
        isbn=new_book.isbn
    )


@app.delete("/books/{isbn}",
           response_model=MessageResponse,
           summary="Kitap sil",
           description="Belirtilen ISBN'e sahip kitabı kütüphaneden siler.")
async def delete_book(isbn: str):
    """
    Belirtilen ISBN'e sahip kitabı siler.
    
    Args:
        isbn (str): Silinecek kitabın ISBN numarası
        
    Returns:
        MessageResponse: İşlem sonucu mesajı
        
    Raises:
        HTTPException: Kitap bulunamazsa 404 hatası döner
    """
    isbn = isbn.strip()
    
    # Kitabın var olup olmadığını kontrol et
    book = library.find_book(isbn)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ISBN {isbn} numaralı kitap bulunamadı."
        )
    
    # Kitabı sil
    success = library.remove_book(isbn)
    
    if success:
        return MessageResponse(
            message=f"ISBN {isbn} numaralı kitap başarıyla silindi.",
            success=True
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Kitap silinirken bir hata oluştu."
        )


@app.get("/books/{isbn}",
         response_model=BookResponse,
         summary="Belirli bir kitabı getir",
         description="ISBN numarası ile belirli bir kitabın bilgilerini getirir.")
async def get_book(isbn: str):
    """
    Belirtilen ISBN'e sahip kitabı getirir.
    
    Args:
        isbn (str): Aranacak kitabın ISBN numarası
        
    Returns:
        BookResponse: Bulunan kitabın bilgileri
        
    Raises:
        HTTPException: Kitap bulunamazsa 404 hatası döner
    """
    isbn = isbn.strip()
    
    book = library.find_book(isbn)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ISBN {isbn} numaralı kitap bulunamadı."
        )
    
    return BookResponse(
        title=book.title,
        author=book.author,
        isbn=book.isbn
    )


@app.get("/stats",
         response_model=dict,
         summary="Kütüphane istatistikleri",
         description="Kütüphane hakkında genel istatistik bilgilerini döndürür.")
async def get_stats():
    """
    Kütüphane istatistiklerini döndürür.
    
    Returns:
        dict: İstatistik bilgileri
    """
    books = library.list_books()
    authors = set(book.author for book in books)
    
    return {
        "total_books": len(books),
        "total_authors": len(authors),
        "most_common_authors": list(authors)[:10] if authors else []
    }


# Uygulama çalıştırma
if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )