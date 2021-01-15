const dialog = window.require('electron').remote.dialog;
const { remote } = window.require('electron');
const fs = window.require('fs');
const { PythonShell } = window.require("python-shell");
let settings = window.require("electron-settings");

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
    }

    static async openFile() {
        let filename = await dialog.showOpenDialog(remote.getCurrentWindow());
        if(filename.canceled) return ["", ""]
        let file = filename.filePaths[0];
        let text = fs.readFileSync(file);
        return [text.toString(), file];
    }

    static async compileScript(data, file, errHandler) {
        await this.saveFile(data, file);
        let options = {
            mode: 'text',
            pythonOptions: ['-u'],
            args: [file, "./src/output/code"],
        };
        let compiler = await settings.get('settings.compilerPath');
        await PythonShell.run(compiler, options, function (err, results){
            console.log(results.toString()  + "\n" + err ? err : "")
            errHandler(results.toString()  + "\n" + err ? err : "");
        })
    }

    static async openEmulator(data, file, errHandler){
        await this.compileScript(data, file, errHandler);
        let emulator = await settings.get("settings.emulatorPath");
        let options = {
            mode: 'text',
            pythonOptions: ['-u'],
            args: ["./src/output/code.bin"],
        };
        await PythonShell.run(emulator, options, (err, results) => {
            console.log(results.toString()  + "\n" + err ? err : "")
            errHandler(results.toString()  + "\n" + err ? err : "");
        })
    }

    static async programMemory(data, file, errHandler){
        await this.compileScript(data, file, errHandler);
        let programmer = await settings.get("settings.programmerPath");
        let port = await settings.get("settings.port")
        let options = {
            mode: 'text',
            pythonOptions: ['-u'],
            args: ["./src/output/code.bin", port],
        };
        await PythonShell.run(programmer, options, (err, results) => {
            console.log(results.toString() + "\n" + err ? err : "")
            errHandler(results.toString()  + "\n" + err ? err : "");
        })
    }

    static async getPathToChosenFile(){
        let filename = await dialog.showOpenDialog(remote.getCurrentWindow());
        if(filename.canceled) return "";
        return filename.filePaths[0];
    }
}