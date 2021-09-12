import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import forgePlugin from './plugins/forge'
import VMdEditor from './plugins/vmdeditor'
import surf from './utils/surf/api'
import VuetifyDialog from 'vuetify-dialog'
import 'vuetify-dialog/dist/vuetify-dialog.css'
import filters from './plugins/filters.js'
import shieldPlugin from "./plugins/shield"

Vue.use(VuetifyDialog, {
    context: {
        vuetify
    }
})

Vue.use(shieldPlugin, {
    store
})

Vue.config.productionTip = false

Vue.prototype.$surf = surf

require("promise.prototype.finally").shim();

Object.keys(filters).forEach(k => Vue.filter(k, filters[k]))


let vue = new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')

export default vue
