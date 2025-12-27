# Claude Code Rules

## Git Workflow

**IMPORTANT: Разработка ведётся в отдельных ветках!**

1. **Создай ветку** для задачи:
   ```bash
   git checkout -b feature/название-задачи
   # или
   git checkout -b fix/описание-бага
   ```

2. **Работай в своей ветке** — никогда не коммить напрямую в `main`

3. **После завершения задачи** создай Pull Request:
   ```bash
   git push -u origin feature/название-задачи
   gh pr create --title "Описание" --body "Детали изменений"
   ```

4. **Дождись ревью** от Claude Code Action перед мержем

## Before Committing

**ALWAYS run all tests before making a commit:**

```bash
pytest tests/ -v --tb=short
```

- All tests must pass (0 failed, 0 errors)
- If tests fail, fix the issues before committing
- Do not commit broken code

## Project Structure

```
omnimap-tgbot/
├── bot/
│   ├── __init__.py
│   ├── main.py           # Entry point, health server
│   ├── config.py         # Settings from environment
│   ├── handlers/         # Command handlers
│   │   ├── start.py      # /start, /status, /unlink
│   │   └── callbacks.py  # Inline button handlers
│   ├── api/
│   │   └── client.py     # HTTP client for omnimap-back
│   └── keyboards/
│       └── inline.py     # Inline keyboard builders
├── tests/                # Unit and integration tests
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Workflow

1. Create a feature branch
2. Read the requirements
3. Implement the feature
4. Write unit tests
5. Run ALL tests: `pytest tests/`
6. Fix any failures
7. Commit only when all tests pass
8. Push and create a Pull Request

## Key Components

### Health Endpoint

Bot exposes `/health` endpoint on port 8002 for Kubernetes probes.

### Webhook vs Polling

- **Development**: Use polling mode (leave `WEBHOOK_URL` empty)
- **Production**: Set `WEBHOOK_URL` for webhook mode

### API Client

`bot/api/client.py` communicates with `omnimap-back` API:
- Check if Telegram user is linked
- Unlink user from OmniMap account
- Get linked user info

All requests include `X-Bot-Secret` header for authentication.

## Cross-Service Changes (ВАЖНО!)

**НИКОГДА не изменяй код других сервисов напрямую!**

Если изменения в omnimap-tgbot требуют изменений в других сервисах:

1. **НЕ редактируй** файлы в `omnimap-back`, `omnimap-front` или других сервисах
2. **Создай файл задач** `BACKEND_TASKS.md` или `FRONTEND_TASKS.md` в корне этого репозитория
3. **В PR укажи**, что требуются изменения в других сервисах
4. Агент, работающий над соответствующим сервисом, выполнит задачи

## Incoming Tasks

Проверь файл `TGBOT_TASKS.md` (если существует) — там могут быть задачи от бэкенда или других сервисов.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | Yes |
| `TELEGRAM_BOT_SECRET` | Secret for internal API auth | Yes |
| `OMNIMAP_BACKEND_URL` | Backend API URL | Yes |
| `FRONTEND_URL` | Frontend URL for links | Yes |
| `WEBHOOK_URL` | Webhook URL (production only) | No |
| `WEBHOOK_PORT` | Health/webhook port | No (default: 8002) |
| `LOG_LEVEL` | Logging level | No (default: INFO) |

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/ -v --tb=short

# Run with coverage
pytest tests/ --cov=bot --cov-report=html
```
