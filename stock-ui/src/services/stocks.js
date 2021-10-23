import axios from 'axios'

const getLastStocksByCountry = async (country='br') => {
  return axios
    .get(`/api/v1/stocks/${country}/last`)
    .then((response) => {
      if (!response.data.data) {
        return null
      }
      const { data } = response.data
      return data.map((stock) => ({
        id: stock.id,
        name: stock.name,
        country: stock.country,
        price: stock.price
      }))
    });
}

const getLastStockByCountryAndName = async (country, name) => {
  return axios
    .get(`/api/v1/stocks/${country}/last/${name}`)
    .then((response) => {
      if (!response.data.data) {
        return null
      }
      const { data } = response.data
      return {
        id: data.id,
        name: data.name,
        country: data.country,
        price: data.price
      }
    });
}

export {
  getLastStockByCountryAndName,
  getLastStocksByCountry
}
