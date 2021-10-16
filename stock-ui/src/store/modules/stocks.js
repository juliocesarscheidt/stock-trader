import { getLastStocks } from '../../services/stocks'

const setStocksOnStorage = (stocks) => {
  sessionStorage.setItem('stocks', JSON.stringify(stocks))
}

// const getLastStocksFromStorage = () => {
//   const storedStocks = sessionStorage.getItem('stocks')
//   return storedStocks ? JSON.parse(storedStocks) : []
// }

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
        price: parseFloat((stock.price * (1 + Math.random() - 0.45)).toFixed(2))
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
      const stocks = await getLastStocks();
      commit('setStocks', stocks)
      // const storedStocks = getLastStocksFromStorage()
      // if (storedStocks.length) {
      //   commit('setStocks', storedStocks)
      // } else {
      //   const stocks = await getLastStocks();
      //   commit('setStocks', stocks)
      // }
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