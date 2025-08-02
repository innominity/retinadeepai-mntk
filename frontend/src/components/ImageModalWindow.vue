<template>
  <div class="modal" :class="{ 'modal-active': showModal }">
    <div class="modal-background"></div>
    <div class="modal-content">
      <p data-v-e8b67d3c="" class="image is-4by3">
        <img
          :src="imageSrc"
          alt=""
          style="object-fit: contain"
        />
      </p>
    </div>
    <button @click="close();"
      data-v-e8b67d3c=""
      class="modal-close is-large"
      aria-label="close"
    ></button>
  </div>
</template>

<script>
export default {
  name: "ImageModalWindow",
  props: {
    imageSrc: { type: [String] },
    showModal: { type: [Boolean] },
  },
  methods: {
    close() {
      this.$emit("close");
    }
  }
};
</script>


<style scoped>

.modal {
  align-items: center;
  display: none;
  flex-direction: column;
  justify-content: center;
  overflow: hidden;
  position: fixed;
  z-index: 40;
  bottom: 0;
  left: 0;
  position: fixed;
  right: 0;
  top: 0;
}

.modal-active {
  display: flex;
}

.modal-background {
  background-color: rgba(10, 10, 10, 0.86);
  bottom: 0;
  left: 0;
  position: fixed;
  right: 0;
  top: 0;
}

.modal-content,
.modal-card {
  margin: 0 20px;
  max-height: calc(100vh - 160px);
  overflow: auto;
  position: relative;
  width: 100%;
}

.modal-close,
.delete {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  user-select: none;
  -moz-appearance: none;
  -webkit-appearance: none;
  background-color: rgba(10, 10, 10, 0.2);
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  pointer-events: auto;
  display: inline-block;
  flex-grow: 0;
  flex-shrink: 0;
  font-size: 0;
  height: 20px;
  max-height: 20px;
  max-width: 20px;
  min-height: 20px;
  min-width: 20px;
  outline: none;
  position: relative;
  vertical-align: top;
  width: 20px;
}

.modal-close {
  background: none;
  height: 40px;
  position: fixed;
  right: 20px;
  top: 20px;
  width: 40px;
}

.is-large.modal-close,
.is-large.delete {
  height: 32px;
  max-height: 32px;
  max-width: 32px;
  min-height: 32px;
  min-width: 32px;
  width: 32px;
}

.modal-close::after, .delete::after {
    height: 50%;
    width: 2px;
}

.modal-close::before,
.delete::before {
  height: 2px;
  width: 50%;
}

.modal-close::before,
.delete::before,
.modal-close::after,
.delete::after {
  background-color: hsl(0, 0%, 100%);
  content: "";
  display: block;
  left: 50%;
  position: absolute;
  top: 50%;
  transform: translateX(-50%) translateY(-50%) rotate(45deg);
  transform-origin: center center;
}

.modal-close:hover, .delete:hover, .modal-close:focus, .delete:focus {
    background-color: rgba(10, 10, 10, 0.3);
}

.image {
  display: block;
  position: relative;
}

.image.is-4by3 {
  padding-top: 75%;
}

.image.is-4by3 img {
  bottom: 0;
  left: 0;
  position: absolute;
  right: 0;
  top: 0;
}

@media screen and (min-width: 769px) {
  .modal-content,
  .modal-card {
    margin: 0 auto;
    max-height: calc(100vh - 40px);
    width: 640px;
  }
}
</style>