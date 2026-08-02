<script setup lang="ts">
import type { BalanceState, CentrifugoTickPayload, TickEvent, TickKind } from '~/types/payday'

const config = useRuntimeConfig()

const balance = ref<number | null>(null)
const events = ref<TickEvent[]>([])
const lastEvent = ref<{ kind: TickKind, label: string, amount: number } | null>(null)
const sequence = ref(0)
const loading = ref(true)
const error = ref<string | null>(null)

async function fetchBalance() {
  const data = await $fetch<BalanceState>('/balance', { baseURL: config.public.apiBase })
  balance.value = Number(data.balance)
}

async function fetchTicks() {
  const data = await $fetch<TickEvent[]>('/ticks', { baseURL: config.public.apiBase })
  events.value = [...data].reverse()
}

onMounted(async () => {
  try {
    await Promise.all([fetchBalance(), fetchTicks()])
    const latest = events.value[events.value.length - 1]
    if (latest) {
      lastEvent.value = { kind: latest.kind, label: latest.label, amount: Number(latest.amount) }
    }
  } catch {
    error.value = 'Не удалось загрузить данные с сервера'
  } finally {
    loading.value = false
  }
})

useCentrifugo(async (payload: CentrifugoTickPayload) => {
  balance.value = Number(payload.balance)
  lastEvent.value = { kind: payload.kind, label: payload.label, amount: Number(payload.amount) }
  sequence.value += 1

  try {
    await fetchTicks()
  } catch {
    // keep the last known chart data if the refetch fails
  }
})
</script>

<template>
  <div class="ticker-page">
    <header class="ticker-page__header">
      <span class="ticker-page__brand">Доходы Сергеева</span>
    </header>

    <main class="ticker-page__main">
      <p v-if="error" class="ticker-page__error">
        {{ error }}
      </p>

      <template v-else-if="balance !== null">
        <TickerAmount :value="balance" />
        <LastEventLine
          :kind="lastEvent?.kind ?? null"
          :label="lastEvent?.label ?? null"
          :amount="lastEvent?.amount ?? null"
          :sequence="sequence"
        />
        <EventsChart :events="events" class="ticker-page__chart" />
      </template>

      <p v-else class="ticker-page__loading">
        Загрузка…
      </p>
    </main>
  </div>
</template>

<style scoped>
.ticker-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: var(--ui-bg, #09090b);
}

.ticker-page__header {
  padding: 1.5rem 1rem 0;
  align-self: stretch;
  text-align: center;
}

.ticker-page__brand {
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--ui-text-muted, #71717a);
}

.ticker-page__main {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  padding: 2rem 1rem 4rem;
}

.ticker-page__chart {
  margin-top: 2rem;
}

.ticker-page__loading,
.ticker-page__error {
  color: var(--ui-text-muted, #71717a);
  font-size: 0.9375rem;
}

.ticker-page__error {
  color: var(--ui-error, #f43f5e);
}
</style>
