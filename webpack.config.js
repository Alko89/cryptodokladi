var path = require('path')
var webpack = require('webpack')
const { VueLoaderPlugin } = require('vue-loader')

module.exports = {
  entry: __dirname + '/cryptodokladi/static/src/main.js',
  output: {
    path: path.resolve(__dirname, 'cryptodokladi/static/dist'),
    filename: 'build.js'
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader'
        ],
      },      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
          }
          // other vue-loader options go here
        }
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]?[hash]'
        }
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    },
    extensions: ['*', '.js', '.vue', '.json']
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true,
    overlay: true,
    contentBase: __dirname + "cryptodokladi/static/dist",
    publicPath: "http://localhost:8080/cryptodokladi/static/dist/",
    compress: true,
    headers: { 'Access-Control-Allow-Origin': '*' }
  },
  performance: {
    hints: false
  },
  devtool: '#eval-source-map',

  plugins: [
    // make sure to include the plugin for the magic
    new VueLoaderPlugin()
  ]
}

if (process.env.NODE_ENV === 'production') {
  module.exports.output.publicPath = '/static/dist/'
}
else {
  module.exports.output.publicPath = 'http://localhost:8080/cryptodokladi/static/dist/'
}
