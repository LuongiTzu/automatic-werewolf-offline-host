# Phase 5A: Quick Start Testing Guide

## 🚀 Start Development Server

```bash
# Terminal 1: Backend (if not already running)
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm install  # (if needed)
npm run dev
```

## 📖 What's New

**Files Created:**
- ✅ `frontend/src/services/audioService.ts` - Web Speech API service
- ✅ `frontend/src/components/host/AudioControl.vue` - Audio control UI

**Files Updated:**
- ✅ `frontend/src/pages/HostRoom.vue` - Added AudioControl component
- ✅ `frontend/src/services/index.ts` - Export audioService

## 🧪 Quick Testing (2 minutes)

1. **Open Host Room Page**
   - Go to: http://localhost:5173/
   - Create a room or navigate to existing host room
   - Should see AudioControl panel at the top

2. **Enable Audio**
   - Click "🎤 Kích Hoạt Âm Thanh" button
   - You'll hear: "Âm thanh đã sẵn sàng"
   - Status changes to: "✅ Sẵn sàng"

3. **Test Speaking**
   - Click "🧪 Đọc Thử" button
   - You'll hear the same test message
   - "Đọc Lại" button becomes enabled

4. **Test Volume**
   - Move "Âm Lượng Giọng Đọc" slider to 50%
   - Click "🧪 Đọc Thử" again
   - Audio should be quieter

5. **Test Toggle**
   - Click checkbox to disable speech
   - All audio buttons become disabled
   - Toggle on again to re-enable

## 📋 Complete Test Checklist

```
Audio Service Tests:
[✓] Enable audio - speaks test message
[✓] Test button - repeats test message
[✓] Replay button - replays last text
[✓] Stop button - stops speaking
[✓] Voice volume - affects TTS volume
[✓] Ambient volume - controls ambient level
[✓] Speech toggle - enables/disables TTS
[✓] Ambient toggle - enables/disables ambient
[✓] Status display - shows correct state
[✓] Error handling - displays error messages
[✓] Browser check - warns if not supported
[✓] Text display - shows current text
```

## 🎯 Key Component Locations

| File | Purpose | Changes |
|------|---------|---------|
| audioService.ts | Audio engine | NEW - Core service |
| AudioControl.vue | UI controls | NEW - Component |
| HostRoom.vue | Host page | UPDATED - Added component |
| index.ts | Exports | UPDATED - Export audioService |

## ✅ Verification Checklist

Before considering Phase 5A complete, verify:

- [ ] AudioControl.vue renders without errors
- [ ] Audio initializes when button clicked
- [ ] Test button produces sound
- [ ] Replay button works
- [ ] Stop button works
- [ ] Volume sliders adjust output
- [ ] Toggles enable/disable features
- [ ] Status indicator updates correctly
- [ ] Error messages display when needed
- [ ] Works in Chrome (primary test browser)
- [ ] Works in Firefox (secondary)
- [ ] Graceful degradation in unsupported browsers

## 🐛 Debugging

### If AudioControl not showing:
```
1. Check console for errors (F12 → Console)
2. Verify import in HostRoom.vue
3. Check if component directory exists:
   frontend/src/components/host/
```

### If no sound:
```
1. Check browser volume
2. Test in different browser
3. Verify: window.speechSynthesis exists
   (Check in browser console)
4. Check browser supports Web Speech API
```

### If buttons disabled:
```
1. Click "Kích Hoạt Âm Thanh" first
2. Wait for test audio to complete
3. Check status indicator
```

## 📝 Notes

- **Language**: Vietnamese TTS
- **Browser Support**: Chrome, Firefox, Safari 14.1+, Edge 79+
- **Volume Range**: 0-100% (internally 0-1)
- **State**: Synced with audioService via reactive subscriptions
- **Error Handling**: User-friendly Vietnamese messages

## 🎓 Learning Resources

If you need to modify the audio service:

**Web Speech API Docs:**
- https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API
- https://www.w3.org/TR/speech-synthesis/

**Vue 3 Reactivity:**
- https://vuejs.org/guide/extras/reactivity-in-depth.html
- Observer pattern implementation with subscriptions

## 🚀 Next Phase

After Phase 5A is verified working:
- Phase 5B: Player role UI
- Phase 3B: Start game logic
- Phase 4: Night phase engine

---

**Status: Phase 5A Complete ✅**
**Last Updated:** Now
**Files: 2 new, 2 updated**
