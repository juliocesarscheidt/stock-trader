import axios from 'axios'

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
    }).catch((err) => {
      console.error(err)
    })
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
    }).catch((err) => {
      console.error(err)
    })
}

export {
  getLastStockByName,
  getLastStocks
}
