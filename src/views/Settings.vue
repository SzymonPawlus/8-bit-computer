<template>
 <div class="settings">
    <div class="option">
      <div class="option-label">Compiler Location</div>
      <div class="option-value">
        <div class="value-display">{{ set.compilerPath }}</div>
        <button class="value-change" @click="setCompilerPath">...</button>
      </div>
    </div>
   <div class="option">
     <div class="option-label">Emulator Location</div>
     <div class="option-value">
       <div class="value-display">{{ set.emulatorPath }}</div>
       <button class="value-change" @click="setEmulatorPath">...</button>
     </div>
   </div>
   <div class="option">
     <div class="option-label">Programmer Location</div>
     <div class="option-value">
       <div class="value-display">{{ set.programmerPath }}</div>
       <button class="value-change" @click="setProgrammerPath">...</button>
     </div>
   </div>
   <div class="option">
     <div class="option-label">Serial Port</div>
     <div class="option-value">
       <input type="text" placeholder="Enter serial port here..." v-model="set.port"/>
     </div>
   </div>
   <div class="option">
     <div class="option-label">Line Counting</div>
     <div class="option-value">
        <select v-model="set.lineCount">
          <option value="n">No line count</option>
          <option value="d">Decimal line count</option>
          <option value="h">Hexadecimal line count</option>
        </select>
     </div>
   </div>
    <button class="apply" @click="saveSettings">Apply changes</button>
 </div>
</template>

<script>
import fileHandler from "@/fileHandler";
let settings = window.require("electron-settings");

export default {
name: "Settings",
  data() {
    return {
      set: {
        compilerPath: "",
        emulatorPath: "",
        programmerPath: "",
        port: "",
        lineCount: "n"
      }
    }
  },
  methods: {
    async setCompilerPath() { this.set.compilerPath = await fileHandler.getPathToChosenFile(); },
    async setEmulatorPath() { this.set.emulatorPath = await fileHandler.getPathToChosenFile(); },
    async setProgrammerPath() { this.set.programmerPath = await fileHandler.getPathToChosenFile(); },
    async saveSettings() { await settings.set('settings', this.set); },
    async getSettings() { this.set = await settings.get('settings'); }
  },
  mounted() {
    this.getSettings();
  }
}
</script>

<style lang="scss" scoped>
  .settings {
    padding: 20px;
    display: flex;
    flex-direction: column;

    .option {
      width: 460px;
      margin: 20px auto;

      .option-label {
        font-size: 1.5rem;
        color: white;
        margin-bottom: 10px;
        font-family: "Roboto", sans-serif;
      }

      .option-value {
        width: 454px;
        height: 30px;
        padding: 3px;
        outline: none;
        border: none;
        background: #404040;
        justify-content: center;
        display: flex;
        font-size: 1.2rem;
        color: white;
        overflow: hidden;

        .value-display {
          width: 460px;
          margin: auto;

        }

        .value-change {
          height: 30px;
          width: 30px;
          padding: 3px;
        }

        select {
          width: 100%;
          outline: none;
          border: none;
          background: #404040;
          font-size: 1.2rem;
          color: white;
          font-family: "Roboto", sans-serif;
          padding-left: 10px;
        }

        option {
          font-family: "Roboto", sans-serif;
        }

        input {
          width: 100%;
          outline: none;
          border: none;
          background: #404040;
          font-size: 1.2rem;
          color: white;
          font-family: "Roboto", sans-serif;
          padding-left: 10px;
        }
      }
    }

    .apply {
      background: #0099ff;
      outline: none;
      border: #101010 1px solid;
      color: white;
      height: 40px;
      font-weight: bold;
      width: 460px;
      margin: 20px auto;
      font-family: "Roboto", sans-serif;
      font-size: 1.2rem;
    }
  }
</style>