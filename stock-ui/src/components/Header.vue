<template>
  <v-toolbar app>
    <v-toolbar-title class="headline text-uppercase mx-4">
      <span>Stock</span>
      <span class="font-weight-light">Trader</span>
    </v-toolbar-title>
    <v-toolbar-items>
      <v-btn flat :to="{name: 'Home'}">Home</v-btn>
      <v-btn flat :to="{name: 'Portfolio'}">Portfolio</v-btn>
      <v-btn flat :to="{name: 'Stocks'}">Stocks</v-btn>
    </v-toolbar-items>
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <v-select
        :items="countries"
        :value="country"
        @input="setCountry"
        label="Country"
        filled
        item-text="name"
        item-value="abbreviation"
        class="mx-4"
        style="max-width: 100px; white-space: nowrap;"
      >
      </v-select>
      <!-- <v-select
        v-model="country"
        :items="countries"
        filled
        item-text="name"
        item-value="abbreviation"
        style="max-width: 100px; white-space: nowrap;"
      >
      </v-select>
      <select
        v-model="country"
        label="Country"
        style="max-width: 100px; width: 100px; height: 60%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; border-bottom: #222 1px solid; outline: none; cursor: pointer;"
      >
        <option v-for="c in countries" :value="c.abbreviation" :key="c.abbreviation">
          {{ c.name}}
        </option>
      </select> -->
      <v-btn flat @click="finishDay">Finish Day</v-btn>
      <!-- <v-menu offset-y>
        <v-btn flat slot="activator">Save & Load</v-btn>
        <v-list>
          <v-list-tile>
            <v-list-tile-title>Save Data</v-list-tile-title>
          </v-list-tile>
          <v-list-tile>
            <v-list-tile-title>Load Data</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu> -->
      <v-layout align-center>
        <span class="text-uppercase grey--text text--darken-2">
          Balance: {{ balance | currency }}
        </span>
      </v-layout>
    </v-toolbar-items>
  </v-toolbar>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  computed: {
    ...mapGetters(['balance', 'country'])
  },
  data() {
    return {
      countries: [
        {
          name: 'Brazil',
          abbreviation: 'br'
        }, {
          name: 'United States',
          abbreviation: 'us'
        },
      ]
    }
  },
  methods: {
    ...mapActions(['randomizeStocks']),
    finishDay() {
      this.randomizeStocks()
    },
    setCountry(country) {
      this.$store.dispatch('setCountry', country)
    }
  }
}
</script>

<style>

</style>