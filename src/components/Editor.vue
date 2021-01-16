<template>
  <div class="editor">
    <div class="settings-bar">
      <span class="filename">{{ currentPath === "" ? "MyApp" : getFileName(currentPath) }}</span>
      <div class="not-saved-dot" v-if="!saved" />
      <div class="separator"/>
      <button class="setting" @click="compile">Compile</button>
      <button class="setting" @click="emulate">Emulate</button>
      <button class="setting" @click="program">Program</button>
    </div>
    <div class="stack">
      <textarea @keyup.tab="tabClick" @click="currentLine" @keyup="currentLine" @input="lineCount" @change="currentLine" id="editor" v-model="content" spellcheck="false" onscroll="display.scrollTo(0, this.scrollTop)"/>
      <div class="display" id="display">
        <div class="line" v-for="(line, index) in lines" :key="index">
          <div class="line-number">{{ index + 1 }}</div>
          <div class="line-content" v-html="colorLine(line)" />
        </div>
      </div>
    </div>
    <div class="terminal">
      <div class="top-bar">
        <div class="label">Output</div>
      </div>
      <div class="terminal-field" v-html="terminal"></div>
    </div>
  </div>
</template>

<script>
import { coloring, commands } from "@/variables";
import fileHandler from "../fileHandler";
let path =  require("path");

export default {
  name: "Editor",
  data() {
    return {
      content: '',
      currentLineNum: 0,
      currentLineCount: 0,
      lines: [""],
      selectionEnd: 0,
      editable: false,
      currentPath: "",
      saved: false,
      terminal: ""
    }
  },
  mounted() {
    window.ipcRenderer.on("new", async () => {
      if(this.content !== "") await fileHandler.saveFile(this.content, this.currentPath);
      this.currentPath = "";
      this.content = "";
      this.lineCount();
      this.partitionDocument()
    });
    window.ipcRenderer.on("open", async () => {
      let [content, currentPath ] = await fileHandler.openFile();
      if(currentPath !== "") {
        [this.content, this.currentPath] = [content, currentPath];
        this.lineCount();
        this.partitionDocument()
      }
    });
    window.ipcRenderer.on("save", async () => {
      await fileHandler.saveFile(this.content, this.currentPath);
      this.saved = true;
    });
    window.ipcRenderer.on("saveAs", async () => {
      this.currentPath = await fileHandler.saveFileAs(this.content);
      this.saved = true;
    });
    window.ipcRenderer.on("compile", async () => {
      await this.compile();
    });
    window.ipcRenderer.on("emulate", async () => {
      await this.emulate();
    });
    window.ipcRenderer.on("program", async () => {
      await this.program();
    });
  },
  methods: {
    currentLine(e) {
      this.currentLineNum = e.target.value.substr(0, e.target.selectionStart).split("\n").length;
      this.selectionEnd = e.target.value.substr(0, e.target.selectionEnd).split("\n").length;
    },
    lineCount() {
      let lineCount = this.content.length ? this.content.split(/\r\n|\r|\n/).length : 1;

      if(lineCount > this.currentLineCount) this.partitionDocument();
      else if(lineCount < this.currentLineCount) this.partitionDocument();
      else this.lines[this.currentLineNum - 1] = this.content.split(/\r\n|\r|\n/)[this.currentLineNum - 1];
      this.saved = false;
      this.currentLineCount = lineCount;
    },
    partitionDocument() {
      this.lines = this.content.split(/\r\n|\r|\n/);
    },
    colorLine(text) {
      coloring.forEach(coloring => { text = text.replace(coloring.value, "<span style='color: " + coloring.color + "'>" + coloring.replace + "</span>"); });
      commands.forEach(command => { text = text.replace(new RegExp(command, "gi"), `<span style='color: #d7b150'>$&</span>`); });
      return text;
    },
    tabClick() {
      this.lines[this.currentLineNum - 1] = this.content.split(/\r\n|\r|\n/)[this.currentLineNum - 1] + "0x";
      let editor = document.getElementById("editor");
      const startPos = editor.selectionStart, endPos = editor.selectionEnd;
      this.content = editor.value.substring(0, startPos) + "0x" + editor.value.substring(endPos, editor.value.length);
    },
    getFileName(txt) {
      return path.basename(txt);
    },
    println(data) {
      this.terminal += data + "<br>";
    },
    async compile() {
      await fileHandler.compileScript(this.content, this.currentPath, msg => {
        if(msg) this.println(msg)
        else this.println("<span style='color: green'>Compiled!</span>")
      });

      this.saved = true;
    },
    async emulate() {
      console.log(await fileHandler.openEmulator(this.content, this.currentPath, msg => {
        if(msg) this.println(msg)
        else this.println("Emulator on!")
      }));

      this.saved = true;
    },
    async program() {
      console.log(await fileHandler.programMemory(this.content, this.currentPath, msg => {
        if(msg) this.println(msg)
        else this.println("<span style='color: greenyellow'>Programed!</span>")
      }));

      this.saved = true;
    }
  }
}
</script>

<style lang="scss" scoped>
  .editor {
    height: 100vh;
    padding: 30px;

    .settings-bar {
      height: 30px;
      padding-right: 30px;
      padding-bottom: 15px;
      margin-left: -10px;
      display: flex;
      font-weight: bold;

      .filename {
        margin: auto 10px;
      }

      .not-saved-dot {
        height: 10px;
        width: 10px;
        border-radius: 10px;
        background: red;
        margin: auto 0;
      }

      .separator {
        flex: 1;
      }

      .setting {
        outline: none;
        border: none;
        margin: 0 10px;
        padding: 0 10px;
        background: #202020;
        color: white;
        cursor: pointer;
        font-family: "Roboto", sans-serif;
      }
    }

    .stack {
      #editor {
        position: absolute;
        width: 100%;
        height: calc(80% - 90px);
        background-color: #101010;
        outline: none;
        border: none;
        font-size: 25px;
        color: rgba(0, 0, 0, 0);
        caret-color: red;
        line-height: 34px;
        pointer-events: auto;
        letter-spacing: normal;
        padding: 0;
        tab-size: 4;
        margin: 1px 0 0 40px;
        overflow-y: scroll;
      }

      .display {
        position: fixed;
        width: 100%;
        height: calc(80% - 90px);
        pointer-events: none;
        background: transparent;
        overflow-y: hidden;

        .line {
          display: flex;
          align-items: center;

          .line-number {
            color: #404040;
            width: 40px;
            height: 34px;
            display: flex;
            align-items: center;
          }

          .line-content {
            letter-spacing: normal;
            padding: 0;
            margin: 0;
            font-size: 25px;
            pointer-events: none;
            white-space: pre;
          }
        }
      }
    }

    .terminal {
      position: absolute;
      width: calc(100% - 60px);
      height: 20%;
      bottom: 0;
      margin-left: -30px;
      padding: 0 30px;
      background: #202020;

      .top-bar {
        height: 40px;
        width: 100vw;
        margin: 0 -30px;
        background: black;
        border: #101010 2px solid;

        .label {
          font-family: "Roboto", sans-serif;
          font-weight: bold;
          margin: 3px 20px;
          padding: 10px;
        }
      }

      .terminal-field {
        height: auto;
        overflow-y: scroll;
        padding: 10px 0;
        max-height: calc(100% - 66px);
      }
    }
  }
</style>