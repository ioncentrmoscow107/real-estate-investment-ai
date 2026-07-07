# Локальный запуск на Windows

Этот файл описывает стабильный локальный запуск проекта без активации виртуального окружения через `Activate.ps1`. Все команды выполняются из корня репозитория:

```powershell
C:\Users\ant_o\Documents\Codex\2026-06-23\real-estate-investment-ai
```

## Требования

- Python
- Node.js
- `npm.cmd`
- Git
- Windows PowerShell

## Первый запуск

Создайте виртуальное окружение, если его еще нет:

```powershell
python -m venv .venv
```

Установите зависимости backend:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Установите зависимости frontend:

```powershell
cd frontend
npm.cmd install
cd ..
```

## Запуск backend

Рекомендуемый запуск через скрипт:

```powershell
.\scripts\start_backend.ps1
```

Прямая команда без скрипта:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Оставьте окно PowerShell открытым, пока backend нужен для работы.

## Запуск frontend

Рекомендуемый запуск через скрипт:

```powershell
.\scripts\start_frontend.ps1
```

Прямая команда без скрипта:

```powershell
cd frontend
npm.cmd run dev
```

Оставьте окно PowerShell открытым, пока frontend нужен для работы.

## Локальные URL

- Backend dashboard API: http://127.0.0.1:8000/api/v1/dashboard/properties
- Frontend: http://localhost:3000
- Backend docs, если backend запущен: http://127.0.0.1:8000/docs

## Проверка окружения

Можно быстро проверить версии инструментов, наличие `.venv`, `node_modules` и занятость портов:

```powershell
.\scripts\check_env.ps1
```

## Тесты

Основная команда:

```powershell
python -m pytest backend/tests
```

Если нужен Python из виртуального окружения:

```powershell
.\.venv\Scripts\python.exe -m pytest backend/tests
```

## PowerShell и Activate.ps1

Если PowerShell блокирует `.venv\Scripts\Activate.ps1`, не используйте активацию. Запускайте Python напрямую:

```powershell
.\.venv\Scripts\python.exe -m pytest backend/tests
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Если PowerShell блокирует запуск самих `.ps1` скриптов, используйте прямые команды из этого документа или разовый запуск с обходом политики только для текущей команды:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_backend.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\start_frontend.ps1
```

## npm в PowerShell

Если PowerShell блокирует `npm.ps1`, используйте `npm.cmd`:

```powershell
npm.cmd install
npm.cmd run dev
```

## Частые проблемы

### Порт 8000 занят

Backend не запустится, если порт уже слушает другой процесс. Закройте старое окно backend или найдите процесс:

```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen
```

### Порт 3000 занят

Next.js может предложить другой порт, например `3001`. Если нужен именно `3000`, закройте старое окно frontend или найдите процесс:

```powershell
Get-NetTCPConnection -LocalPort 3000 -State Listen
```

### Backend недоступен

Проверьте, что окно `.\scripts\start_backend.ps1` открыто и в нем нет ошибки. Затем откройте:

```text
http://127.0.0.1:8000/api/v1/dashboard/properties
```

### Frontend недоступен

Проверьте, что окно `.\scripts\start_frontend.ps1` открыто и команда `npm.cmd run dev` не завершилась с ошибкой. Затем откройте:

```text
http://localhost:3000
```

### Hydration error в браузере

Иногда hydration error появляется из-за расширений браузера, которые меняют HTML страницы. Проверьте страницу в режиме инкогнито или временно отключите расширения.

### `.git/index.lock`

Файл `.git/index.lock` может остаться после прерванной операции Git. Перед удалением убедитесь, что `git add`, `git commit`, `git pull` или `git push` больше не выполняются.

### Access denied в `.git`

Обычно это проблема прав Windows или заблокированных файлов, а не ошибка проекта. Закройте редакторы и терминалы, которые используют репозиторий, и проверьте права.

## Если Codex или Git получает Access denied

Безопасная последовательность действий:

1. Закройте Codex, VS Code и окна PowerShell, которые используют репозиторий.
2. Откройте PowerShell от имени администратора.
3. Выполните:

```powershell
$repo = "C:\Users\ant_o\Documents\Codex\2026-06-23\real-estate-investment-ai"
cd $repo
takeown /F $repo /R /D Y
icacls $repo /grant "$($env:USERNAME):(OI)(CI)F" /T
attrib -R -S -H "$repo*" /S /D
Remove-Item -Force "$repo\.git\index.lock" -ErrorAction SilentlyContinue
git status --short
```

4. При необходимости заново откройте Codex от имени администратора.

`Access denied` чаще всего означает, что Windows держит файл заблокированным или у пользователя не хватает прав на часть рабочей папки. Сгенерированные папки не нужно добавлять в коммит.

## Git workflow

Проверьте статус:

```powershell
git status --short
```

Добавляйте только релевантные файлы:

```powershell
git add .gitignore README.md PROJECT_STATUS.md docs/local-run.md pytest.ini frontend/eslint.config.mjs frontend/package-lock.json scripts/start_backend.ps1 scripts/start_frontend.ps1 scripts/check_env.ps1 scripts/git_status.ps1
```

Создайте коммит:

```powershell
git commit -m "Stabilize local development environment"
```

Отправьте изменения:

```powershell
git push origin main
```

Не добавляйте runtime/cache папки:

- `frontend/node_modules/`
- `frontend/.next/`
- `.venv/`
- `backend/**/__pycache__/`
- `.pytest_cache/`
