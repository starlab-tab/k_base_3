import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import '@mdi/font/css/materialdesignicons.css'

Vue.use(Vuetify);

export default new Vuetify({
    icons: {
        iconfont: 'mdi',
    },
    theme: {
        themes: {
            light: {
                primary: '#2c586d',
                secondary: '#fbd300',
                BlogPrimary: '#367bf0',
                BlogSecondary: '#FFFFFF',
                SecPrimary: '#367bf0',
                SecSecondary: '#FFFFFF',
            },
        },
    },
});
