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
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters(['balance'])
  }
}
</script>

<style>

</style>