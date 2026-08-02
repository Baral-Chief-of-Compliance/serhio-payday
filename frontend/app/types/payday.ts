export type TickKind = 'income' | 'expense'

export interface TickEvent {
  id: number
  kind: TickKind
  label: string
  amount: string
  balance_after: string
  created_at: string
}

export interface CentrifugoTickPayload {
  kind: TickKind
  label: string
  amount: string
  balance: string
}

export interface BalanceState {
  id: number
  balance: string
  updated_at: string
}
