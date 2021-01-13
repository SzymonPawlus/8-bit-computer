module.exports = {
    pluginOptions: {
        electronBuilder: {
            preload: 'src/preload.js',
            extraResources: 'src/assets/compiler.py'
        }
    }
}