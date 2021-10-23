import { getLastStocksByCountry } from '../../services/stocks'

const INITIAL_COUNTRY = 'br'
const INITIAL_STOCKS = {
  'br': [],
  'us': [],
};

const setCountryOnStorage = (country) => {
  sessionStorage.setItem('country', country)
}

const getCountryFromStorage = () => {
  const country = sessionStorage.getItem('country')
  return (country === undefined || country === null) ? INITIAL_COUNTRY : country
}

export default  {
  state: {
    stocks: INITIAL_STOCKS,
    country: getCountryFromStorage()
  },
  mutations: {
    setStocks(state, stocks) {
      const initialStocks = INITIAL_STOCKS;
      initialStocks[state.country] = stocks;
      state.stocks = initialStocks
    },
    randomizeStocks(state) {
      const stocks = state.stocks[state.country].map(stock => ({
        ...stock,
        price: parseFloat((stock.price * (1 + Math.random() - 0.45)).toFixed(2))
      }))
      const initialStocks = INITIAL_STOCKS;
      initialStocks[state.country] = stocks;
      state.stocks = initialStocks
    },
    setCountry(state, country) {
      if (country !== state.country) {
        state.country = country
        setCountryOnStorage(country)
        this.dispatch('initStocks')
      }
    }
  },
  actions: {
    buyStock({ commit }, order) {
      // commit portfolio's mutation buyStock
      commit('buyStock', order)
    },
    async initStocks(context) {
      const stocks = await getLastStocksByCountry(context.state.country);
      context.commit('setStocks', stocks)
    },
    randomizeStocks({ commit }) {
      commit('randomizeStocks')
    },
    setCountry({ commit }, country) {
      commit('setCountry', country)
    }
  },
  getters: {
    stocks(state) {
      return state.stocks[state.country]
    },
    country(state) {
      return state.country
    },
  }
}