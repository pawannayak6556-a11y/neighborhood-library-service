import { useEffect, useState } from "react";
import { getBooks, createBook } from "./api/libraryApi";

function App() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    getBooks().then(setBooks);
  }, []);

  return (
    <div>
      <h2>Library</h2>
      <button onClick={() =>
        createBook({ title: "1984", author: "Orwell", copies: 2 })
          .then(() => getBooks().then(setBooks))
      }>
        Add Book
      </button>

      <ul>
        {books.map(b => (
          <li key={b.id}>{b.title} ({b.available_copies})</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
