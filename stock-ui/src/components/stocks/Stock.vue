<template>
  <v-flex class="px-1 py-1" xs12 md6 lg4>
    <v-card class="green darken-2 white--text">
      <v-card-title class="headline">
        <strong>
          {{ stock.name }}
          <small>(Price: {{ stock.price | currency }} | Total: {{ (stock.price * amount) | currency }})</small>
        </strong>
      </v-card-title>
    </v-card>
    <v-card>
      <v-container fill-height>
        <v-text-field
          label="Amount"
          type="number"
          min="0"
          :error="!Number.isInteger(amount) || insufficientBalance"
          v-model.number="amount"
        />
        <v-btn class="green darken-2 white--text" :disabled="disableButton" @click="buyStock">Buy</v-btn>
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
    insufficientBalance() {
      return (this.stock.price * this.amount) > this.balance
    }
  },
  methods: {
    buyStock() {
      if (this.invalidAmount) {
        this.$notify({
          group: 'notification',
          type: 'error',
          title: 'Error',
          text: 'Invalid amount!'
        });
        return;
      }
      if (this.insufficientBalance) {
        this.$notify({
          group: 'notification',
          type: 'error',
          title: 'Error',
          text: 'Insufficient balance!'
        });
        return;
      }
      const order = {
        stockId: this.stock.id,
        stockName: this.stock.name,
        stockPrice: this.stock.price,
        amount: this.amount
      }
      // call stocks' store buy action
      this.$store.dispatch('buyStock', order)
      // after success
      this.amount = 0;
    }
  }
}
</script>

<style>

</style>