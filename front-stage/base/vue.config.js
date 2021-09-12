const path = require('path')
module.exports = {
    transpileDependencies: [
        'vuetify'
    ],
    devServer: {
      port: 80
    },
    pluginOptions: {
        'style-resources-loader': {
            preProcessor: 'scss',
            patterns: [
                path.resolve(__dirname, './src/assets/styles/global/_config.scss')
            ]
        }
    },
}