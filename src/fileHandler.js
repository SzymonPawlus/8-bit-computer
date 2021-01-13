const dialog = window.require('electron').remote.dialog;
const { remote } = window.require('electron');
const fs = window.require('fs');
const { PythonShell } = window.require("python-shell")

export default class fileHandler {
    static async saveFileAs(data) {
        let filename = await dialog.showSaveDialog(remote.getCurrentWindow());
        if(filename.canceled) return "";
        let file = filename.filePath;
        fs.writeFile(file, data, (err) => {
            if(err) throw err;
        });
        return file;
    }

    static async saveFile(data, file) {
        if(!fs.existsSync(file)) return await this.saveFileAs(data);
        fs.writeFile(file, data, (err) => {
            if (err) throw err;
        });
        return file;
    }

    static async openFile() {
        let filename = await dialog.showOpenDialog(remote.getCurrentWindow());
        if(filename.canceled) return ["", ""]
        let file = filename.filePaths[0];
        let text = fs.readFileSync(file);
        return [text.toString(), file];
    }

    static async compileScript(data, file) {
        let file_ = await this.saveFile(data, file);
        let options = {
            mode: 'text',
            args: [file, "./src/output/code"],
        };
        PythonShell.run("./src/python/compiler.py", options, function (err, results){
            if(err) console.log(err);
            console.log(results);
        })
        return file_;
    }
}