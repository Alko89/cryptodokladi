// vue.config.js
var path = require('path')

function resolve (dir) {
    return path.join(__dirname, dir)
}

module.exports = {
    configureWebpack: {
        resolve: {
            alias: {
              '@': resolve('cryptodokladi/static/src')
            }
        }
    },
    lintOnSave: false,

    pages: {
        index: {
          // entry for the page
          entry: 'cryptodokladi/static/src/main.js'
        }
    },
    outputDir: 'cryptodokladi/static/dist/',
    indexPath: resolve('cryptodokladi/templates/index.html'),

    baseUrl: '/static/dist/',

    devServer: {
        // headers: { 'Access-Control-Allow-Origin': '*' }
    }
}
