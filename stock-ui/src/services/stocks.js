const randomBetweeen = (min, max) => Math.round(Math.random() * (max - min + 1) + min)

const getStocks = () => {
  const stocks = [
    { id: 1, name: 'BMW', price: randomBetweeen(75, 250) },
    { id: 2, name: 'Google', price: randomBetweeen(75, 250) },
    { id: 3, name: 'Apple', price: randomBetweeen(75, 250) },
    { id: 4, name: 'Tesla', price: randomBetweeen(75, 250) }
  ]

  return new Promise((resolve) => resolve(stocks))
}

export {
  getStocks
}
