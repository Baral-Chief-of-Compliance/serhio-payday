# serhio-payday

Живой тикер зарплаты/капитала: сервис-генератор случайных +/- тиков пишет их в
Postgres и рассылает через Centrifugo, backend отдаёт историю по REST,
frontend (Nuxt) и vk-bot их показывают.

Сервисы: `postgres`, `centrifugo`, `backend`, `payday-generator`, `frontend`, `vk-bot`.

## env_params/

Все переменные окружения контейнеров лежат в `env_params/` и подключаются
через `env_file:` в docker-compose. Папка в `.gitignore`, в репозиторий не
попадает — на сервере нужно создать эти файлы руками.

### Prod (`docker-compose.yaml`)

**`.env.postgres.prod`**

| Переменная | Описание |
|---|---|
| `POSTGRES_USER` | пользователь БД |
| `POSTGRES_PASSWORD` | пароль пользователя БД |
| `POSTGRES_DB` | имя БД (используется всеми сервисами, которые ходят в Postgres) |
| `TZ` | таймзона контейнера, например `Europe/Moscow` |

**`backend.env`**

| Переменная | Описание |
|---|---|
| `POSTGRES_HOST` | хост Postgres, обычно `serhio-payday-postgres` (имя контейнера в сети compose) |
| `POSTGRES_PORT` | порт Postgres, `5432` |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` | должны совпадать со значениями из `.env.postgres.prod` |
| `CORS_ORIGINS` | JSON-список origin'ов фронта, например `["https://serhio.payday.polartitan.ru"]` |

**`payday-generator.env`**

| Переменная | Описание |
|---|---|
| `POSTGRES_HOST` / `POSTGRES_PORT` / `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` | те же, что и у backend |
| `START_BALANCE` | стартовый баланс |
| `TICK_MIN_SECONDS` / `TICK_MAX_SECONDS` | диапазон интервала между тиками, сек |
| `INCOME_PROBABILITY` | вероятность положительного тика (0..1) |
| `CENTRIFUGO_ENABLED` | `true`/`false` — рассылать ли тики в Centrifugo |
| `CENTRIFUGO_API_URL` | внутренний HTTP API Centrifugo, `http://serhio-payday-centrifugo:8000/api` |
| `CENTRIFUGO_API_KEY` | должен совпадать с `http_api.key` в `centrifugo/config.prod.json` |
| `CENTRIFUGO_CHANNEL` | канал публикации, например `serhio_payday:ticks` |

**`frontend.env`**

| Переменная | Описание |
|---|---|
| `NUXT_PUBLIC_API_BASE` | публичный адрес backend API, например `https://serhio.payday.polartitan.ru/api` |
| `NUXT_PUBLIC_CENTRIFUGO_WS_URL` | публичный WS-адрес Centrifugo, `wss://serhio.payday.polartitan.ru/connection/websocket` |
| `NUXT_PUBLIC_CENTRIFUGO_TOKEN` | JWT-токен клиента для подписки на канал (подписывается `hmac_secret_key` из `centrifugo/config.prod.json`) |
| `NUXT_PUBLIC_CENTRIFUGO_CHANNEL` | канал подписки, должен совпадать с `CENTRIFUGO_CHANNEL` |

**`vk-bot.env`**

| Переменная | Описание |
|---|---|
| `VK_TOKEN` | токен группы VK (Bot/Group token) |
| `API_BASE` | внутренний адрес backend, `http://serhio-payday-backend:8000` |
| `CHAT_BROADCAST_INTERVAL_SECONDS` | интервал рассылки в чат, сек |
| `WALL_POST_INTERVAL_SECONDS` | интервал постов на стену, сек |

### Dev (`docker-compose-dev.yaml`)

Поднимает только `postgres` и `centrifugo` локально, остальные сервисы
запускаются вне docker (`uv run`, `pnpm dev` и т.д.).

**`.env.postgres.dev`** — `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `TZ`.

**`.env.centrifugo.dev`** — переменные окружения Centrifugo для dev-конфига
(`centrifugo/config.dev.json`); если конфиг не читает env — можно оставить
пустым, как сейчас.

## ⚠️ На заметку

- `centrifugo/config.prod.json` тоже в `.gitignore` (содержит боевые секреты
  `client.token.hmac_secret_key` и `http_api.key`), в репозиторий не попадает —
  на сервере его нужно создавать/выкладывать отдельно (scp/CI secret), так же
  как и `env_params/`.
- `CENTRIFUGO_API_KEY` в `payday-generator.env` и `http_api.key` в
  `centrifugo/config.prod.json` должны быть идентичны — иначе генератор не
  сможет публиковать тики.
- `NUXT_PUBLIC_CENTRIFUGO_TOKEN` во frontend.env — это JWT, подписанный
  `hmac_secret_key` из `centrifugo/config.prod.json`; при смене секрета токен
  нужно перевыпустить.
