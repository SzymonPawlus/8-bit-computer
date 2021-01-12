<template>
  <div class="editor">
    <span>{{ currentLineNum }} / {{ currentLineCount }}</span>
    <div class="stack">
      <textarea @click="currentLine" @keyup="currentLine" @input="lineCount" @change="currentLine" id="editor" v-model="content" spellcheck="false"/>
      <div class="display" >
        <div class="line" v-for="(line, index) in lines" :key="index" v-html="colorLine(line)"></div>
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
      lines: [],
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
      else if(lineCount < this.currentLineCount){
        this.partitionDocument();
      }
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
    }
  }
}
</script>

<style lang="scss" scoped>
.editor {
  height: 100vh;

  span {
    height: 5%;
  }

  .stack {
    #editor {
      font-family: Roboto,serif;
      position: absolute;
      width: 100%;
      height: 95%;
      background-color: #101010;
      outline: none;
      border: none;
      font-size: 25px;
      color: rgba(0, 0, 0, 0);
      caret-color: red;
      line-height: 25px;
      pointer-events: auto;
      letter-spacing: normal;
      padding: 0;
      margin: 1px 0 0 0;
      tab-size: 4;

    }
    .display {
      position: relative;
      width: 100%;
      height: 95%;
      pointer-events: none;
      background: transparent;

      .line {
        font-family: Roboto, serif;
        letter-spacing: normal;
        padding: 0;
        margin: 0;
        font-size: 25px;
        height: 25px;
        pointer-events: none;
      }
    }
  }
}
</style>