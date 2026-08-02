<script setup lang="ts">
import type { TickKind } from '~/types/payday'

const props = defineProps<{
  kind: TickKind | null
  label: string | null
  amount: number | null
  sequence: number
}>()

const formatted = computed(() => {
  if (props.amount === null) return ''
  return props.amount.toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  })
})
</script>

<template>
  <div class="last-event">
    <Transition name="last-event__fade" mode="out-in">
      <p
        v-if="kind && label"
        :key="sequence"
        class="last-event__line"
        :class="kind === 'income' ? 'last-event__line--income' : 'last-event__line--expense'"
      >
        <UIcon
          :name="kind === 'income' ? 'i-lucide-arrow-up-right' : 'i-lucide-arrow-down-right'"
          class="last-event__icon"
        />
        <span class="last-event__amount">{{ kind === 'income' ? '+' : '-' }}{{ formatted }}</span>
        <span class="last-event__label">{{ label }}</span>
      </p>
      <p v-else key="placeholder" class="last-event__line last-event__line--placeholder">
        Ожидаем первое событие…
      </p>
    </Transition>
  </div>
</template>

<style scoped>
.last-event {
  min-height: 1.75rem;
  display: flex;
  justify-content: center;
  text-align: center;
}

.last-event__line {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
}

.last-event__icon {
  width: 1.1rem;
  height: 1.1rem;
  flex-shrink: 0;
}

.last-event__line--income {
  color: var(--ui-primary, #00dc82);
}

.last-event__line--expense {
  color: var(--ui-error, #f43f5e);
}

.last-event__line--placeholder {
  color: var(--ui-text-muted, #71717a);
}

.last-event__amount {
  font-variant-numeric: tabular-nums;
  font-weight: 700;
}

.last-event__label {
  color: var(--ui-text-muted, #a1a1aa);
  font-weight: 400;
}

.last-event__fade-enter-active,
.last-event__fade-leave-active {
  transition: all 0.35s ease;
}

.last-event__fade-enter-from {
  opacity: 0;
  transform: translateY(6px);
}

.last-event__fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
