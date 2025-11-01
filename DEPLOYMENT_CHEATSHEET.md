# 🚀 Deployment Cheatsheet

Краткая шпаргалка по деплою и управлению проектом.

---

## 📦 Docker Hub

```bash
# Логин в Docker Hub
docker login -u your-username

# Сборка образа
docker build -f Dockerfile.prod -t your-username/habits-api:latest .

# Пуш образа
docker push your-username/habits-api:latest

# Пулл образа
docker pull your-username/habits-api:latest
```

---

## 🖥️ Команды на сервере

### Управление контейнерами

```bash
# Перейти в директорию проекта
cd /home/$USER/habits-api

# Запустить все сервисы
docker-compose up -d

# Остановить все сервисы
docker-compose down

# Перезапустить конкретный сервис
docker-compose restart web

# Посмотреть логи
docker-compose logs -f web
docker-compose logs -f celery
docker-compose logs --tail=100 web

# Посмотреть статус контейнеров
docker-compose ps

# Обновить контейнеры (пулл новых образов)
docker-compose pull
docker-compose up -d
```

### Django команды

```bash
# Применить миграции
docker-compose exec web python manage.py migrate

# Создать миграции
docker-compose exec web python manage.py makemigrations

# Создать суперпользователя
docker-compose exec web python manage.py createsuperuser

# Собрать статику
docker-compose exec web python manage.py collectstatic --noinput

# Django shell
docker-compose exec web python manage.py shell

# Проверка конфигурации
docker-compose exec web python manage.py check
```

### База данных

```bash
# Зайти в PostgreSQL
docker-compose exec db psql -U habits_user -d habits_prod

# Бэкап БД
docker-compose exec -T db pg_dump -U habits_user habits_prod > backup_$(date +%Y%m%d).sql

# Восстановление БД из бэкапа
docker-compose exec -T db psql -U habits_user habits_prod < backup_20241026.sql

# Посмотреть размер БД
docker-compose exec db psql -U habits_user -d habits_prod -c "SELECT pg_size_pretty(pg_database_size('habits_prod'));"
```

### Очистка

```bash
# Удалить неиспользуемые образы
docker image prune -a

# Удалить неиспользуемые volumes
docker volume prune

# Полная очистка (осторожно!)
docker system prune -a --volumes
```

---

## 🔄 Git & GitHub Actions

### Локально

```bash
# Переключиться на feature-1
git checkout feature-1

# Добавить изменения
git add .
git commit -m "Your message"

# Запушить (триггерит CI/CD)
git push origin feature-1

# Посмотреть логи
git log --oneline -10
```

### GitHub Actions

```bash
# Просмотр workflow runs
gh run list --workflow=ci-cd.yml

# Просмотр конкретного run
gh run view <run-id>

# Перезапуск failed workflow
gh run rerun <run-id>

# Посмотреть логи
gh run view <run-id> --log
```

---

## 🔐 SSH

```bash
# Подключиться к серверу
ssh user@your-server-ip

# Скопировать файл на сервер
scp file.txt user@server:/path/to/destination

# Скопировать файл с сервера
scp user@server:/path/to/file.txt ./local-path

# Скопировать директорию
scp -r ./directory user@server:/path/to/destination

# Проверить SSH ключ
ssh-keygen -l -f ~/.ssh/id_ed25519.pub
```

---

## 📊 Мониторинг

### Системные ресурсы

```bash
# Использование CPU/RAM
docker stats

# Использование диска
df -h

# Топ процессов
htop  # или top

# Проверка портов
netstat -tulpn | grep LISTEN
# или
ss -tulpn | grep LISTEN
```

### Логи

```bash
# Системные логи
journalctl -u docker -f

# Nginx логи
docker-compose exec nginx tail -f /var/log/nginx/access.log
docker-compose exec nginx tail -f /var/log/nginx/error.log

# Celery логи
docker-compose logs -f celery
docker-compose logs -f celery-beat
```

### Health checks

```bash
# Проверка API
curl http://localhost:8000/api/schema/

# Проверка БД
docker-compose exec db pg_isready

# Проверка Redis
docker-compose exec redis redis-cli ping
```

---

## 🐛 Troubleshooting

### Контейнер не запускается

```bash
# Посмотреть детальные логи
docker-compose logs web

# Зайти в контейнер
docker-compose exec web bash

# Проверить переменные окружения
docker-compose exec web env | grep POSTGRES
```

### Миграции не применяются

```bash
# Посмотреть список миграций
docker-compose exec web python manage.py showmigrations

# Применить миграции вручную
docker-compose exec web python manage.py migrate

# Откатить миграцию
docker-compose exec web python manage.py migrate app_name 0001
```

### Проблемы с правами

```bash
# Исправить права на файлы
sudo chown -R $USER:$USER /home/$USER/habits-api

# Добавить пользователя в группу docker
sudo usermod -aG docker $USER

# Перезайти в систему
logout  # и войти снова
```

### Контейнер падает

```bash
# Проверить статус
docker-compose ps

# Перезапустить
docker-compose restart web

# Пересобрать и запустить
docker-compose up -d --build --force-recreate web
```

---

## 🔥 Быстрые команды

### Полный перезапуск

```bash
cd /home/$USER/habits-api
docker-compose down
docker-compose pull
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose ps
```

### Обновление после изменений кода

```bash
# На локальной машине
git push origin feature-1

# На сервере (если нужно вручную)
cd /home/$USER/habits-api
docker-compose pull
docker-compose up -d
```

### Откат к предыдущей версии

```bash
# Найти предыдущий тег образа
docker images | grep habits-api

# Обновить docker-compose.yml с нужным тегом
nano docker-compose.yml
# Изменить: image: username/habits-api:old-commit-sha

# Запустить
docker-compose up -d
```

---

## 📱 Telegram уведомления

### Добавление Telegram бота в workflow

1. Создайте бота через @BotFather
2. Получите токен
3. Добавьте в GitHub Secrets: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
4. Добавьте в workflow:

```yaml
- name: Send Telegram notification
  if: always()
  run: |
    STATUS="${{ job.status }}"
    MESSAGE="🚀 Deployment $STATUS for commit ${{ github.sha }}"
    curl -s -X POST https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage \
      -d chat_id=${{ secrets.TELEGRAM_CHAT_ID }} \
      -d text="$MESSAGE"
```

---

## 🔒 Безопасность

### Обновление зависимостей

```bash
# Локально
pip list --outdated
pip install --upgrade package-name

# Обновить requirements
pip freeze > requirements.txt

# В Docker
docker-compose exec web pip list --outdated
```

### Проверка уязвимостей

```bash
# Установка safety
pip install safety

# Проверка
safety check -r requirements.txt
```

### Смена секретов

```bash
# 1. Сгенерировать новый SECRET_KEY
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# 2. Обновить на сервере
nano .env.prod

# 3. Перезапустить
docker-compose restart web
```

---

## 📈 Производительность

### Масштабирование

```bash
# Увеличить количество workers
docker-compose up -d --scale celery=3

# Изменить количество gunicorn workers
# В docker-compose.yml изменить: --workers 8
```

### Кэширование

```bash
# Очистить Redis кэш
docker-compose exec redis redis-cli FLUSHALL
```

---

## 🎯 Полезные алиасы

Добавьте в `~/.bashrc` или `~/.zshrc`:

```bash
# Алиасы для Docker Compose
alias dc='docker-compose'
alias dcu='docker-compose up -d'
alias dcd='docker-compose down'
alias dcr='docker-compose restart'
alias dcl='docker-compose logs -f'
alias dcp='docker-compose ps'

# Алиасы для Django
alias dm='docker-compose exec web python manage.py'
alias dmm='docker-compose exec web python manage.py migrate'
alias dms='docker-compose exec web python manage.py shell'

# Быстрый деплой
alias deploy='cd /home/$USER/habits-api && docker-compose pull && docker-compose up -d && docker-compose exec web python manage.py migrate'
```

Затем:
```bash
source ~/.bashrc  # или ~/.zshrc
```

---

**Готово!** 📝 Сохраните эту шпаргалку для быстрого доступа к командам.
