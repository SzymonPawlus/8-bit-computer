<template>
  <div class="editor">
    <div class="stack">
      <textarea @keyup.tab="tabClick" @click="currentLine" @keyup="currentLine" @input="lineCount" @change="currentLine" id="editor" v-model="content" spellcheck="false" onscroll="display.scrollTo(0, this.scrollTop)"/>
      <div class="display" id="display">
        <div class="line" v-for="(line, index) in lines" :key="index">
          <div class="line-number">{{ index + 1 }}</div>
          <div class="line-content" v-html="colorLine(line)" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { coloring, commands } from "@/variables";

export default {
  name: "Editor",
  data() {
    return {
      content: '',
      currentLineNum: 0,
      currentLineCount: 0,
      lines: [""],
      selectionEnd: 0,
      editable: false
    }
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
    }
  }
}
</script>

<style lang="scss" scoped>
  .editor {
    height: 100vh;
    padding: 30px;

    span {
      height: 5%;
    }

    .stack {
      #editor {
        position: absolute;
        width: 100%;
        height: 95%;
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
        height: 95%;
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
          }
        }
      }
    }
  }
</style>