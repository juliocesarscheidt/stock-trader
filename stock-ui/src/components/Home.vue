<template>
  <div>
    <h1 class="display-3 font-weight-light mb-4">Deal and Consult Stocks</h1>
    <!-- <v-sheet :elevation="6" class="py-2 px-2 primary">
      <v-icon class="white--text mx-2">info</v-icon>
      <span class="headline white--text font-weight-light">
        You can Save & Load Data
      </span>
    </v-sheet> -->
    <v-sheet :elevation="6" class="py-2 px-2 my-2 success">
      <v-icon class="white--text mx-2">info</v-icon>
      <span class="headline white--text font-weight-light">
        Click on "Finish Day" to start a new day for trading
      </span>
    </v-sheet>
    <v-divider class="my-4"></v-divider>
    <p class="display-1">
      <strong>Balance: </strong>{{ balance | currency }}
    </p>

    <v-card>
      <v-container fill-height>
        <v-text-field
          label="Search Stock"
          type="string"
          v-model.trim="stockName"
        />
        <v-btn class="blue darken-2 white--text" :disabled="disableButton" @click="searchStock">Search</v-btn>
      </v-container>
    </v-card>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getLastStockByCountryAndName, getLastStocksByCountry } from '../services/stocks'

export default {
  computed: {
    ...mapGetters(['balance', 'country']),
    disableButton() {
      return !this.stockName || this.searchingStock;
    },
  },
  data() {
    return {
      stockName: '',
      searchStockTimeout: null,
      searchingStock: false,
      searchRetries: 0,
      searchMaxRetries: 3
    }
  },
  methods: {
    clearTimer() {
      this.searchRetries = 0
      clearTimeout(this.searchStockTimeout)
      this.searchStockTimeout = null
    },
    async searchStock() {
      if (!this.stockName) {
        this.$notify({
          group: 'notification',
          type: 'error',
          title: 'Error',
          text: 'Invalid stock name!'
        });
        return
      }
      this.searchingStock = true

      const stock = await getLastStockByCountryAndName(this.country, this.stockName)
      if (stock) {
        const stocks = await getLastStocksByCountry(this.country)

        const existingStock = stocks.find(s => s.name === stock.name)
        if (existingStock) {
          stocks.splice(stocks.indexOf(existingStock), 1, stock)
        } else {
          stocks.push(stock)
        }
        this.$notify({
          group: 'notification',
          type: 'success',
          title: 'Success',
          text: 'The stock was found!'
        });

        this.$store.commit('setStocks', stocks)
        this.$router.push({name: 'Stocks'})

        this.searchingStock = false
      } else {
        if (this.searchRetries >= this.searchMaxRetries) {
          this.$notify({
            group: 'notification',
            type: 'error',
            title: 'Error',
            text: 'The stock was not found!'
          });
          this.clearTimer()
          this.searchingStock = false
          return
        }
        this.$notify({
          group: 'notification',
          type: 'info',
          title: 'Info',
          text: 'The stock is being consulted...'
        });

        const vm = this
        this.searchStockTimeout = setTimeout(() => {
          vm.searchRetries += 1
          vm.searchStock()
        }, (3 * 1000));
      }
    }
  },
  beforeDestroy() {
    this.clearTimer()
  }
}
</script>

<style>

</style>