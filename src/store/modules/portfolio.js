const INITIAL_BALANCE = 1000

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
  return storedStocksPortfolio ? JSON.parse(storedStocksPortfolio) : []
}

export default  {
  state: {
    balance: getBalanceFromStorage(),
    stocks: getStocksPortfolioFromStorage()
  },
  mutations: {
    buyStock(state, { stockId, stockPrice, amount }) {
      const price = parseFloat(stockPrice * amount)
      // cannot buy more stocks than those we can afford
      if (price > state.balance) return
      const record = state.stocks.find(({ id }) => id === stockId)
      if (record) {
        // increase amount
        const newAmount = (record.amount + amount)
        Reflect.set(record, 'amount', newAmount)
      } else {
        state.stocks.push({
          id: stockId,
          amount: amount
        })
      }
      // persist new stocks portfolio
      setStocksPortfolioOnStorage(this.getters.stocksPortfolio)
      // decrease balance
      state.balance -= price
      setBalanceOnStorage(state.balance)
    },
    sellStock(state, { stockId, stockPrice, amount }) {
      const price = parseFloat(stockPrice * amount)
      const record = state.stocks.find(({ id }) => id === stockId)
      if (!record) return
      // cannot sell more stocks than the amount we have
      if (amount > record.amount) return
      if (record.amount > amount) {
        // decrease amount
        const newAmount = (record.amount - amount)
        Reflect.set(record, 'amount', newAmount)
      } else {
        state.stocks.splice(state.stocks.indexOf(record), 1)
      }
      // persist new stocks portfolio
      setStocksPortfolioOnStorage(this.getters.stocksPortfolio)
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
      const stocks = state.stocks.map(stock => {
        // accessing the "stocks" getter from stocks module to recover all stocks
        const record = getters.stocks.find(({ id }) => id === stock.id)
        if (record) {
          return {
            id: stock.id,
            amount: stock.amount,
            name: record.name,
            price: record.price,
          }
        }
      })

      return stocks
    },
    balance(state) {
      return state.balance
    }
  }
}