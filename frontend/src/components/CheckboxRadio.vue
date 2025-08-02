<template>
    <div class="checkbox-wrapper">
        <label class="switch">
            <input type="checkbox" v-model="model" :value="value" :disabled="disabled"/>
            <div class="slider round"></div>
        </label>
    </div>
</template>

<script>
export default {
  name: 'CheckboxRadio',
  props: {
    modelValue: { type: [Array, Boolean] },
    value: { type: [Boolean, Object] },
    disabled: { type: [Boolean, Object] },
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

.checkbox-wrapper .switch {
  display: inline-block;
  height: 22px;
  position: relative;
  width: 36px;

}

.checkbox-wrapper .switch input {
  display:none;
}

.checkbox-wrapper .slider {
    background-color: #bfc2c5;
    bottom: 0;
    cursor: pointer;
    left: 0;
    position: absolute;
    right: 0;
    top: 0;
    transition: .4s;
}

.checkbox-wrapper .slider:before {
  background-color: #fff;
  bottom: 4px;
  content: "";
  height: 14px;
  left: 4px;
  position: absolute;
  transition: .4s;
  width: 14px;
}

.checkbox-wrapper input:checked + .slider {
  background-color: #506bc5/*#66bb6a*/;
}

.checkbox-wrapper input:checked + .slider:before {
  transform: translateX(14px);
}

.checkbox-wrapper .slider.round {
  border-radius: 18px;
}

.checkbox-wrapper .slider.round:before {
  border-radius: 50%;
}
</style>