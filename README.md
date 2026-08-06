# 🎬 Cinema Tickets - Online Booking Platform

Платформа для поиска, бронирования и онлайн-покупки билетов в кино.

## 📋 Описание

Единая платформа включает:
- 🌐 Веб-сайт (React/Next.js)
- 🤖 Telegram-бот (aiogram 3)
- ⚙️ Административная панель
- 🗄 PostgreSQL база данных
- 💳 Онлайн-оплата (Stripe)
- 🎟 Электронные билеты
- 📱 QR-коды для проверки

## 🏗 Архитектура

```
Веб-сайт → FastAPI Backend ← Telegram Bot
              ↓
          PostgreSQL
              ↓
     Платежи & Админ-панель
```

## 📁 Структура проекта

```
cinema-tickets/
├── backend/              # FastAPI приложение
│   ├── app/
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   └── requirements.txt
├── frontend/             # React/Next.js приложение
│   ├── pages/
│   ├── components/
│   ├── styles/
│   └── package.json
├── telegram_bot/         # Telegram Bot (aiogram)
│   ├── handlers/
│   ├── keyboards/
│   └── requirements.txt
├── admin/                # Admin Panel
├── docker-compose.yml
├── .env.example
└── docs/                 # Документация
```

## 🚀 Быстрый старт

### 1. Клонируем репозиторий
```bash
git clone https://github.com/Pack6712/cinema-tickets.git
cd cinema-tickets
```

### 2. Создаём .env файл
```bash
cp .env.example .env
```

### 3. Запускаем Docker
```bash
docker-compose up -d
```

### 4. Создаём базу данных
```bash
docker-compose exec backend alembic upgrade head
```

## 🛠 Технологический стек

### Backend
- Python 3.10+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic

### Frontend
- React / Next.js
- TypeScript
- Tailwind CSS
- Axios

### Telegram Bot
- Python 3.10+
- aiogram 3
- asyncio

### DevOps
- Docker
- Docker Compose
- Nginx
- Ubuntu/Linux

## 📊 Этапы разработки

Всего 30 этапов. Отслеживаются через GitHub Issues.

1. Архитектура & ТЗ
2. PostgreSQL модели
3. FastAPI сервер
4. Авторизация
5. Фильмы
6. Кинотеатры
7. Залы
8. Места
9. Сеансы
10. Бронирование
... и далее

## 👥 Роли пользователей

- **USER** - покупатель билетов
- **STAFF** - сотрудник кинотеатра (проверка билетов)
- **ADMIN** - управление контентом
- **SUPERADMIN** - полный контроль

## 💳 Безопасность

- ✅ HTTPS
- ✅ Хеширование паролей (bcrypt)
- ✅ JWT токены
- ✅ Защита от двойного бронирования
- ✅ Webhook подпись (платежи)
- ✅ Rate limiting
- ✅ Audit logs
- ✅ Секреты в .env (не в коде!)

## 📝 Лицензия

MIT

---

**Разработка начата:** 2026-08-06
**Статус:** 🔨 В разработке
