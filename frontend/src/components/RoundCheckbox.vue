<template>
    <div class="checkbox-wrapper">
      <label class="round">
        <input :disabled="disabled" type="checkbox" v-model="model" :value="value"/>
        <span class="checkbox-radio"></span>
      </label>
    </div>
  </template>
  
  <script>
  export default {
    name: 'RoundCheckbox',
    props: {
      modelValue: { type: [Array, Boolean] },
      value: { type: [Boolean, Object] },
      disabled: { type: [Boolean] },
    },
    computed:{
      model:{
        get() {
          return this.modelValue;
        },
        set(value) {
          this.$emit("update:modelValue", value);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  
  .checkbox-wrapper {
    display: inline-flex;
  }
  
  .checkbox-wrapper .round .checkbox-radio {
    position: relative;
    background-color: #fff;
    border: 1px solid #d9d9d9;
    border-radius: 50%;
    cursor: pointer;
    height: 18px;
    width: 18px;
    display: block;
  }
  
  .checkbox-wrapper .round .checkbox-radio:after {
    border: 2px solid #fff;
    border-top: none;
    border-right: none;
    content: "";
    height: 5px;
    left: 4px;
    opacity: 0;
    position: absolute;
    top: 5px;
    transform: rotate(-45deg);
    width: 8px;
  }
  
  .checkbox-wrapper .round input[type="checkbox"] {
    visibility: hidden;
    display: none;
    opacity: 0;
  }
  
  .checkbox-wrapper .round input[type="checkbox"]:checked + .checkbox-radio {
    background-color: #5e8de1;
    border-color: #5789e7;
  }
  
  .checkbox-wrapper .round input[type="checkbox"]:checked + .checkbox-radio:after {
    opacity: 1;
  }
  
  </style>
  