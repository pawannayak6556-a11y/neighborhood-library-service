import grpc
from concurrent import futures
import library_pb2
import library_pb2_grpc
from db import get_conn
from config import GRPC_PORT

class LibraryService(library_pb2_grpc.LibraryServiceServicer):

    def CreateBook(self, request, context):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO books (title, author, total_copies, available_copies)
            VALUES (%s, %s, %s, %s) RETURNING id
        """, (request.title, request.author, request.copies, request.copies))
        book_id = cur.fetchone()[0]
        conn.commit()
        return library_pb2.Book(
            id=book_id,
            title=request.title,
            author=request.author,
            available_copies=request.copies
        )

    def ListBooks(self, request, context):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, title, author, available_copies FROM books")
        books = [
            library_pb2.Book(
                id=r[0], title=r[1], author=r[2], available_copies=r[3]
            ) for r in cur.fetchall()
        ]
        return library_pb2.BookList(books=books)

    def BorrowBook(self, request, context):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT available_copies FROM books WHERE id=%s",
            (request.book_id,)
        )
        row = cur.fetchone()
        if not row or row[0] <= 0:
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, "Book not available")

        cur.execute("""
            INSERT INTO loans (book_id, member_id)
            VALUES (%s, %s) RETURNING id
        """, (request.book_id, request.member_id))

        cur.execute("""
            UPDATE books SET available_copies = available_copies - 1
            WHERE id=%s
        """, (request.book_id,))
        conn.commit()

        return library_pb2.Loan(
            book_id=request.book_id,
            member_id=request.member_id
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    library_pb2_grpc.add_LibraryServiceServicer_to_server(
        LibraryService(), server
    )
    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    server.start()
    print(f"gRPC server running on port {GRPC_PORT}")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
