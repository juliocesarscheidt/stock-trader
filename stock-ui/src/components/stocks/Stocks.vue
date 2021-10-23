<template>
  <v-layout row wrap>
    <template v-if="stocks.length > 0">
      <Stock
        v-for="stock in stocks"
        :key="stock.id"
        :stock="stock"
      />
    </template>
    <template v-else>
      <span class="grey--text text--darken-2">
        Any stock found
      </span>
    </template>
  </v-layout>
</template>

<script>
import { mapGetters } from 'vuex'
import Stock from './Stock'

export default {
  components: {
    Stock
  },
  computed: {
    ...mapGetters(['stocks'])
  },
  created() {
    this.$store.dispatch('initStocks')
  }
}
</script>

<style>

</style>