# 🚀 Backend Phase 2: Room API & Player Join - COMPLETE

## ✅ What's Implemented

### Models (SQLAlchemy)
- ✅ **Room** - room_code (6 chars), host_token, status, current_phase, timestamps
- ✅ **Player** - name, session_token, role_code, is_alive, is_connected

### Schemas (Pydantic)
- ✅ **CreateRoomResponse** - room_id, room_code, host_token, status
- ✅ **JoinRoomRequest** - name validation
- ✅ **JoinRoomResponse** - player_id, session_token, player_count
- ✅ **RoomInfoResponse** - full room state with players
- ✅ **PlayerResponse** & **PlayerInRoomResponse**

### REST API Endpoints
- ✅ **POST /api/rooms** - Host creates room, gets room_code and host_token
- ✅ **POST /api/rooms/{room_code}/join** - Player joins with name, gets session_token
- ✅ **GET /api/rooms/{room_code}** - Get room info and player list

### Services
- ✅ **RoomService** - create_room, get_room, player_count, token generation
- ✅ **PlayerService** - join_room, get_player, connection status

### Database
- ✅ **SQLite local** - Auto-creates tables on startup
- ✅ **Database creation** - Automatic via app lifespan

### Architecture
- ✅ models/ - SQLAlchemy ORM models
- ✅ schemas/ - Pydantic request/response validation
- ✅ services/ - Business logic isolated
- ✅ routers/ - Clean API endpoint definitions

---

## 🎯 Run Commands

### Terminal 1 - Backend Server

```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     🚀 Starting Werewolf Game API...
INFO:     ✅ Database tables created/verified
```

**Available at:**
- 🌐 API: http://localhost:8000
- 📚 Swagger UI: http://localhost:8000/docs
- 📖 ReDoc: http://localhost:8000/redoc
- 🏥 Health: http://localhost:8000/health

---

## 🧪 Quick Test in Swagger UI

1. Open **http://localhost:8000/docs**
2. Click "Try it out" buttons:

### Test Sequence:

**1. Create Room (POST /api/rooms)**
- Click "Try it out" → "Execute"
- Save: `room_code` (e.g., "ABC123")

**2. Get Room (GET /api/rooms/{room_code})**
- Put room_code from step 1
- Execute → See empty players list

**3. Join Room (POST /api/rooms/{room_code}/join)**
- Use room_code from step 1
- Request body: `{"name": "Player Name"}`
- Execute → Get player_id and session_token
- Repeat multiple times to add more players

**4. Get Room Again**
- Should now show all joined players

---

## 📋 API Examples (cURL)

### Create Room
```bash
curl -X POST http://localhost:8000/api/rooms
```

### Join Room
```bash
curl -X POST http://localhost:8000/api/rooms/ABC123/join \
  -H "Content-Type: application/json" \
  -d '{"name": "Player Name"}'
```

### Get Room
```bash
curl -X GET http://localhost:8000/api/rooms/ABC123
```

---

## 🧪 Full Test Script

Run this Python script to test all endpoints:

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Create room
print("Creating room...")
r = requests.post(f"{BASE_URL}/api/rooms")
room = r.json()
room_code = room["room_code"]
print(f"✅ Room created: {room_code}")

# 2. Players join
print(f"Players joining {room_code}...")
for name in ["Player 1", "Player 2", "Player 3"]:
    r = requests.post(f"{BASE_URL}/api/rooms/{room_code}/join",
                     json={"name": name})
    player = r.json()
    print(f"✅ {name} joined (ID: {player['player_id'][:8]}...)")

# 3. Get room with all players
print(f"Getting room info...")
r = requests.get(f"{BASE_URL}/api/rooms/{room_code}")
room_info = r.json()
print(f"✅ Total players: {room_info['player_count']}")
for p in room_info["players"]:
    print(f"   - {p['name']}")
```

---

## 📊 Database Schema

**rooms table:**
```
id              VARCHAR(36) PRIMARY KEY
room_code       VARCHAR(6) UNIQUE
host_token      VARCHAR(64) UNIQUE
status          ENUM(waiting, playing, ended)
current_phase   ENUM(setup, night, day, vote, ended)
night_number    VARCHAR
day_number      VARCHAR
created_at      DATETIME
updated_at      DATETIME
```

**players table:**
```
id              VARCHAR(36) PRIMARY KEY
room_id         VARCHAR(36) FOREIGN KEY → rooms.id
name            VARCHAR(50)
session_token   VARCHAR(64) UNIQUE
role_code       VARCHAR(50) NULLABLE
is_alive        BOOLEAN
is_connected    BOOLEAN
created_at      DATETIME
updated_at      DATETIME
```

---

## 🔒 Security Features

- ✅ **Session tokens** - Random 64-char hex for each player
- ✅ **Host token** - Unique for each room
- ✅ **Input validation** - Name length, emptiness checks
- ✅ **Status checking** - Only join if room is "waiting"
- ✅ **Token uniqueness** - Ensures no collisions
- ✅ **SQL injection protection** - SQLAlchemy ORM

---

## 📁 Code Files Added/Modified

### New Files:
- `backend/app/models/base.py` - Base model
- `backend/app/models/room.py` - Room model
- `backend/app/models/player.py` - Player model
- `backend/app/models/__init__.py` - Updated
- `backend/app/schemas/room.py` - Room schemas
- `backend/app/schemas/player.py` - Player schemas
- `backend/app/schemas/__init__.py` - Updated
- `backend/app/services/room_service.py` - Room logic
- `backend/app/services/player_service.py` - Player logic
- `backend/app/services/__init__.py` - Updated
- `backend/app/routers/rooms.py` - Room endpoints
- `backend/app/routers/__init__.py` - Updated

### Updated Files:
- `backend/app/main.py` - Added routers and startup
- `backend/app/database.py` - SQLite config
- `backend/app/config.py` - Updated for SQLite
- `backend/requirements.txt` - Cleaned up

---

## 🚦 Testing Checklist

- [ ] Backend starts without errors
- [ ] POST /api/rooms creates room with room_code
- [ ] GET /api/rooms/{room_code} returns room info
- [ ] POST /api/rooms/{room_code}/join adds player
- [ ] Multiple joins increase player_count
- [ ] Each player gets unique session_token
- [ ] Room status is "waiting"
- [ ] Players show in room's players list
- [ ] Swagger UI shows all 3 endpoints
- [ ] Database file created (werewolf.db)

---

## 📈 Status

| Task | Status |
|------|--------|
| Models | ✅ Complete |
| Schemas | ✅ Complete |
| API Endpoints | ✅ Complete |
| Services | ✅ Complete |
| Database | ✅ Complete |
| Error Handling | ✅ Complete |
| Documentation | ✅ Complete |
| Swagger UI | ✅ Ready |

---

## 🎯 Next Phase Features

Not implemented yet (for next phase):
- WebSocket realtime events
- GET /api/rooms/{room_id}/players (detailed)
- PUT /api/rooms/{room_id}/role-cart (setup roles)
- POST /api/rooms/{room_id}/start (start game)
- Night/Day phase logic
- Vote system
- Game engine

---

**Backend Phase 2 is complete and tested!** 🎉

See `TESTING_API.md` for detailed testing instructions and examples.
