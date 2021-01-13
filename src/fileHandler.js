const dialog = window.require('electron').remote.dialog;
const { remote } = window.require('electron');
const fs = window.require('fs');

export default class fileHandler{
    static async saveFileAs(data){
        let filename = await dialog.showSaveDialog(remote.getCurrentWindow());
        let set = !filename.canceled;
        if(set) {
            let file = filename.filePath;
            fs.writeFile(file, data, (err) => {
                if (err) throw err;
            });
            return file;
        }
       return "";

    }

    static async saveFile(data, file){
        if(fs.existsSync(file)){
            fs.writeFile(file, data, (err) => {
                if (err) throw err;
            });
            return file;
        }else{
            await this.saveFileAs(data);
        }
    }

    static async openFile(){
        let filename = await dialog.showOpenDialog(remote.getCurrentWindow());
        let set = !filename.canceled;
        if(set){
            let file = filename.filePaths[0];
            let text = fs.readFileSync(file);
            return [text.toString(), file];
        }
        return ["", ""]
    }
}