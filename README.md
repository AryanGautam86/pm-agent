# PM Agent

An AI-powered Project Management Assistant built using FastAPI, React, and Google Gemini.

## Features

- Create projects
- Create tasks
- Update task status
- Update task priority
- Update due date
- Delete tasks
- Delete projects
- Dashboard with project progress
- AI-powered natural language commands

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- Google Gemini API

### Frontend
- React
- Vite
- Tailwind CSS

## Local Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Deployment

- Backend: Render
- Frontend: Vercel / Render