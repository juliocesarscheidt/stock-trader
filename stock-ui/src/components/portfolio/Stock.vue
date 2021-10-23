<template>
  <v-flex class="px-1 py-1" xs12 md6 lg4>
    <v-card class="blue darken-2 white--text">
      <v-card-title class="headline">
        <strong>
          {{ stock.name }}
          <small>(Price: {{ stock.price | currency }} | Amount: {{ stock.amount }})</small>
        </strong>
      </v-card-title>
    </v-card>
    <v-card>
      <v-container fill-height>
        <v-text-field
          label="Amount"
          type="number"
          min="0"
          :error="!Number.isInteger(amount) || insufficientAmount"
          v-model.number="amount"
        />
        <v-btn class="blue darken-2 white--text" :disabled="disableButton" @click="sellStock">Sell</v-btn>
      </v-container>
    </v-card>
  </v-flex>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  props: {
    stock: Object
  },
  data() {
    return {
      amount: 0
    }
  },
  computed: {
    ...mapGetters(['balance']),
    disableButton() {
      return this.amount <= 0 || !Number.isInteger(this.amount);
    },
    invalidAmount() {
      return !this.amount || this.amount <= 0
    },
    insufficientAmount() {
      return this.amount > this.stock.amount
    }
  },
  methods: {
    sellStock() {
      if (this.invalidAmount) {
        this.$notify({
          group: 'notification',
          type: 'error',
          title: 'Error',
          text: 'Invalid amount!'
        });
        return;
      }
      if (this.insufficientAmount) {
        this.$notify({
          group: 'notification',
          type: 'error',
          title: 'Error',
          text: 'Insufficient amount!'
        });
        return;
      }
      const order = {
        stockId: this.stock.id,
        stockName: this.stock.name,
        stockPrice: this.stock.price,
        amount: this.amount
      }
      // call stocks' store sell action
      this.$store.dispatch('sellStock', order)
      // after success
      this.amount = 0;
    }
  }
}
</script>

<style>

</style>