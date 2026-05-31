# 🚀 Project Setup Guide

## ✅ Project Structure Created

```
automatic-werewolf-offline-host/
│
├── 📁 backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              ✅ FastAPI server
│   │   ├── config.py            ✅ Configuration
│   │   ├── database.py          ✅ DB connection
│   │   ├── models/              ✅ SQLAlchemy models (placeholder)
│   │   ├── schemas/             ✅ Pydantic schemas (placeholder)
│   │   ├── routers/             ✅ API routes (placeholder)
│   │   ├── services/            ✅ Business logic (placeholder)
│   │   ├── game_engine/         ✅ Game logic (placeholder)
│   │   ├── websocket/           ✅ WebSocket (placeholder)
│   │   └── utils/               ✅ Utilities (placeholder)
│   ├── requirements.txt         ✅ Python dependencies
│   ├── .env.example             ✅ Environment template
│   └── Dockerfile               ✅ Container config
│
├── 📁 frontend/
│   ├── src/
│   │   ├── App.vue              ✅ Root component
│   │   ├── main.ts              ✅ Entry point
│   │   ├── index.css            ✅ TailwindCSS styles
│   │   ├── components/          ✅ Components (host, player, common)
│   │   ├── pages/               ✅ Page components
│   │   ├── stores/              ✅ Pinia stores
│   │   ├── services/            ✅ API/WebSocket services
│   │   ├── types/               ✅ TypeScript types
│   │   └── assets/              ✅ Audio & styles folders
│   ├── index.html               ✅ Entry HTML
│   ├── package.json             ✅ NPM dependencies
│   ├── vite.config.ts           ✅ Vite config
│   ├── tailwind.config.js       ✅ TailwindCSS config
│   ├── postcss.config.js        ✅ PostCSS config
│   ├── tsconfig.json            ✅ TypeScript config
│   ├── tsconfig.node.json       ✅ TS config for build
│   ├── .gitignore               ✅ Git ignore rules
│   └── Dockerfile               ✅ Container config
│
├── 📁 docs/
│   └── SRS.md                   ✅ Full specification
│
├── README.md                     ✅ Project documentation
├── .env.example                  ✅ Global env template
├── .gitignore                    ✅ Git ignore rules
└── .git/                         ✅ Git repository

```

---

## 📋 Installation & Run Commands

### **Step 1: Backend Setup**

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
copy .env.example .env
# Edit .env file - at minimum, set DATABASE_URL if using PostgreSQL
# For now, backend can run without a real database connection
```

### **Step 2: Run Backend Server**

```bash
# Make sure virtual environment is activated
# (you should see (venv) in your terminal)

# Run FastAPI server with auto-reload
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Or simply:
python -m uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete
```

**Backend is now available at:**
- 🌐 API: http://localhost:8000
- 📚 Documentation: http://localhost:8000/docs (Swagger UI)
- 🏥 Health Check: http://localhost:8000/health

---

### **Step 3: Frontend Setup**

**Open a NEW terminal (keep backend running in first terminal)**

```bash
# Navigate to frontend directory (from root)
cd frontend

# Install npm dependencies
npm install

# This installs:
# - Vue 3
# - Vite
# - TailwindCSS
# - Pinia
# - TypeScript
# - And all other dependencies
```

### **Step 4: Run Frontend Development Server**

```bash
# From frontend directory
npm run dev

# Or explicitly:
npm run dev -- --host
```

**Expected Output:**
```
  VITE v5.0.8  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

**Frontend is now available at:**
- 🌐 App: http://localhost:5173

---

## 🎯 Running Everything (Recommended Setup)

### **Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # On Windows
python -m uvicorn app.main:app --reload
```

### **Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Both should run simultaneously!

---

## ✨ Verification Checklist

After running both servers, verify:

- [ ] Backend responds to `http://localhost:8000/` → JSON response
- [ ] Backend docs at `http://localhost:8000/docs` → Swagger UI loads
- [ ] Frontend loads at `http://localhost:5173/` → Welcome page shows
- [ ] Frontend shows "Backend Status: http://localhost:8000"

---

## 🛠️ Useful Development Commands

### **Backend Commands**
```bash
# Install new package
pip install package-name

# Freeze dependencies
pip freeze > requirements.txt

# Format code
pip install black
black app/

# Lint code
pip install flake8
flake8 app/

# Run tests (when added)
pip install pytest
pytest
```

### **Frontend Commands**
```bash
# Install new package
npm install package-name

# Update all packages
npm update

# Build for production
npm run build

# Preview production build
npm run preview

# Format/lint code
npm run lint
```

---

## 📦 Docker Deployment Preview

When ready to deploy:

### **Build Backend Image:**
```bash
docker build -f backend/Dockerfile -t werewolf-backend:latest backend/
docker run -p 8000:8000 werewolf-backend:latest
```

### **Build Frontend Image:**
```bash
docker build -f frontend/Dockerfile -t werewolf-frontend:latest frontend/
docker run -p 80:80 werewolf-frontend:latest
```

---

## 🔧 Environment Setup (Optional)

To use a real PostgreSQL database:

### **Local PostgreSQL:**
```bash
# On Windows, edit backend/.env:
DATABASE_URL=postgresql://postgres:password@localhost/werewolf_db
```

### **Supabase Cloud:**
```bash
# Get connection string from Supabase dashboard
DATABASE_URL=postgresql://user:password@db.supabase.co/postgres?sslmode=require
```

---

## 🐛 Troubleshooting

### **Backend won't start**
```bash
# Check Python version (need 3.10+)
python --version

# Make sure venv is activated (you should see (venv) in terminal)
python -m venv venv
venv\Scripts\activate

# Try installing requirements again
pip install -r requirements.txt
```

### **Frontend npm install fails**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock
rm -rf node_modules package-lock.json

# Try again
npm install
```

### **Port already in use**
```bash
# Change backend port:
python -m uvicorn app.main:app --port 8001

# Change frontend port:
npm run dev -- --port 5174
```

### **CORS errors in console**
- This is normal during development
- CORS is already configured in backend for localhost:5173

---

## 📚 Next Development Steps

1. ✅ **Structure Created** (You are here)
2. ⏭️ **Database Models** - Define SQLAlchemy models
3. ⏭️ **REST API** - Implement room, player, role endpoints
4. ⏭️ **WebSocket Server** - Setup real-time events
5. ⏭️ **Game Logic** - Implement game engine
6. ⏭️ **Frontend Pages** - Build UI components
7. ⏭️ **Audio System** - Add TTS and ambient sound
8. ⏭️ **Testing** - Add unit and integration tests
9. ⏭️ **Deployment** - Deploy to Render + Vercel + Supabase

---

## 📖 Documentation Files

- **[README.md](../README.md)** - Project overview
- **[docs/SRS.md](../docs/SRS.md)** - Complete specification
- **[Backend API Docs](http://localhost:8000/docs)** - Swagger UI (when server running)

---

## 🎮 Current Status

- ✅ Project Structure: Complete
- ✅ Backend: Ready to run
- ✅ Frontend: Ready to run
- ✅ Configuration: Ready
- 🔲 Database Models: Pending
- 🔲 API Endpoints: Pending
- 🔲 Game Logic: Pending
- 🔲 UI Components: Pending

---

**Ready to start development! 🚀**

Run the commands above in two terminal windows and you're good to go.
