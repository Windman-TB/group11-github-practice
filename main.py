"""
main.py - Điểm khởi chạy chương trình, hiển thị menu chính
"""

import sys
import os

# Thêm thư mục hiện tại vào sys.path để import module cùng cấp
sys.path.insert(0, os.path.dirname(__file__))

from operations import (
    add_book,
    display_all_books,
    display_book_detail,
    search_books,
)
from models import load_books, save_books


BANNER = r"""
  ╔══════════════════════════════════════════╗
  ║   📚  HỆ THỐNG QUẢN LÝ SÁCH  📚         ║
  ║        Book Management System            ║
  ╚══════════════════════════════════════════╝
"""

MENU = """
  ┌──────────────────────────────────────────┐
  │  1.  Thêm sách mới                       │
  │  2.  Hiển thị tất cả sách                │
  │  3.  Xem chi tiết sách (theo ID)         │
  │  4.  Tìm kiếm sách                       │
  │  5.  Xóa sách (theo ID)                  │
  │  6.  Cập nhật số lượng sách              │
  │  0.  Thoát                               │
  └──────────────────────────────────────────┘
"""


def delete_book() -> None:
    """Xóa sách theo ID."""
    books = load_books()
    if not books:
        print("\n  (Danh sách trống, không có gì để xóa.)")
        return

    try:
        book_id = int(input("\n  Nhập ID sách cần xóa: ").strip())
    except ValueError:
        print("  ⚠  ID không hợp lệ.")
        return

    book = next((b for b in books if b.book_id == book_id), None)
    if not book:
        print(f"\n  ❌  Không tìm thấy sách với ID = {book_id}.")
        return

    confirm = input(f"\n  Bạn chắc chắn muốn xóa «{book.title}»? (y/N): ").strip().lower()
    if confirm == "y":
        books = [b for b in books if b.book_id != book_id]
        save_books(books)
        print(f"\n  ✅  Đã xóa sách «{book.title}» thành công!")
    else:
        print("  ↩  Đã hủy thao tác xóa.")


def update_quantity() -> None:
    """Cập nhật số lượng sách theo ID."""
    books = load_books()
    try:
        book_id = int(input("\n  Nhập ID sách cần cập nhật số lượng: ").strip())
    except ValueError:
        print("  ⚠  ID không hợp lệ.")
        return

    book = next((b for b in books if b.book_id == book_id), None)
    if not book:
        print(f"\n  ❌  Không tìm thấy sách với ID = {book_id}.")
        return

    print(f"\n  Sách: «{book.title}» — Số lượng hiện tại: {book.quantity}")
    try:
        new_qty = int(input("  Nhập số lượng mới: ").strip())
        if new_qty < 0:
            print("  ⚠  Số lượng không thể âm.")
            return
    except ValueError:
        print("  ⚠  Giá trị không hợp lệ.")
        return

    book.quantity = new_qty
    save_books(books)
    print(f"\n  ✅  Đã cập nhật số lượng sách «{book.title}» thành {new_qty}!")


def seed_sample_data() -> None:
    """Khởi tạo dữ liệu mẫu nếu chưa có sách nào."""
    from models import Book, get_next_id
    books = load_books()
    if books:
        return  # đã có dữ liệu, không ghi đè

    samples = [
        Book(1, "Đắc Nhân Tâm", "Dale Carnegie", 1936, "Kỹ năng sống", 89000, 50),
        Book(2, "Nhà Giả Kim", "Paulo Coelho", 1988, "Tiểu thuyết", 75000, 30),
        Book(3, "Tư Duy Nhanh Và Chậm", "Daniel Kahneman", 2011, "Tâm lý học", 120000, 20),
        Book(4, "Sapiens: Lược Sử Loài Người", "Yuval Noah Harari", 2011, "Lịch sử", 145000, 15),
        Book(5, "Clean Code", "Robert C. Martin", 2008, "Lập trình", 250000, 10),
        Book(6, "The Pragmatic Programmer", "Andrew Hunt & David Thomas", 1999, "Lập trình", 220000, 8),
        Book(7,"Lập trình Python để mọi người", "Al Swweigart", 2015, 'Lập trình',180000,25),
    ]
    save_books(samples)
    print("  ℹ  Đã nạp 7 cuốn sách mẫu vào hệ thống.\n")


def main() -> None:
    print(BANNER)
    seed_sample_data()

    actions = {
        "1": add_book,
        "2": display_all_books,
        "4": search_books,
        "5": delete_book,
        "6": update_quantity,
    }

    while True:
        print(MENU)
        choice = input("  👉  Nhập lựa chọn của bạn: ").strip()

        if choice == "0":
            print("\n  👋  Cảm ơn đã sử dụng! Tạm biệt.\n")
            break
        elif choice == "3":
            try:
                book_id = int(input("\n  Nhập ID sách cần xem: ").strip())
                display_book_detail(book_id)
            except ValueError:
                print("  ⚠  ID không hợp lệ.")
        elif choice in actions:
            actions[choice]()
        else:
            print("\n  ⚠  Lựa chọn không hợp lệ, vui lòng chọn lại (0-6).")


if __name__ == "__main__":
    main()


#Toi la phong 