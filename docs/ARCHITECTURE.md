# 🏗 Архитектура Cinema Tickets

## Общая структура системы

```
┌─────────────────────────────────────────────────────────────┐
│                     ПОЛЬЗОВАТЕЛЬ                             │
└────────────────┬──────────────────────────┬────────────────┘
                 │                          │
          ┌──────▼──────┐            ┌──────▼──────┐
          │   Веб-сайт  │            │ Telegram Bot│
          │  (Next.js)  │            │  (aiogram)  │
          └──────┬──────┘            └──────┬──────┘
                 │                          │
                 └──────────────┬───────────┘
                                │
                    ┌───────────▼──────────┐
                    │   FastAPI Backend    │
                    │    (Python)          │
                    └───────────┬──────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
         ┌──────▼──────┐   ┌────▼────┐   ┌─────▼──────┐
         │ PostgreSQL  │   │ Stripe   │   │ Admin Panel│
         │  Database   │   │  (API)   │   │  (React)   │
         └─────────────┘   └──────────┘   └────────────┘
```

## Слои приложения

### 1. **Presentation Layer** (Представление)
- 🌐 **Веб-сайт** (React/Next.js)
  - Главная страница
  - Каталог фильмов
  - Выбор мест
  - Оформление заказа
  - Профиль пользователя

- 🤖 **Telegram Bot** (aiogram)
  - Меню и навигация
  - Покупка билетов
  - Профиль и история
  - Уведомления

- ⚙️ **Admin Panel** (React)
  - Управление фильмами
  - Управление кинотеатрами
  - Просмотр заказов
  - Аналитика

### 2. **Application Layer** (Приложение)
**FastAPI Backend**
- Авторизация (JWT)
- Управление пользователями
- API endpoints для всех сущностей
- Бизнес-логика
- Обработка платежей (Stripe Webhook)
- Генерация QR-кодов

### 3. **Data Layer** (Данные)
**PostgreSQL Database**
- Таблицы пользователей
- Таблицы фильмов и сеансов
- Таблицы кинотеатров и залов
- Таблицы заказов и билетов
- Таблицы платежей

## База данных - Основные таблицы

```
users
├── id (PK)
├── username
├── email
├── password_hash
├── telegram_id
├── role (USER, STAFF, ADMIN, SUPERADMIN)
├── created_at
└── updated_at

movies
├── id (PK)
├── title
├── description
├── poster_url
├── trailer_url
├── genre_id (FK)
├── duration
├── age_rating
├── rating
└── release_date

cinemas
├── id (PK)
├── name
├── city
├── address
├── phone
└── description

halls
├── id (PK)
├── cinema_id (FK)
├── name
├── capacity
└── hall_type

seats
├── id (PK)
├── hall_id (FK)
├── row_number
├── seat_number
├── seat_type (STANDARD, VIP, PREMIUM)
└── status (AVAILABLE, RESERVED, SOLD)

sessions
├── id (PK)
├── movie_id (FK)
├── hall_id (FK)
├── date
├── time
└── status

session_prices
├── id (PK)
├── session_id (FK)
├── seat_type
└── price

reservations
├── id (PK)
├── session_id (FK)
├── seat_id (FK)
├── user_id (FK)
├── reserved_at
└── expires_at

orders
├── id (PK)
├── user_id (FK)
├── total_price
├── status (PENDING, RESERVED, PAID, CANCELLED)
├── created_at
└── paid_at

order_items
├── id (PK)
├── order_id (FK)
├── seat_id (FK)
└── price

payments
├── id (PK)
├── order_id (FK)
├── stripe_payment_id
├── amount
├── status (PENDING, SUCCEEDED, FAILED)
├── payment_method
├── created_at
└── paid_at

tickets
├── id (PK)
├── order_id (FK)
├── qr_code
├── status (ACTIVE, USED, CANCELLED)
├── created_at
└── used_at

favorites
├── id (PK)
├── user_id (FK)
├── movie_id (FK)
└── created_at

reviews
├── id (PK)
├── user_id (FK)
├── movie_id (FK)
├── rating (1-5)
├── text
└── created_at
```

## API Endpoints (основные)

### Auth
- `POST /api/auth/register` - Регистрация
- `POST /api/auth/login` - Вход
- `POST /api/auth/logout` - Выход
- `POST /api/auth/refresh` - Обновление токена

### Movies
- `GET /api/movies` - Список фильмов
- `GET /api/movies/{id}` - Детали фильма
- `POST /api/movies` - Создать (только admin)
- `PUT /api/movies/{id}` - Редактировать (только admin)

### Cinemas
- `GET /api/cinemas` - Список кинотеатров
- `GET /api/cinemas/{id}` - Детали

### Sessions
- `GET /api/sessions?movie_id=...&date=...` - Сеансы
- `GET /api/sessions/{id}` - Детали сеанса

### Seats
- `GET /api/sessions/{id}/seats` - Места в зале
- `POST /api/reservations` - Забронировать место

### Orders
- `POST /api/orders` - Создать заказ
- `GET /api/orders/{id}` - Детали заказа
- `GET /api/orders` - Мои заказы

### Payments
- `POST /api/payments` - Создать платёж
- `POST /api/payments/webhook` - Webhook от Stripe

### Tickets
- `GET /api/tickets/{id}` - Билет
- `GET /api/tickets` - Мои билеты
- `POST /api/tickets/{id}/verify` - Проверить QR

## Безопасность

### Аутентификация
- JWT токены (access_token + refresh_token)
- HttpOnly cookies
- CORS настроена

### Авторизация
- Роли: USER, STAFF, ADMIN, SUPERADMIN
- Проверка прав доступа на каждом endpoint

### Платежи
- Stripe API для обработки карт
- Webhook подпись
- Данные карты не сохраняются
- Webhook шифруется

### Данные
- Пароли хешируются (bcrypt)
- SQL injection защита (SQLAlchemy ORM)
- Rate limiting на endpoints

## Поток покупки билета

```
1. Пользователь открывает сайт/Telegram
   ↓
2. Выбирает город → фильм → кинотеатр
   ↓
3. Выбирает дату → сеанс
   ↓
4. Видит схему зала (GET /api/sessions/{id}/seats)
   ↓
5. Выбирает места
   ↓
6. Резервирует места (POST /api/reservations)
   ↓
7. Места становятся RESERVED (на 10 минут)
   ↓
8. Создаёт заказ (POST /api/orders)
   ↓
9. Вводит данные карты через Stripe Form
   ↓
10. Отправляет платёж (POST /api/payments)
   ↓
11. Stripe обрабатывает платёж
   ↓
12. Stripe отправляет webhook (POST /api/payments/webhook)
   ↓
13. Backend обновляет статус заказа → PAID
   ↓
14. Места → SOLD
   ↓
15. Создаёт билет с QR (POST /api/tickets)
   ↓
16. Пользователь получает билет
```

## Развёртывание

```
Production Server (Ubuntu 20.04)
├── Docker
├── Docker Compose
├── PostgreSQL (контейнер)
├── FastAPI Backend (контейнер)
├── Telegram Bot (контейнер)
├── Next.js Frontend (статика)
├── Nginx (reverse proxy)
└── SSL (Let's Encrypt)
```

---

**Версия:** 1.0.0  
**Дата:** 2026-08-06
