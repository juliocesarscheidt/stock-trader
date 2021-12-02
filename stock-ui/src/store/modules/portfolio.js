const INITIAL_BALANCE = 10000
const INITIAL_STOCKS = {
  'br': [],
  'us': [],
};

const setBalanceOnStorage = (balance) => {
  sessionStorage.setItem('balance', balance)
}

const getBalanceFromStorage = () => {
  const balance = sessionStorage.getItem('balance')
  return (balance === undefined || balance === null) ? INITIAL_BALANCE : parseFloat(balance)
}

const setStocksPortfolioOnStorage = (stocksPortfolio) => {
  sessionStorage.setItem('stocksPortfolio', JSON.stringify(stocksPortfolio))
}

const getStocksPortfolioFromStorage = () => {
  const storedStocksPortfolio = sessionStorage.getItem('stocksPortfolio')
  return storedStocksPortfolio ? JSON.parse(storedStocksPortfolio) : INITIAL_STOCKS
}

export default  {
  state: {
    balance: getBalanceFromStorage(),
    stocksPortfolio: getStocksPortfolioFromStorage()
  },
  mutations: {
    buyStock(state, { stockId, stockName, stockPrice, amount }) {
      const price = parseFloat(stockPrice * amount)
      // cannot buy more stocksPortfolio than those we can afford
      if (price > state.balance) return
      const record = state.stocksPortfolio[this.getters.country].find(s => s.name === stockName)
      if (record) {
        // increase amount
        const newAmount = (record.amount + amount)
        Reflect.set(record, 'amount', newAmount)
      } else {
        state.stocksPortfolio[this.getters.country].push({
          id: stockId,
          name: stockName,
          amount: amount
        })
      }
      // persist new stocksPortfolio portfolio
      setStocksPortfolioOnStorage(state.stocksPortfolio)
      // decrease balance
      state.balance -= price
      setBalanceOnStorage(state.balance)
    },
    sellStock(state, { stockName, stockPrice, amount }) {
      const price = parseFloat(stockPrice * amount)
      const record = state.stocksPortfolio[this.getters.country].find(s => s.name === stockName)
      if (!record) return
      // cannot sell more stocksPortfolio than the amount we have
      if (amount > record.amount) return
      if (record.amount > amount) {
        // decrease amount
        const newAmount = (record.amount - amount)
        Reflect.set(record, 'amount', newAmount)
      } else {
        state.stocksPortfolio[this.getters.country].splice(state.stocksPortfolio[this.getters.country].indexOf(record), 1)
      }
      // persist new stocksPortfolio portfolio
      setStocksPortfolioOnStorage(state.stocksPortfolio)
      // increase balance
      state.balance += price
      setBalanceOnStorage(state.balance)
    }
  },
  actions: {
    sellStock({ commit }, order) {
      commit('sellStock', order)
    }
  },
  getters: {
    stocksPortfolio(state, getters) {
      if (!state.stocksPortfolio
        || !state.stocksPortfolio[getters.country]
        || !state.stocksPortfolio[getters.country].length) {
        return [];
      }
      const allStocks = getters.stocks
      const stocks = state.stocksPortfolio[getters.country]
        .map(stock => {
          // accessing the "stocks" getter from stocks module to recover all stocks
          if (stock && stock.name) {
            const record = allStocks.find(s => s.name === stock.name)
            if (record) {
              return {
                id: record.id,
                amount: stock.amount,
                name: record.name,
                country: record.country,
                price: record.price,
              }
            }
          }
        })
        .filter(s => s && s.id !== undefined && s.id !== null)
      return stocks
    },
    balance(state) {
      return state.balance
    }
  }
}