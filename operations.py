"""
operations.py - Các chức năng nghiệp vụ: thêm, hiển thị, tìm kiếm sách
"""

from models import Book, load_books, save_books, get_next_id


# ──────────────────────────────────────────────
# THÊM SÁCH
# ──────────────────────────────────────────────

def add_book() -> None:
    """Nhập thông tin từ người dùng và thêm sách mới vào danh sách."""
    print("\n" + "─" * 45)
    print("  📚  THÊM SÁCH MỚI")
    print("─" * 45)

    title = _input_required("  Tên sách  : ")
    author = _input_required("  Tác giả   : ")
    year = _input_int("  Năm xuất bản (VD: 2023): ", 1000, 2100)
    genre = _input_required("  Thể loại  : ")
    price = _input_float("  Giá (VNĐ) : ")
    quantity = _input_int("  Số lượng  : ", 0, 99999)

    books = load_books()
    new_book = Book(
        book_id=get_next_id(books),
        title=title,
        author=author,
        year=year,
        genre=genre,
        price=price,
        quantity=quantity,
    )
    books.append(new_book)
    save_books(books)

    print(f"\n  ✅  Đã thêm sách «{title}» (ID: {new_book.book_id}) thành công!")


# ──────────────────────────────────────────────
# HIỂN THỊ SÁCH
# ──────────────────────────────────────────────

def display_all_books() -> None:
    """Hiển thị toàn bộ danh sách sách."""
    books = load_books()
    print("\n" + "─" * 45)
    print("  📖  DANH SÁCH SÁCH")
    print("─" * 45)

    if not books:
        print("  (Chưa có sách nào trong hệ thống.)")
        return

    _print_table(books)
    print(f"\n  Tổng cộng: {len(books)} cuốn sách.")


def display_book_detail(book_id: int) -> None:
    """Hiển thị chi tiết một cuốn sách theo ID."""
    books = load_books()
    book = _find_by_id(books, book_id)
    if book:
        print("\n" + "─" * 45)
        print("  📗  CHI TIẾT SÁCH")
        print("─" * 45)
        print(book)
    else:
        print(f"\n  ❌  Không tìm thấy sách với ID = {book_id}.")


# ──────────────────────────────────────────────
# TÌM KIẾM SÁCH
# ──────────────────────────────────────────────

def search_books() -> None:
    """Menu tìm kiếm nhiều tiêu chí."""
    print("\n" + "─" * 45)
    print("  🔍  TÌM KIẾM SÁCH")
    print("─" * 45)
    print("  1. Tìm theo tên sách")
    print("  2. Tìm theo tác giả")
    print("  3. Tìm theo thể loại")
    print("  4. Tìm theo năm xuất bản")
    print("  5. Tìm theo khoảng giá")
    print("─" * 45)

    choice = input("  Chọn tiêu chí (1-5): ").strip()

    books = load_books()
    results: list[Book] = []

    if choice == "1":
        keyword = _input_required("  Nhập tên (hoặc một phần tên): ").lower()
        results = [b for b in books if keyword in b.title.lower()]

    elif choice == "2":
        keyword = _input_required("  Nhập tên tác giả: ").lower()
        results = [b for b in books if keyword in b.author.lower()]

    elif choice == "3":
        keyword = _input_required("  Nhập thể loại: ").lower()
        results = [b for b in books if keyword in b.genre.lower()]

    elif choice == "4":
        year = _input_int("  Nhập năm xuất bản: ", 1000, 2100)
        results = [b for b in books if b.year == year]

    elif choice == "5":
        min_p = _input_float("  Giá tối thiểu (VNĐ): ")
        max_p = _input_float("  Giá tối đa   (VNĐ): ")
        results = [b for b in books if min_p <= b.price <= max_p]

    else:
        print("  ⚠  Lựa chọn không hợp lệ.")
        return

    print("\n" + "─" * 45)
    if results:
        print(f"  Tìm thấy {len(results)} kết quả:")
        _print_table(results)
    else:
        print("  Không tìm thấy sách phù hợp.")


# ──────────────────────────────────────────────
# HÀM HỖ TRỢ NỘI BỘ
# ──────────────────────────────────────────────

def _input_required(prompt: str) -> str:
    """Nhập chuỗi không được để trống."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("  ⚠  Không được để trống, vui lòng nhập lại.")


def _input_int(prompt: str, min_val: int = 0, max_val: int = 10**9) -> int:
    """Nhập số nguyên hợp lệ trong khoảng [min_val, max_val]."""
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val <= val <= max_val:
                return val
            print(f"  ⚠  Vui lòng nhập số từ {min_val} đến {max_val}.")
        except ValueError:
            print("  ⚠  Giá trị không hợp lệ, vui lòng nhập lại.")


def _input_float(prompt: str) -> float:
    """Nhập số thực không âm."""
    while True:
        try:
            val = float(input(prompt).strip().replace(",", ""))
            if val >= 0:
                return val
            print("  ⚠  Giá trị phải >= 0.")
        except ValueError:
            print("  ⚠  Giá trị không hợp lệ, vui lòng nhập lại.")


def _find_by_id(books: list[Book], book_id: int):
    """Trả về Book có book_id khớp, hoặc None."""
    return next((b for b in books if b.book_id == book_id), None)


def _print_table(books: list[Book]) -> None:
    """In danh sách sách dạng bảng."""
    header = f"  {'ID':>4}  {'Tên sách':<30}  {'Tác giả':<20}  {'Năm':>4}  {'Giá (VNĐ)':>12}  {'SL':>4}"
    sep = "  " + "─" * (len(header) - 2)
    print(sep)
    print(header)
    print(sep)
    for b in books:
        row = (
            f"  {b.book_id:>4}  {b.title[:30]:<30}  "
            f"{b.author[:20]:<20}  {b.year:>4}  "
            f"{b.price:>12,.0f}  {b.quantity:>4}"
        )
        print(row)
    print(sep)


