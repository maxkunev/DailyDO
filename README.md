# DailyDO

DailyDO is a Telegram-based personal productivity app that combines a chat bot with a Telegram Mini App for fast daily task management. The project is built as a full-stack product with a Django backend, a React frontend, a Telegram bot, and a separate scheduler service for automated reminders.[1][2]

## Overview

DailyDO is designed for simple everyday planning inside Telegram instead of a separate standalone app. A user can create tasks, view them in the Mini App, update their status, and receive scheduled reminders in Telegram chat.[3][2]

The system includes four main parts:
- Telegram bot for user interaction and reminders.[4][2]
- React Telegram Mini App for the main task interface.[5]
- Django REST API for authentication and task CRUD operations.[3]
- Scheduler service for morning and evening reminder jobs.[1][2]

## Features

- Telegram Mini App authentication flow.
- Task creation, editing, deletion, and completion toggling.[6][3]
- Daily reminders with separate morning and evening jobs.[1][2]
- User-based task isolation on the backend through authenticated queries.[3]
- Input validation for task text length on the backend, with the frontend adjusted accordingly during UI rework.[7][8]
- Docker-based local development with separate services for web, bot, database, scheduler, and frontend.[9]

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django, Django REST Framework |
| Frontend | React, Vite, Telegram Mini App UI integration |
| Bot | Python, aiogram |
| Database | PostgreSQL |
| Scheduler | APScheduler |
| Infrastructure | Docker Compose |

The project uses a service-oriented local architecture where the web app, bot, and scheduler run as separate processes. The scheduler is implemented as an async process with cron-based jobs and timezone support through `ZoneInfo`.[1][9]

## Architecture

The backend exposes authenticated task endpoints, and each task is bound to the current authenticated user. This prevents users from reading or mutating tasks that belong to someone else through direct object access.[3]

The scheduler runs independently from the bot and sends reminder messages through a dedicated sender layer. Morning and evening jobs collect unfinished tasks for the current date, group them by Telegram chat, and send localized reminder messages.[2]

## What was implemented

This version includes the transition from a prototype into a usable personal product. The work covered bot localization, React UI improvements, scheduler integration, reminder delivery, backend task validation, and general product hardening discussed during development.[5][1][2]

From an engineering perspective, the project demonstrates:
- backend API design and authentication;
- Telegram bot integration;
- React Mini App client development;
- scheduled background jobs;
- Docker-based multi-service setup;
- iterative product refinement based on real usage.

## Running locally

Typical local startup is done with Docker Compose so that all services run together.[9]

```bash
docker compose up --build
```

Expected services:
- `web` — Django API.[9]
- `bot` — Telegram bot process.[9]
- `scheduler` — reminder scheduler.[9]
- `db` — PostgreSQL database.[9]
- `frontend` — React Mini App frontend.[9]

The project also requires environment variables such as the Telegram bot token, database settings, API URL, and timezone configuration for scheduler jobs.[1][9]

## Why this project matters

DailyDO is not just a demo CRUD app. It is a practical product intended for real daily use, which shaped decisions around reminders, validation, privacy-minded data handling, and iterative UX improvements during development.

For hiring purposes, the project shows the ability to design and ship a small but complete product: from backend and frontend to automation, deployment preparation, and product iteration based on real feedback.[1][2]

## Status

This repository represents the first usable release of DailyDO. Future changes are expected to be driven by real-world usage feedback and further iteration after deployment.[1][2]
