# 🐺 Werewolf Game - Automatic Realtime Host

An automated, realtime Werewolf game management system for offline multiplayer games. Host uses a central screen and audio, while players use their phones.

## 📋 Project Overview

This is a full-stack web application based on the SRS (Software Requirements Specification) in `docs/SRS.md`.

**Architecture:**
- **Frontend**: Vue 3 + Vite + TailwindCSS + Pinia (Vercel)
- **Backend**: Python FastAPI + WebSocket + SQLAlchemy (Render)
- **Database**: Supabase PostgreSQL
- **Realtime**: WebSocket for live synchronization

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.10+ (for backend)
- **PostgreSQL** (or Supabase)

### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Copy environment variables
copy .env.example .env
# Edit .env with your database URL and settings

# 6. Run the backend server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be running at: **http://localhost:8000**

API Documentation: **http://localhost:8000/docs**

### Frontend Setup

```bash
# 1. Navigate to frontend directory (from root)
cd frontend

# 2. Install dependencies
npm install

# 3. Run development server
npm run dev
```

Frontend will be available at: **http://localhost:5173**

## 📁 Project Structure

```
automatic-werewolf-offline-host/
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # Database connection
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic
│   │   ├── game_engine/         # Game logic
│   │   ├── websocket/           # WebSocket management
│   │   └── utils/               # Utilities
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/                     # Vue 3 + Vite frontend
│   ├── src/
│   │   ├── assets/              # Images, audio, styles
│   │   ├── components/          # Vue components
│   │   ├── pages/               # Page components
│   │   ├── stores/              # Pinia stores
│   │   ├── services/            # API & WebSocket
│   │   ├── types/               # TypeScript types
│   │   ├── App.vue
│   │   └── main.ts
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── docs/
│   └── SRS.md                   # Complete specification
│
├── README.md
└── .gitignore
```

## 🎮 MVP Features (Phase 1)

- ✅ Create and join rooms with room codes
- ✅ Setup role cart and random role assignment
- ✅ WebSocket realtime synchronization
- ✅ Night phase with role calls (Text-To-Speech)
- ✅ Ambient noise during night
- ✅ Day phase and vote system
- ✅ Win conditions (Village vs Werewolves)
- ✅ Support 10+ players per room

**MVP Roles:**
- Werewolf (Sói)
- Villager (Dân Làng)
- Protector (Bảo Vệ)
- Seer (Tiên Tri)
- Witch (Phù Thủy)

## 🔄 Running Both Frontend and Backend

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # or: source venv/bin/activate
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Both will run simultaneously. Frontend communicates with backend via HTTP API and WebSocket.

## 🛠️ Development Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run server with auto-reload
python -m uvicorn app.main:app --reload

# Run tests (when added)
pytest

# Format code
black app/

# Lint
flake8 app/
```

### Frontend
```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint and fix
npm run lint
```

## 📚 Documentation

- `docs/SRS.md` - Complete Software Requirements Specification
- API Documentation available at `http://localhost:8000/docs` (Swagger UI)

## 🗄️ Database Setup

The application uses Supabase PostgreSQL. To set up locally:

1. Create a PostgreSQL database
2. Update `DATABASE_URL` in `backend/.env`
3. Run migrations (Alembic - coming in next phase)

**Supabase Cloud:**
```
DATABASE_URL=postgresql://user:password@db.supabasehost.com/werewolf_db?sslmode=require
```

## 🚀 Deployment

### Frontend (Vercel)
```bash
cd frontend
npm run build
# Deploy dist/ folder to Vercel
```

### Backend (Render)
1. Push code to GitHub
2. Connect repository to Render
3. Set environment variables
4. Deploy from main branch

## 📖 Next Steps

1. **Phase 2**: Implement database models and REST API
2. **Phase 3**: Build WebSocket event system
3. **Phase 4**: Create game engine logic
4. **Phase 5**: Build UI components
5. **Phase 6**: Audio system implementation
6. **Phase 7**: Testing and deployment

## 🐛 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.10+)
- Verify venv is activated
- Check database URL in .env

### Frontend npm install fails
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Try `npm cache clean --force`

### WebSocket connection fails
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Verify frontend WebSocket URL matches backend

## 📝 License

Private project - Werewolf Game System

## 👥 Team

- Backend: FastAPI + PostgreSQL
- Frontend: Vue 3 + TailwindCSS
- Game Logic: Python
- Realtime: WebSocket

---

**Status**: 🟢 Ready for Development

**Last Updated**: May 31, 2026
