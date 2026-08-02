<script setup lang="ts">
const props = defineProps<{
  value: number
}>()

function formatAmount(value: number): string {
  const sign = value < 0 ? '-' : ''
  const abs = Math.abs(value)
  const [intPart, fracPart] = abs.toFixed(2).split('.')
  const withCommas = intPart!.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  return `${sign}$${withCommas}.${fracPart}`
}

const formatted = computed(() => formatAmount(props.value))
const chars = computed(() => formatted.value.split(''))

const pulsing = ref(false)
watch(() => props.value, (next, prev) => {
  if (next === prev) return
  pulsing.value = true
  window.setTimeout(() => { pulsing.value = false }, 500)
})
</script>

<template>
  <div
    class="ticker-amount"
    :class="{ 'ticker-amount--pulsing': pulsing }"
    role="status"
    aria-live="polite"
    :aria-label="formatted"
  >
    <template v-for="(char, i) in chars" :key="chars.length - 1 - i">
      <OdometerDigit v-if="/\d/.test(char)" :digit="Number(char)" />
      <span v-else class="ticker-amount__symbol">{{ char }}</span>
    </template>
  </div>
</template>

<style scoped>
.ticker-amount {
  display: inline-flex;
  align-items: baseline;
  font-variant-numeric: tabular-nums;
  font-weight: 800;
  font-size: clamp(2.75rem, 9vw, 6rem);
  letter-spacing: -0.02em;
  color: var(--ui-primary, #00dc82);
  text-shadow: 0 0 24px color-mix(in oklab, var(--ui-primary, #00dc82) 45%, transparent);
  transition: text-shadow 0.5s ease;
}

.ticker-amount--pulsing {
  text-shadow: 0 0 40px color-mix(in oklab, var(--ui-primary, #00dc82) 80%, transparent);
}

.ticker-amount__symbol {
  display: inline-block;
}
</style>
