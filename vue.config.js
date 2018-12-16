// vue.config.js
var path = require('path')

function resolve (dir) {
    return path.join(__dirname, dir)
}

module.exports = {
    pages: {
        index: {
          // entry for the page
          entry: 'cryptodokladi/static/src/main.js'
        }
    },
    indexPath: resolve('cryptodokladi/templates/index.html'),
    outputDir: 'cryptodokladi/static/dist/',
    baseUrl: '/static/dist/',

    configureWebpack: {
        resolve: {
            alias: {
                '@': resolve('cryptodokladi/static/src')
            }
        }
    },

    devServer: {
        proxy: 'http://localhost:6543',
        headers: {
            'Access-Control-Allow-Origin': '*',
        },
    },
}
