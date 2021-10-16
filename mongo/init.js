db.createCollection('history');

// sample stock
db.history.insertMany([
  {
    name: "itub4",
    price: 24.80,
    date: new Date().toISOString()
  }
]);
