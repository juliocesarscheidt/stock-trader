import axios from 'axios'
// const apiUri = process.env.VUE_APP_API_URI

const getLastStockByName = async (name) => {
  return axios
    .get(`/api/v1/stocks/last/${name}`)
    .then((response) => {
      if (!response.data.data) {
        return null
      }
      const { data } = response.data
      return {
        id: data.id,
        name: data.name,
        price: data.price
      }
    });
}

const getLastStocks = async () => {
  return axios
    .get('/api/v1/stocks/last')
    .then((response) => {
      if (!response.data.data) {
        return null
      }
      const { data } = response.data
      return data.map((stock) => ({
        id: stock.id,
        name: stock.name,
        price: stock.price
      }))
    });
}

export {
  getLastStockByName,
  getLastStocks
}
