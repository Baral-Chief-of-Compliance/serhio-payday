<script setup lang="ts">
import type { TickEvent } from '~/types/payday'

const props = defineProps<{
  events: TickEvent[]
}>()

const width = 600
const height = 220
const padding = { top: 16, right: 12, bottom: 16, left: 12 }
const innerWidth = width - padding.left - padding.right
const innerHeight = height - padding.top - padding.bottom

const points = computed(() => {
  const data = props.events
  const n = data.length
  if (n === 0) return []

  const values = data.map(e => Number(e.balance_after))
  const minRaw = Math.min(...values)
  const maxRaw = Math.max(...values)
  const span = maxRaw - minRaw || 1
  const pad = span * 0.15
  const min = minRaw - pad
  const max = maxRaw + pad

  return data.map((event, i) => {
    const x = n === 1
      ? padding.left + innerWidth / 2
      : padding.left + (i / (n - 1)) * innerWidth
    const value = Number(event.balance_after)
    const y = padding.top + innerHeight - ((value - min) / (max - min)) * innerHeight
    return { x, y, value, event }
  })
})

const linePath = computed(() =>
  points.value.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x.toFixed(2)},${p.y.toFixed(2)}`).join(' ')
)

const areaPath = computed(() => {
  if (points.value.length === 0) return ''
  const baseline = padding.top + innerHeight
  const first = points.value[0]!
  const last = points.value[points.value.length - 1]!
  return `${linePath.value} L${last.x.toFixed(2)},${baseline} L${first.x.toFixed(2)},${baseline} Z`
})

const gridLines = computed(() => {
  const steps = 3
  return Array.from({ length: steps + 1 }, (_, i) => padding.top + (innerHeight / steps) * i)
})

const hoveredIndex = ref<number | null>(null)
const hovered = computed(() => hoveredIndex.value === null ? null : points.value[hoveredIndex.value] ?? null)

const step = computed(() => {
  const n = points.value.length
  return n > 1 ? innerWidth / (n - 1) : innerWidth
})

const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2
})

function formatValue(value: number): string {
  return currencyFormatter.format(value)
}

function formatTime(iso: string): string {
  return new Date(iso).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

const showTable = ref(false)
</script>

<template>
  <section class="events-chart">
    <div class="events-chart__header">
      <h2 class="events-chart__title">
        Баланс — последние {{ events.length }} событий
      </h2>
      <button type="button" class="events-chart__table-toggle" @click="showTable = !showTable">
        {{ showTable ? 'Скрыть таблицу' : 'Показать как таблицу' }}
      </button>
    </div>

    <div v-if="points.length > 1" class="events-chart__plot">
      <svg
        :viewBox="`0 0 ${width} ${height}`"
        class="events-chart__svg"
        preserveAspectRatio="none"
        role="img"
        aria-label="График баланса за последние события"
      >
        <line
          v-for="(y, i) in gridLines"
          :key="i"
          :x1="padding.left"
          :x2="width - padding.right"
          :y1="y"
          :y2="y"
          class="events-chart__gridline"
        />

        <path :d="areaPath" class="events-chart__area" />
        <path :d="linePath" class="events-chart__line" />

        <line
          v-if="hovered"
          :x1="hovered.x"
          :x2="hovered.x"
          :y1="padding.top"
          :y2="padding.top + innerHeight"
          class="events-chart__crosshair"
        />

        <circle
          v-for="(p, i) in points"
          :key="p.event.id"
          :cx="p.x"
          :cy="p.y"
          :r="i === hoveredIndex || i === points.length - 1 ? 5 : 3"
          class="events-chart__dot"
          :class="{ 'events-chart__dot--active': i === hoveredIndex || i === points.length - 1 }"
        />

        <rect
          v-for="(p, i) in points"
          :key="`hit-${p.event.id}`"
          :x="p.x - step / 2"
          :y="padding.top"
          :width="step"
          :height="innerHeight"
          fill="transparent"
          tabindex="0"
          class="events-chart__hit"
          :aria-label="`${formatValue(p.value)}, ${p.event.label}, ${formatTime(p.event.created_at)}`"
          @pointerenter="hoveredIndex = i"
          @pointerleave="hoveredIndex = null"
          @focus="hoveredIndex = i"
          @blur="hoveredIndex = null"
        />
      </svg>

      <div
        v-if="hovered"
        class="events-chart__tooltip"
        :style="{ left: `${(hovered.x / width) * 100}%`, top: `${(hovered.y / height) * 100}%` }"
      >
        <div class="events-chart__tooltip-value">
          {{ formatValue(hovered.value) }}
        </div>
        <div class="events-chart__tooltip-label">
          {{ hovered.event.label }}
        </div>
        <div class="events-chart__tooltip-time">
          {{ formatTime(hovered.event.created_at) }}
        </div>
      </div>
    </div>

    <p v-else class="events-chart__empty">
      Пока недостаточно данных для графика
    </p>

    <div v-if="showTable" class="events-chart__table-wrap">
      <table class="events-chart__table">
        <thead>
          <tr>
            <th>Время</th>
            <th>Событие</th>
            <th>Сумма</th>
            <th>Баланс</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="event in [...events].reverse()" :key="event.id">
            <td>{{ formatTime(event.created_at) }}</td>
            <td>{{ event.label }}</td>
            <td :class="event.kind === 'income' ? 'events-chart__amount--income' : 'events-chart__amount--expense'">
              {{ event.kind === 'income' ? '+' : '-' }}{{ formatValue(Number(event.amount)) }}
            </td>
            <td>{{ formatValue(Number(event.balance_after)) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
.events-chart {
  width: 100%;
  max-width: 44rem;
}

.events-chart__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.events-chart__title {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--ui-text-muted, #a1a1aa);
  margin: 0;
}

.events-chart__table-toggle {
  font-size: 0.75rem;
  color: var(--ui-text-muted, #a1a1aa);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
  text-underline-offset: 2px;
}

.events-chart__table-toggle:hover {
  color: var(--ui-primary, #00dc82);
}

.events-chart__plot {
  position: relative;
}

.events-chart__svg {
  width: 100%;
  height: 220px;
  display: block;
  overflow: visible;
}

.events-chart__gridline {
  stroke: var(--ui-border, #27272a);
  stroke-width: 1;
}

.events-chart__area {
  fill: color-mix(in oklab, var(--ui-primary, #00dc82) 12%, transparent);
  stroke: none;
}

.events-chart__line {
  fill: none;
  stroke: var(--ui-primary, #00dc82);
  stroke-width: 2;
  stroke-linejoin: round;
  stroke-linecap: round;
}

.events-chart__crosshair {
  stroke: var(--ui-border, #3f3f46);
  stroke-width: 1;
}

.events-chart__dot {
  fill: var(--ui-primary, #00dc82);
  stroke: var(--ui-bg, #0c0c0e);
  stroke-width: 2;
  transition: r 0.15s ease;
}

.events-chart__hit {
  cursor: pointer;
  outline: none;
}

.events-chart__tooltip {
  position: absolute;
  transform: translate(-50%, -120%);
  background: var(--ui-bg-elevated, #18181b);
  border: 1px solid var(--ui-border, #27272a);
  border-radius: 0.5rem;
  padding: 0.5rem 0.75rem;
  pointer-events: none;
  white-space: nowrap;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
}

.events-chart__tooltip-value {
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  color: var(--ui-text, #f4f4f5);
  font-size: 0.875rem;
}

.events-chart__tooltip-label,
.events-chart__tooltip-time {
  color: var(--ui-text-muted, #a1a1aa);
  font-size: 0.75rem;
}

.events-chart__empty {
  color: var(--ui-text-muted, #a1a1aa);
  font-size: 0.875rem;
  text-align: center;
  padding: 2rem 0;
}

.events-chart__table-wrap {
  margin-top: 1rem;
  max-height: 16rem;
  overflow-y: auto;
  overflow-x: auto;
  border: 1px solid var(--ui-border, #27272a);
  border-radius: 0.5rem;
}

.events-chart__table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8125rem;
}

.events-chart__table th,
.events-chart__table td {
  padding: 0.5rem 0.75rem;
  text-align: left;
  white-space: nowrap;
}

.events-chart__table th {
  color: var(--ui-text-muted, #a1a1aa);
  font-weight: 500;
  position: sticky;
  top: 0;
  background: var(--ui-bg-elevated, #18181b);
}

.events-chart__table td:first-child,
.events-chart__table td:last-child {
  font-variant-numeric: tabular-nums;
}

.events-chart__amount--income {
  color: var(--ui-primary, #00dc82);
  font-variant-numeric: tabular-nums;
}

.events-chart__amount--expense {
  color: var(--ui-error, #f43f5e);
  font-variant-numeric: tabular-nums;
}
</style>
