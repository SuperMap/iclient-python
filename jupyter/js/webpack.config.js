var path = require('path');
var version = require('./package.json').version;
var webpack = require('webpack');
var CopyWebpackPlugin = require('copy-webpack-plugin');

var leaflet_marker_selector = /leaflet\/dist\/images\/marker-.*\.png/;
var rules = [
    {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
    },
    {
        test: /\.(png|jpg|jpeg|gif|woff|woff2|svg|eot|ttf)$/,
        use: [{
            loader: 'url-loader',
            options: {
                limit: 80000
            }
        }]
    },
    {
        test: leaflet_marker_selector,
        use: [{
            loader: 'file-loader',
            options: {
                name: '[name].[ext]'
            }
        }]
    },
    {
        test: [/\.js$/],
        exclude: /node_modules[\/\\]underscore|mapv|geojson-utils|geojson-polygon-self-intersections/,
        loader: 'babel-loader',
        query: {
            presets: ['es2015'],
            plugins: [
                'transform-class-properties'
            ]
        }
    }
]

plugins = [
    new webpack.DllReferencePlugin({
        context: __dirname,
        manifest: require('./manifest.json')
    }),
    new CopyWebpackPlugin([{
        from: './build/lib.js',
        to: path.resolve(__dirname, '..', 'iclientpy', 'static')
    }])
]

module.exports = [
    {
        entry: './src/extension.js',
        output: {
            filename: 'extension.js',
            path: path.resolve(__dirname, '..', 'iclientpy', 'static'),
            libraryTarget: 'amd'
        },
        plugins: plugins
    }, {
        entry: ['./src/index.js'],
        output: {
            filename: 'index.js',
            path: path.resolve(__dirname, '..', 'iclientpy', 'static'),
            libraryTarget: 'amd'
        },
        devtool: 'source-map',
        module: {
            rules: rules
        },
        externals: ['@jupyter-widgets/base'],
        plugins: plugins
    }, {
        entry: './src/embed.js',
        output: {
            filename: 'index.js',
            path: path.resolve(__dirname, 'dist'),
            libraryTarget: 'amd',
            publicPath: 'https://unpkg.com/iclientpy@' + version + '/dist/'
        },
        devtool: 'source-map',
        module: {
            rules: rules
        },
        externals: ['@jupyter-widgets/base'],
        plugins: plugins
    }
];
