<template>
	<v-app>
    <Header/>
    <v-content>
      <v-container>
        <transition name="slide" mode="out-in">
          <router-view></router-view>
        </transition>
      </v-container>
    </v-content>
    <notifications position="top right" group="notification" class="my-4 mx-4"/>
  </v-app>
</template>

<script>
import Header from './components/Header'

export default {
  components: {
    Header
  }
}
</script>

<style>
@keyframes slide-in {
  from {
    transform: translateX(-25px);
    opacity: 0;
  }
  to {
    transform: translateX(0px);
    opacity: 1;
  }
}

@keyframes slide-out {
  from {
    transform: translateX(0px);
    opacity: 1;
  }
  to {
    transform: translateX(-25px);
    opacity: 0;
  }
}

.slide-enter-active {
  animation: slide-in 0.25s ease;
}

.slide-leave-active {
  animation: slide-out 0.25s ease;
}
</style>

