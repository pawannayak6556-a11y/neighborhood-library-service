const express = require("express");
const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");

const app = express();
app.use(express.json());

const protoDef = protoLoader.loadSync("proto/library.proto");
const proto = grpc.loadPackageDefinition(protoDef).library;

const client = new proto.LibraryService(
  "localhost:50051",
  grpc.credentials.createInsecure()
);

app.get("/books", (_, res) => {
  client.ListBooks({}, (_, response) => res.json(response.books));
});

app.post("/books", (req, res) => {
  client.CreateBook(req.body, (_, response) => res.json(response));
});

app.post("/borrow", (req, res) => {
  client.BorrowBook(req.body, (_, response) => res.json(response));
});

app.listen(3001, () => console.log("Gateway running on 3001"));
