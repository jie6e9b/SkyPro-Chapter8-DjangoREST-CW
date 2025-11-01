# 🚀 CI/CD Setup Guide

Пошаговая инструкция по настройке GitHub Actions CI/CD для автоматического деплоя проекта Habits API.

---

## 📋 Содержание

1. [Архитектура CI/CD](#архитектура-cicd)
2. [Предварительные требования](#предварительные-требования)
3. [Настройка Docker Hub](#настройка-docker-hub)
4. [Настройка сервера](#настройка-сервера)
5. [Настройка GitHub Secrets](#настройка-github-secrets)
6. [Запуск первого деплоя](#запуск-первого-деплоя)
7. [Troubleshooting](#troubleshooting)

---

## 🏗️ Архитектура CI/CD

При пуше в ветку `feature-1` запускается pipeline:

```
Push → Lint → Test → Build Docker → Push to Hub → Deploy → Notify
  ↓      ↓      ↓         ↓              ↓           ↓        ↓
  ✓    flake8  pytest   Dockerfile   DockerHub   SSH+Deploy  Success
```

### Этапы pipeline:

1. **Lint** - проверка кода линтерами (flake8)
2. **Test** - запуск тестов с PostgreSQL и Redis
3. **Build** - сборка Docker образа
4. **Push** - загрузка образа в Docker Hub
5. **Deploy** - деплой на сервер через SSH
6. **Notify** - уведомление о результате

---

## ✅ Предварительные требования

### На вашей машине:

- [x] Git установлен
- [x] Docker и Docker Compose установлены
- [x] SSH ключ для доступа к серверу

### На сервере:

- [x] Ubuntu 20.04+ (или другой Linux)
- [x] Docker и Docker Compose установлены
- [x] Открыты порты 80, 443 (для HTTP/HTTPS)
- [x] SSH доступ с ключом

---

## 🐳 Настройка Docker Hub

### 1. Создайте аккаунт на Docker Hub

Перейдите на https://hub.docker.com и зарегистрируйтесь.

### 2. Создайте репозиторий

1. Нажмите **Create Repository**
2. Имя: `habits-api` (или другое)
3. Видимость: `Public` или `Private`
4. Нажмите **Create**

### 3. Создайте Access Token

1. Перейдите в **Account Settings** → **Personal Access Token** →
2. Нажмите **Generate New Token**
3. Описание: `GitHub Actions`
4. Права: `Read, Write, Delete`
5. Нажмите **Generate**
6. **Сохраните токен!** (он больше не будет показан)

---

## 🖥️ Настройка сервера

### 1. Подключитесь к серверу

```bash
ssh user@your-server-ip
```

### 2. Установите Docker и Docker Compose

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезагрузка (или logout/login)
sudo reboot
```

### 3. Создайте директорию для проекта

```bash
# Создание директории
mkdir -p /home/$USER/habits-api
cd /home/$USER/habits-api

# Клонирование репозитория (опционально, если нужны конфиги)
# git clone https://github.com/your-username/your-repo.git .
```

### 4. Создайте .env.prod файл

```bash
nano .env.prod
```

Скопируйте содержимое из `.env.prod.example` и заполните реальными значениями:

```bash
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-server-ip

POSTGRES_DB=habits_prod
POSTGRES_USER=habits_user
POSTGRES_PASSWORD=strong-password-here
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

ACCESS_TOKEN_MINUTES=60
REFRESH_TOKEN_DAYS=7
PAGE_SIZE=10

TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

Сохраните (Ctrl+O, Enter, Ctrl+X).

### 5. Скопируйте docker-compose.prod.yml на сервер

```bash
# На локальной машине
scp docker-compose.prod.yml user@your-server-ip:/home/user/habits-api/docker-compose.yml
scp nginx.conf user@your-server-ip:/home/user/habits-api/
```

Или создайте файлы вручную на сервере.

### 6. Настройте файрвол (опционально)

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

---

## 🔐 Настройка GitHub Secrets

### 1. Перейдите в настройки репозитория

```
GitHub → Ваш репозиторий → Settings → Secrets and variables → Actions
```

### 2. Добавьте следующие секреты:

Нажмите **New repository secret** для каждого:

#### Docker Hub:

| Имя секрета | Значение | Описание |
|------------|---------|----------|
| `DOCKERHUB_USERNAME` | `your-dockerhub-username` | Ваш username на Docker Hub |
| `DOCKERHUB_TOKEN` | `dckr_pat_xxxxx...` | Access Token из Docker Hub |

#### Сервер:

| Имя секрета | Значение | Описание |
|------------|---------|----------|
| `SERVER_HOST` | `123.45.67.89` | IP адрес или домен сервера |
| `SERVER_USER` | `username` | SSH пользователь (обычно `ubuntu` или ваш юзер) |
| `SERVER_PORT` | `22` | SSH порт (по умолчанию 22) |
| `SERVER_SSH_KEY` | `-----BEGIN OPENSSH...` | Приватный SSH ключ (см. ниже) |
| `DEPLOY_PATH` | `/home/user/habits-api` | Путь к проекту на сервере |

### 3. Получение SSH ключа

#### Если у вас НЕТ SSH ключа:

```bash
# На локальной машине
ssh-keygen -t ed25519 -C "github-actions"

# Просмотр приватного ключа
cat ~/.ssh/id_ed25519

# Просмотр публичного ключа
cat ~/.ssh/id_ed25519.pub
```

#### Копирование публичного ключа на сервер:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@your-server-ip
```

Или вручную:

```bash
# На сервере
mkdir -p ~/.ssh
nano ~/.ssh/authorized_keys
# Вставьте содержимое ~/.ssh/id_ed25519.pub
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

#### Добавление приватного ключа в GitHub Secrets:

1. Скопируйте **весь** приватный ключ:
   ```bash
   cat ~/.ssh/id_ed25519
   ```

2. В GitHub Secrets → New secret:
   - Name: `SERVER_SSH_KEY`
   - Value: вставьте весь ключ (включая `-----BEGIN OPENSSH PRIVATE KEY-----` и `-----END OPENSSH PRIVATE KEY-----`)

---

## 🚀 Запуск первого деплоя

### 1. Проверьте настройки

Убедитесь, что:
- ✅ Все GitHub Secrets добавлены
- ✅ Docker Hub репозиторий создан
- ✅ Сервер настроен
- ✅ SSH доступ работает

### 2. Создайте ветку feature-1

```bash
# Локально
git checkout -b feature-1

# Добавьте изменения
git add .
git commit -m "Setup CI/CD pipeline"

# Запушьте в GitHub
git push origin feature-1
```

### 3. Наблюдайте за выполнением

1. Перейдите в GitHub → **Actions**
2. Вы увидите запущенный workflow **CI/CD Pipeline**
3. Кликните на него, чтобы видеть прогресс

### 4. Проверьте результат

После успешного деплоя:

```bash
# Проверьте, что приложение работает
curl http://your-server-ip/api/schema/

# Проверьте Docker контейнеры на сервере
ssh user@your-server-ip
docker ps
```

---

## 🐛 Troubleshooting

### Проблема: Тесты падают в CI

**Решение:**
- Проверьте логи в GitHub Actions
- Убедитесь, что `.env` файл создается корректно в workflow
- Проверьте совместимость версий зависимостей

### Проблема: Docker login failed

**Решение:**
- Проверьте, что `DOCKERHUB_TOKEN` - это Access Token, а не пароль
- Убедитесь, что username написан правильно (без `@`)

### Проблема: SSH connection failed

**Решение:**
- Проверьте, что SSH ключ скопирован полностью (с заголовками)
- Проверьте, что публичный ключ добавлен в `~/.ssh/authorized_keys` на сервере
- Проверьте права: `chmod 600 ~/.ssh/authorized_keys`
- Попробуйте подключиться вручную: `ssh -i ~/.ssh/id_ed25519 user@server-ip`

### Проблема: Deploy timeout

**Решение:**
- Увеличьте таймаут в workflow (добавьте `timeout-minutes: 30`)
- Проверьте, что сервер не перегружен
- Проверьте интернет-соединение сервера

### Проблема: Permission denied при deploy

**Решение:**
- Убедитесь, что пользователь в группе `docker`: `sudo usermod -aG docker $USER`
- Перезайдите в SSH: `logout` и зайдите снова
- Проверьте права на директорию: `sudo chown -R $USER:$USER /home/$USER/habits-api`

### Проблема: Миграции не применяются

**Решение:**
```bash
# На сервере вручную
cd /home/$USER/habits-api
docker-compose exec web python manage.py migrate
```

---

## 🎯 Следующие шаги

После успешного деплоя:

1. **Настройте SSL (HTTPS)**:
   ```bash
   # Установка certbot
   sudo apt install certbot python3-certbot-nginx

   # Получение сертификата
   sudo certbot --nginx -d your-domain.com
   ```

2. **Настройте мониторинг** (Prometheus, Grafana, Sentry)

3. **Настройте бэкапы БД**:
   ```bash
   # Создайте cron job для бэкапа PostgreSQL
   crontab -e
   # Добавьте: 0 2 * * * docker-compose exec -T db pg_dump -U habits_user habits_prod > /backups/db_$(date +\%Y\%m\%d).sql
   ```

4. **Настройте уведомления** (Slack, Telegram, Email)

5. **Добавьте staging окружение** для тестирования перед продакшеном

---

## 📚 Дополнительные ресурсы

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

## 🆘 Нужна помощь?

Если что-то не работает:
1. Проверьте логи в GitHub Actions
2. Проверьте логи на сервере: `docker-compose logs`
3. Создайте Issue в репозитории

---

**Готово!** 🎉 Теперь при каждом пуше в `feature-1` будет автоматически:
- Проверяться код линтерами
- Запускаться тесты
- Собираться Docker образ
- Деплоиться на сервер

Удачи! 🚀
