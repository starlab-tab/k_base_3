import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import surf from './utils/surf/api'
import VuetifyDialog from 'vuetify-dialog'
import 'vuetify-dialog/dist/vuetify-dialog.css'
import { VueMasonryPlugin } from 'vue-masonry'
import filters from './plugins/filters.js'

Vue.prototype.$surf = surf

Vue.use(VuetifyDialog, {
    context: {
        vuetify
    }
})

Vue.use(VueMasonryPlugin)

Object.keys(filters).forEach(k => Vue.filter(k, filters[k]))

Vue.config.productionTip = false

const vue = new Vue({
    router,
    vuetify,
    render: h => h(App)
}).$mount('#app')

export default vue