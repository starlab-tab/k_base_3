import Vue from 'vue'

import forge from 'node-forge'; 

const forgePlugin = {
    install(Vue) {
        Vue.prototype.$forge = forge;
    }
}
Vue.use(forgePlugin);

export default forgePlugin