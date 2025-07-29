const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

let dealerships = [ { id: 1, name: "Best Dealz", city: "El Paso", state: "Texas", st: "TX", address: "123 Main St", zip: "79901" }, { id: 2, name: "Honest Cars", city: "Topeka", state: "Kansas", st: "KS", address: "456 Oak Ave", zip: "66603" }, { id: 3, name: "Scranton Motors", city: "Scranton", state: "Pennsylvania", st: "PA", address: "789 Pine Ln", zip: "18503" }, ];
let reviews = [ { id: 1, dealerId: 1, name: "John Doe", review: "Great service!", purchase: true, purchase_date: "2024-01-15" }, { id: 2, dealerId: 1, name: "Jane Smith", review: "Friendly staff.", purchase: false }, { id: 3, dealerId: 2, name: "Sam Wilson", review: "Found the perfect car in Kansas.", purchase: true, purchase_date: "2024-02-20" }, ];

app.get('/api/dealership', (req, res) => {
    const { state, id } = req.query;
    let results = dealerships;
    if (id) results = dealerships.filter(d => d.id == id);
    else if (state) results = dealerships.filter(d => d.st == state);
    if (results.length > 0) res.json(results);
    else res.status(404).send("Not Found");
});

app.get('/api/review', (req, res) => {
    const { dealerId } = req.query;
    let results = reviews;
    if (dealerId) results = reviews.filter(r => r.dealerId == dealerId);
    if (results.length > 0) res.json(results);
    else res.status(404).send("Not Found");
});

app.post('/api/review', (req, res) => {
    const newReview = req.body;
    newReview.id = reviews.length + 1;
    reviews.push(newReview);
    res.status(201).json(newReview);
});

app.listen(port, () => {
    console.log(`Server Express berjalan di http://localhost:${port}`);
});