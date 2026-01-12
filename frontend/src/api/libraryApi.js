const BASE = "http://localhost:3001";

export const getBooks = () =>
  fetch(`${BASE}/books`).then(res => res.json());

export const createBook = (data) =>
  fetch(`${BASE}/books`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
