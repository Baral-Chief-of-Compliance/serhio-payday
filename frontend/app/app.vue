<script setup>
useHead({
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],
  link: [
    { rel: 'icon', type: 'image/png', href: '/favicon.png' }
  ],
  htmlAttrs: {
    lang: 'ru'
  }
})

const title = 'Доходы Сергеева'
const description = 'Живой тикер дохода и расходов — зарплаты и бизнес-прибыль против покупки заводов и компаний.'

useSeoMeta({
  title,
  description,
  ogTitle: title,
  ogDescription: description
})
</script>

<template>
  <UApp>
    <NuxtPage />
  </UApp>
</template>
