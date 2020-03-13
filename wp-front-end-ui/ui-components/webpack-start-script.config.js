const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopywebpackPlugin = require('copy-webpack-plugin');


const startConfig = (options, entry, htmlFile, enableCesium = false) => {
    const devtool_val = options.mode == 'development' ? 'source-map' : '';
    let cesiumPlugins = []
    let cesiumAliasPath = '';
    if (enableCesium) {
        // The path to the cesium source code
        const cesiumSource = 'node_modules/cesium/Source';
        const cesiumWorkers = '../Build/Cesium/Workers';
        const olSource = 'node_modules/openlayers/src/ol';
        cesiumAliasPath = path.resolve(__dirname, cesiumSource)
        cesiumPlugins = [
            // Copy Cesium Assets, Widgets, and Workers to a static directory
            new CopywebpackPlugin([{from: path.join(cesiumSource, cesiumWorkers), to: 'Workers'}]),
            new CopywebpackPlugin([{from: path.join(cesiumSource, 'Assets'), to: 'Assets'}]),
            new CopywebpackPlugin([{from: path.join(cesiumSource, 'Widgets'), to: 'Widgets'}]),
            new webpack.DefinePlugin({
                // Define relative base path in cesium for loading assets
                CESIUM_BASE_URL: JSON.stringify('')
            }),
        ]
    }
    return {
        entry: entry,
        devtool: devtool_val,
        output: {
            filename: '[name].bundle.js',
            chunkFilename: '[name].bundle.js',
            path: path.resolve(__dirname, 'dist'),
            // Needed by Cesium for multiline strings
            sourcePrefix: ''
        },
        amd: {
            // Enable webpack-friendly use of require in cesium
            toUrlUndefined: true
        },
        node: {
            // Resolve node module use of fs
            fs: "empty"
        },
        resolve: {
            extensions: ['.js', '.jsx', '.ts', '.tsx', '.json'],
            alias: {
                // Cesium module name
                cesium: cesiumAliasPath,
            }
        },
        module: {
            rules: [
                {
                    // Remove pragmas
                    test: /\.js$/,
                    // enforce: 'pre',
                    exclude: /node_modules/,
                    // include: path.resolve(__dirname, cesiumSource),
                    use: {loader: "babel-loader"}
                },
                {
                    test: /\.tsx?$/,
                    loader: 'awesome-typescript-loader'
                },
                {
                    test: /\.css$/,
                    use: ['style-loader', {
                        loader: 'css-loader',
                        // options: {
                        //     // Minify css
                        //     minimize: true
                        // }
                    }]
                },
                {
                    test: /\.(png|gif|jpe?g|svg|xml|json)$/,
                    use: {
                        loader: 'url-loader',
                    },
                },
                {
                    test: /\.pug$/,
                    loader: 'pug-loader'
                }
            ]
        },
        plugins: [
            ...cesiumPlugins,
            new HtmlWebpackPlugin({
                template: 'src/templates/' + htmlFile
            }),
        ],
        mode: options.mode
    }
};
module.exports = startConfig;