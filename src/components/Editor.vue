<template>
  <div class="editor">
    {{ currentLineNum }} / {{ currentLineCount }}
    <textarea @click="countLines" @keyup="countLines" @input="countLines" id="editor" v-model="content" />
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
      lines: []
    }
  },
  methods: {
    countLines(e) {
      this.currentLine(e);
      this.lineCount();
      console.log(this.lines);
    },
    currentLine(e) {
      this.currentLineNum = e.target.value.substr(0, e.target.selectionStart).split("\n").length;
    },
    lineCount() {
      let lineCount = this.content.length ? this.content.split(/\r\n|\r|\n/).length : 0;

      if(lineCount > this.currentLineCount) this.lines.splice(this.currentLineNum - 1, 0, this.content.split(/\r\n|\r|\n/)[this.currentLineNum - 1]);
      else if(lineCount < this.currentLineCount) this.lines.splice(this.currentLineNum, 1);
      else this.lines[this.currentLineNum - 1] = this.content.split(/\r\n|\r|\n/)[this.currentLineNum - 1];

      this.currentLineCount = lineCount;
    }
  }
}
</script>

<style lang="scss" scoped>
.editor {
  #editor {
    width: 100%;
    height: 100vh;
    background-color: #101010;
    outline: none;
    border: none;
    color: white;
  }
}
</style>