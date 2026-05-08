"""
models.py - Định nghĩa lớp Book và quản lý dữ liệu (lưu/đọc file JSON)
"""

import json
import os
from datetime import datetime


DATA_FILE = "books_data.json"


class Book:
    """Lớp đại diện cho một cuốn sách."""

    def __init__(self, book_id: int, title: str, author: str, year: int,
                 genre: str, price: float, quantity: int = 1):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.price = price
        self.quantity = quantity
        self.added_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        """Chuyển đối tượng Book thành dictionary để lưu JSON."""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre,
            "price": self.price,
            "quantity": self.quantity,
            "added_at": self.added_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """Tạo đối tượng Book từ dictionary."""
        book = cls(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            genre=data["genre"],
            price=data["price"],
            quantity=data.get("quantity", 1),
        )
        book.added_at = data.get("added_at", "")
        return book

    def __str__(self) -> str:
        return (
            f"  ID      : {self.book_id}\n"
            f"  Tên sách: {self.title}\n"
            f"  Tác giả : {self.author}\n"
            f"  Năm XB  : {self.year}\n"
            f"  Thể loại: {self.genre}\n"
            f"  Giá     : {self.price:,.0f} VNĐ\n"
            f"  Số lượng: {self.quantity}\n"
            f"  Ngày thêm: {self.added_at}"
        )


# ──────────────────────────────────────────────
# Hàm đọc / ghi dữ liệu
# ──────────────────────────────────────────────

def load_books() -> list[Book]:
    """Đọc danh sách sách từ file JSON. Trả về list rỗng nếu file chưa tồn tại."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Book.from_dict(item) for item in data]
    except (json.JSONDecodeError, KeyError):
        print("⚠  File dữ liệu bị lỗi, khởi tạo danh sách trống.")
        return []


def save_books(books: list[Book]) -> None:
    """Lưu danh sách sách vào file JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([b.to_dict() for b in books], f, ensure_ascii=False, indent=2)


def get_next_id(books: list[Book]) -> int:
    """Tạo ID tự tăng cho sách mới."""
    return max((b.book_id for b in books), default=0) + 1
