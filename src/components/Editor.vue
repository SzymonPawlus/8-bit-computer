<template>
  <div class="editor">
    <span>{{ currentLineNum }} / {{ currentLineCount }}</span>
    <div class="stack">
      <textarea @click="currentLine" @keyup="currentLine" @input="lineCount" @change="currentLine" id="editor" v-model="content" spellcheck="fals"/>
      <div class="display" >
        <div class="line" v-for="(line, index) in lines" :key="index" v-html="colorLine(line)"></div>
      </div>
    </div>
  </div>
</template>

<script>
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
    countLines(e) {
      this.currentLine(e);
      this.lineCount();
    },
    currentLine(e) {
      this.currentLineNum = e.target.value.substr(0, e.target.selectionStart).split("\n").length;
      this.selectionEnd = e.target.value.substr(0, e.target.selectionEnd).split("\n").length;
      console.log(this.lines);
    },
    lineCount() {
      let lineCount = this.content.length ? this.content.split(/\r\n|\r|\n/).length : 1;
      //if(lineCount > this.currentLineCount) this.lines.splice(this.currentLineNum - 1, 0, this.content.split(/\r\n|\r|\n/)[this.currentLineNum - 1]);
      if(lineCount > this.currentLineCount) this.partitionDocument();
      else if(lineCount < this.currentLineCount){
        this.partitionDocument();
      }
      else this.lines[this.currentLineNum - 1] = this.content.split(/\r\n|\r|\n/)[this.currentLineNum - 1];

      this.currentLineCount = lineCount;
      console.log(this.lines);
    },
    partitionDocument(){
      this.lines = this.content.split(/\r\n|\r|\n/);
    },
    colorLine(text){
      text = text.replace(/(["'])(?:(?=(\\?))\2.)*?\1/, "<span style='color: red'>$&</span>");
      text = text.replace("#define", "<span style='color: blue'>#define</span>");
      text = text.replace(/0[xX][0-9a-fA-F]+/, "<span style='color: yellow'>$&</span>");
      text = text.replace(/^\.\w+[a-zA-Z0-9_]:/, "<span style='color: green'>$&</span>");
      text = text.replace(/;.*$/, "<span style='color: gray'>$&</span>");

      return text;
    }
  }
}
</script>

<style lang="scss" scoped>
.editor {
  height: 100vh;
  span{
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
      font-size: 16px;
      color: rgba(0, 0, 0, 0);
      caret-color: red;
      line-height: 16px;
      pointer-events: auto;
      letter-spacing: normal;
      padding: 0;
      margin: 1px 0 0 0;
      tab-size: 4;

    }
    .display{
      position: relative;
      width: 100%;
      height: 95%;
      pointer-events: none;
      background: transparent;

      .line{
        font-family: Roboto,serif;
        letter-spacing: normal;
        padding: 0;
        margin: 0;
        font-size: 16px;
        height: 16px;
        pointer-events: none;
      }
    }

  }
}
</style>