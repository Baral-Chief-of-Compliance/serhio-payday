import { Centrifuge } from 'centrifuge'
import type { CentrifugoTickPayload } from '~/types/payday'

export function useCentrifugo(onTick: (payload: CentrifugoTickPayload) => void) {
  const config = useRuntimeConfig()
  let centrifuge: Centrifuge | null = null

  onMounted(() => {
    centrifuge = new Centrifuge(config.public.centrifugoWsUrl, {
      token: config.public.centrifugoToken
    })

    const subscription = centrifuge.newSubscription(config.public.centrifugoChannel)
    subscription.on('publication', (ctx) => {
      onTick(ctx.data as CentrifugoTickPayload)
    })
    subscription.subscribe()

    centrifuge.connect()
  })

  onUnmounted(() => {
    centrifuge?.disconnect()
    centrifuge = null
  })
}
