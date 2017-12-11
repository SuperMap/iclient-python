const webpack = require('webpack')
const path = require('path')

var leaflet_marker_selector = /leaflet\/dist\/images\/marker-.*\.png/;
var rules = [
    {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
    },
    {
        //图片小于80k采用base64编码
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
        exclude: /node_modules[\/\\]proj4|classic|underscore|mapv/,
        loader: 'babel-loader',
        query: {
            presets: ['es2015'],
            plugins: [
                'transform-class-properties'
            ]
        }
    }
]

const vendors = [
    '@turf/turf',
    'echarts',
    'elasticsearch',
    'jupyter-leaflet',
    'leaflet',
    'leaflet.heat',
    'lodash',
    'mapv',
    'underscore',
    'vector-tile',
    '@supermap/iclient-common',
    '@supermap/iclient-leaflet'
]

module.exports = {
    output: {
        path: path.resolve(__dirname, 'build'),
        filename: '[name].js',
        library: '[name]'
    },
    entry: {
        'lib': vendors,
    },
    plugins: [
        new webpack.DllPlugin({
            path: 'manifest.json',
            name: '[name]',
            context: __dirname,
        })
    ],
    module: {
        rules: rules
    }
}