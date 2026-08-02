<script setup lang="ts">
defineProps<{
  digit: number
}>()
</script>

<template>
  <span class="odometer-digit">
    <span
      class="odometer-digit__strip"
      :style="{ transform: `translateY(-${digit * 10}%)` }"
    >
      <span v-for="n in 10" :key="n" class="odometer-digit__cell">{{ n - 1 }}</span>
    </span>
  </span>
</template>

<style scoped>
.odometer-digit {
  display: inline-block;
  overflow: hidden;
  height: 1em;
  line-height: 1;
  vertical-align: baseline;
}

.odometer-digit__strip {
  display: flex;
  flex-direction: column;
  transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

.odometer-digit__cell {
  display: block;
  height: 1em;
  line-height: 1;
}
</style>
