const currency = value => `US$ ${parseFloat(value).toFixed(2).toLocaleString()}`

export {
  currency
}
