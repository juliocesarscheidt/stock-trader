import { getStocks } from '../../services/stocks'

const setStocksOnStorage = (stocks) => {
  sessionStorage.setItem('stocks', JSON.stringify(stocks))
}

const getStocksFromStorage = () => {
  const storedStocks = sessionStorage.getItem('stocks')
  return storedStocks ? JSON.parse(storedStocks) : []
}

export default  {
  state: {
    stocks: []
  },
  mutations: {
    setStocks(state, stocks) {
      state.stocks = stocks
      setStocksOnStorage(state.stocks)
    },
    randomizeStocks(state) {
      const stocks = state.stocks.map(stock => ({
        ...stock,
        price: Math.round(stock.price * (1 + Math.random() - 0.45))
      }))
      state.stocks = stocks
      setStocksOnStorage(state.stocks)
    }
  },
  actions: {
    buyStock({ commit }, order) {
      // commit portfolio's mutation buyStock
      commit('buyStock', order)
    },
    async initStocks({ commit }) {
      // const stocks = await getStocks();
      // commit('setStocks', stocks)
      const storedStocks = getStocksFromStorage()
      if (storedStocks.length) {
        commit('setStocks', storedStocks)
      } else {
        const stocks = await getStocks();
        commit('setStocks', stocks)
      }
    },
    randomizeStocks({ commit }) {
      commit('randomizeStocks')
    }
  },
  getters: {
    stocks(state) {
      return state.stocks
    }
  }
}