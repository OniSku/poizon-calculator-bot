# Poizon Price Calculator Bot

A Telegram bot designed to automate price calculations for the Poizon marketplace. Built as a production-ready solution for logistics and dropshipping businesses.

## Tech Stack
- Python 3.12
- aiogram 3.x (Asynchronous framework)
- SQLAlchemy 2.0 (Modern ORM)
- PostgreSQL (Reliable RDBMS)
- Docker & Docker Compose

## Key Features
- Finite State Machine (FSM): User-friendly flow for category selection and price input.
- Dynamic Calculations: Automatic cost estimation based on CNY rate, shipping fees, and service commission.
- Database Integration: Every calculation is logged in PostgreSQL for analytics.
- Admin Notifications: Real-time alerts for the administrator upon new user queries.

## Calculation Logic
Total (RUB) = (Price in CNY * Exchange Rate) + Shipping + Commission
$$Total = (Price_{CNY} \times Rate) + Shipping + Commission$$