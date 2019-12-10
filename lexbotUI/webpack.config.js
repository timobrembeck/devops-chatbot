const path = require("path");
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');


module.exports = {
    entry: ['babel-polyfill','whatwg-fetch','./src/js/index.js','./src/css/styles.css'],
    output: {
      path: path.join(__dirname, "./dist/"),
		  filename: "bundle.js"
    },
    resolveLoader: {
      modules: [
          'node_modules',
      ],
    },
    mode: 'production',
    module: {
        rules: [
          {
            test: /\.js$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            query: {
              plugins: ['transform-runtime'],
              presets: ['es2015','stage-0'] 
            }
          },
    
          {
            test: /\.css$/,
            use: ExtractTextPlugin.extract({
                loader: 'css-loader',
                options: {
                    minimize: true,
                },
            }),
          },
      ]
    },
    resolve: {
      extensions: ['.js', '.es6']
    },
    plugins: [ 
      new ExtractTextPlugin({filename: 'bundle.css'}),
      new OptimizeCssAssetsPlugin({
        assetNameRegExp: /\.css$/g,
        cssProcessor: require('cssnano'),
        cssProcessorPluginOptions: {
          preset: ['default', { discardComments: { removeAll: true } }],
        },
        canPrint: true
      })
    ]
    
}