const webpack = require('webpack');
const path = require('path');

const config = {
  output: {
    path: path.join(path.resolve(__dirname), 'build'),
    filename: 'bundle.js',
  },

  resolve: {
    extensions: ['.tsx', '.ts', '.js', '.jsx'],
  },

  entry: ['./src/index.tsx'],

  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: 'awesome-typescript-loader',
      },
    ],
  },

  plugins: [],

  devtool: 'source-map',
};

module.exports = config;
