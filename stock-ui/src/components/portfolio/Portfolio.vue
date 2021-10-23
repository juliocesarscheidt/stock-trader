<template>
  <v-layout row wrap>
    <template v-if="stocksPortfolio.length > 0">
      <Stock
        v-for="stock in stocksPortfolio"
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
    ...mapGetters(['stocksPortfolio'])
  }
}
</script>

<style>

</style>