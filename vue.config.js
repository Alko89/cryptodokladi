// vue.config.js
var path = require('path')

const CopyWebpackPlugin = require('copy-webpack-plugin');

function resolve (dir) {
    return path.join(__dirname, dir)
}

module.exports = {
    pages: {
        index: {
          // entry for the page
          entry: 'frontend/src/main.js',
          // the source template
          template: 'frontend/public/index.html'
        }
    },
    indexPath: resolve('cryptodokladi/templates/index.html'),
    outputDir: 'cryptodokladi/static/dist/',
    baseUrl: '/static/dist/',

    configureWebpack: {
        resolve: {
            alias: {
                '@': resolve('frontend/src')
            }
        },
        // Only needed to copy favicon (https://github.com/vuejs/vue-cli/issues/2436)
        plugins: [
            new CopyWebpackPlugin([{
                from: 'frontend/public/',
                to: './',
                ignore: 'index.html'
            }])
        ],
    },

    devServer: {
        proxy: 'http://localhost:6543',
        headers: {
            'Access-Control-Allow-Origin': '*',
        },
    },
}
