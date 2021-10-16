import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/store'
import { currency } from './filters/filters'
import './plugins/vuetify'
import './plugins/notification'

Vue.config.productionTip = false
Vue.filter('currency', currency)

new Vue({
  router,
  store,
	render: h => h(App),
}).$mount('#app')
