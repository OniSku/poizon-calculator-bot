# Poizon Price Calculator Bot

> **NDA Notice**: The source code in this repository is a sanitized showcase version. The complete implementation, business logic, and client-specific configurations are proprietary and covered by a non-disclosure agreement.

A Telegram bot that automates price calculations for the Poizon marketplace. Targets logistics and dropshipping businesses.

## Tech Stack
- Python 3.12
- aiogram 3.x (Asynchronous framework)
- SQLAlchemy 2.0 (Modern ORM)
- PostgreSQL (Reliable RDBMS)
- Docker & Docker Compose

## Key Features
- Finite State Machine (FSM): Step-by-step flow for category selection and price input.
- Dynamic Calculations: Automatic cost estimation based on CNY rate, shipping fees, and service commission.
- Database Integration: Every calculation is logged in PostgreSQL for analytics.
- Admin Notifications: Real-time alerts for the administrator upon new user queries.

## Calculation Logic
Total (RUB) = (Price in CNY * Exchange Rate) + Shipping + Commission
$$Total = (Price_{CNY} \times Rate) + Shipping + Commission$$