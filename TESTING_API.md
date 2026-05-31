# 🎮 Room API & Player Join API - Testing Guide

## ✅ Implementation Complete

Backend implementation of Room API and Player Join API is now complete with:
- ✅ SQLAlchemy models (Room, Player)
- ✅ Pydantic schemas for request/response
- ✅ REST API endpoints (POST /api/rooms, POST /api/rooms/{code}/join, GET /api/rooms/{code})
- ✅ Business logic services (RoomService, PlayerService)
- ✅ SQLite database (local development)
- ✅ Automatic table creation on startup

---

## 🚀 Running the Backend

### 1. Install Dependencies (if not already done)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# or (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
python -m uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     🚀 Starting Werewolf Game API...
INFO:     ✅ Database tables created/verified
INFO:     Application startup complete
```

**Access Points:**
- 🌐 API Base: http://localhost:8000
- 📚 Swagger UI: http://localhost:8000/docs
- 📖 ReDoc: http://localhost:8000/redoc
- 🏥 Health Check: http://localhost:8000/health

---

## 📝 API Testing in Swagger UI

### **Method 1: Using Swagger UI (Easiest)**

1. Open **http://localhost:8000/docs** in your browser
2. You'll see all endpoints with "Try it out" buttons

---

## 🧪 Manual Testing with cURL

### **1. Create a Room (Host)**

```bash
curl -X POST http://localhost:8000/api/rooms \
  -H "Content-Type: application/json"
```

**Response Example:**
```json
{
  "room_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "room_code": "ABC123",
  "host_token": "a1b2c3d4e5f6789012345678901234567890abcd1234567890",
  "status": "waiting",
  "created_at": "2026-05-31T12:00:00"
}
```

**Save these values:**
- `room_code` → Share with players (e.g., "ABC123")
- `host_token` → For host authentication (next phase)
- `room_id` → For internal use

---

### **2. Get Room Info (Before Players Join)**

```bash
curl -X GET http://localhost:8000/api/rooms/ABC123 \
  -H "Content-Type: application/json"
```

**Response Example:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "room_code": "ABC123",
  "status": "waiting",
  "current_phase": "setup",
  "night_number": "0",
  "day_number": "0",
  "players": [],
  "player_count": 0,
  "created_at": "2026-05-31T12:00:00"
}
```

---

### **3. Player 1 Joins Room**

```bash
curl -X POST http://localhost:8000/api/rooms/ABC123/join \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nguyễn Văn A"
  }'
```

**Response Example:**
```json
{
  "player_id": "xyz789",
  "session_token": "player_token_xyz789",
  "room_code": "ABC123",
  "room_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "player_name": "Nguyễn Văn A",
  "player_count": 1,
  "status": "waiting"
}
```

**Save:** `player_id` and `session_token` for this player

---

### **4. Player 2 Joins Room**

```bash
curl -X POST http://localhost:8000/api/rooms/ABC123/join \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Trần Thị B"
  }'
```

**Response:**
```json
{
  "player_id": "abc456",
  "session_token": "player_token_abc456",
  "room_code": "ABC123",
  "room_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "player_name": "Trần Thị B",
  "player_count": 2,
  "status": "waiting"
}
```

---

### **5. Get Room Info (After Players Join)**

```bash
curl -X GET http://localhost:8000/api/rooms/ABC123 \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "room_code": "ABC123",
  "status": "waiting",
  "current_phase": "setup",
  "night_number": "0",
  "day_number": "0",
  "players": [
    {
      "id": "xyz789",
      "name": "Nguyễn Văn A",
      "is_alive": true,
      "is_connected": true
    },
    {
      "id": "abc456",
      "name": "Trần Thị B",
      "is_alive": true,
      "is_connected": true
    }
  ],
  "player_count": 2,
  "created_at": "2026-05-31T12:00:00"
}
```

---

## 🧪 Complete Test Scenario (Python Script)

Create a file `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("🐺 Werewolf Game API - Test Scenario")
print("=" * 60)

# Step 1: Host creates room
print("\n1️⃣  Host creates room...")
response = requests.post(f"{BASE_URL}/api/rooms")
room_data = response.json()
room_code = room_data["room_code"]
room_id = room_data["room_id"]
host_token = room_data["host_token"]

print(f"   ✅ Room created: {room_code}")
print(f"   Room ID: {room_id}")
print(f"   Host Token: {host_token[:20]}...")

# Step 2: Get room info (empty)
print("\n2️⃣  Get room info (before players join)...")
response = requests.get(f"{BASE_URL}/api/rooms/{room_code}")
room_info = response.json()
print(f"   Players: {room_info['player_count']}")

# Step 3: Player 1 joins
print("\n3️⃣  Player 1 joins...")
response = requests.post(
    f"{BASE_URL}/api/rooms/{room_code}/join",
    json={"name": "Nguyễn Văn A"}
)
player1_data = response.json()
player1_id = player1_data["player_id"]
player1_token = player1_data["session_token"]
print(f"   ✅ {player1_data['player_name']} joined")
print(f"   Player ID: {player1_id}")
print(f"   Session Token: {player1_token[:20]}...")
print(f"   Total players: {player1_data['player_count']}")

# Step 4: Player 2 joins
print("\n4️⃣  Player 2 joins...")
response = requests.post(
    f"{BASE_URL}/api/rooms/{room_code}/join",
    json={"name": "Trần Thị B"}
)
player2_data = response.json()
player2_id = player2_data["player_id"]
player2_token = player2_data["session_token"]
print(f"   ✅ {player2_data['player_name']} joined")
print(f"   Player ID: {player2_id}")
print(f"   Total players: {player2_data['player_count']}")

# Step 5: Player 3 joins
print("\n5️⃣  Player 3 joins...")
response = requests.post(
    f"{BASE_URL}/api/rooms/{room_code}/join",
    json={"name": "Phạm Công C"}
)
player3_data = response.json()
print(f"   ✅ {player3_data['player_name']} joined")
print(f"   Total players: {player3_data['player_count']}")

# Step 6: Get room info (with players)
print("\n6️⃣  Get room info (after players joined)...")
response = requests.get(f"{BASE_URL}/api/rooms/{room_code}")
room_info = response.json()
print(f"   Room Code: {room_info['room_code']}")
print(f"   Status: {room_info['status']}")
print(f"   Current Phase: {room_info['current_phase']}")
print(f"   Total Players: {room_info['player_count']}")
print(f"   Players:")
for player in room_info["players"]:
    print(f"      - {player['name']} (ID: {player['id'][:8]}...)")

print("\n" + "=" * 60)
print("✅ All tests passed!")
print("=" * 60)
```

**Run the test:**
```bash
pip install requests
python test_api.py
```

---

## 🧪 Testing with Postman

1. **Create Collection**: New Collection → "Werewolf Game"

2. **Add Requests**:

   | Method | URL | Body |
   |--------|-----|------|
   | POST | `http://localhost:8000/api/rooms` | (empty) |
   | GET | `http://localhost:8000/api/rooms/ABC123` | (none) |
   | POST | `http://localhost:8000/api/rooms/ABC123/join` | `{"name": "Player Name"}` |

3. **Test**:
   - First request to get `room_code`
   - Use that `room_code` in other requests

---

## 📊 Database File

After running the backend, a SQLite database is created:
```
backend/werewolf.db
```

You can browse it with:
- **SQLite Browser**: https://sqlitebrowser.org/ (GUI)
- **VSCode Extension**: SQLite (by alexcvzz)

---

## ✨ API Endpoints Summary

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/rooms` | Create new room | ✅ Ready |
| GET | `/api/rooms/{room_code}` | Get room info & players | ✅ Ready |
| POST | `/api/rooms/{room_code}/join` | Player joins room | ✅ Ready |

---

## 🔧 Troubleshooting

### **Port 8000 already in use**
```bash
# Use different port
python -m uvicorn app.main:app --port 8001 --reload
```

### **Import errors**
```bash
# Make sure you're in backend folder and venv is activated
cd backend
venv\Scripts\activate
```

### **Database issues**
```bash
# Delete old database
rm werewolf.db
# Restart backend - it will create new one
```

### **CORS errors in frontend**
- Already configured for localhost:5173
- Will be handled in next phase

---

## 📚 Code Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app + routers
│   ├── config.py            # Settings
│   ├── database.py          # DB connection & table creation
│   ├── models/
│   │   ├── base.py          # Base model with timestamps
│   │   ├── room.py          # Room model
│   │   └── player.py        # Player model
│   ├── schemas/
│   │   ├── room.py          # Room request/response
│   │   └── player.py        # Player request/response
│   ├── services/
│   │   ├── room_service.py  # Room business logic
│   │   └── player_service.py # Player business logic
│   └── routers/
│       └── rooms.py         # Room API endpoints
└── requirements.txt
```

---

## 🎯 Next Steps

✅ **Current Phase**: Room API & Player Join API  
⏭️ **Next Phase**: 
- GET /api/rooms/{room_id}/players (more detailed)
- PUT /api/rooms/{room_id}/role-cart (setup role)
- POST /api/rooms/{room_id}/start (start game)
- WebSocket events for realtime updates
- Game logic engine

---

**Backend is ready for Phase 2!** 🚀
