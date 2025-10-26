# Pocket Budget Hero

A full-stack web application for budget tracking with environmental awareness.

## Prerequisites

1. Node.js (v18 or later) - [Download from nodejs.org](https://nodejs.org/)
2. Python 3.8 or later - [Download from python.org](https://python.org)

## Setup Instructions

### Backend (Python FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlmodel python-dotenv
   ```

4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at http://localhost:8000

### Frontend (React + TypeScript)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```
   The app will be available at http://localhost:5173

## Features

- Budget tracking with weekly limits
- AI-powered purchase assistant
- Environmental impact awareness
- Wishlist for sustainable alternatives
- Progress tracking with streaks
- Modern, responsive UI

## API Endpoints

- `GET /api/budget` - Get current budget
- `PUT /api/budget/{id}` - Update budget
- `GET /api/transactions` - List all transactions
- `POST /api/transactions` - Add new transaction
- `GET /api/wishlist` - List wishlist items
- `POST /api/wishlist` - Add wishlist item
- `PUT /api/wishlist/{id}` - Update wishlist item savings

## Development

The project is set up with:
- Frontend: Vite, React, TypeScript, TailwindCSS
- Backend: FastAPI, SQLModel, SQLite
- Development tools: ESLint, TypeScript, Uvicorn
