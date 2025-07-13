# Start Script Documentation

## Enhanced Start Scripts with Port Management

The start scripts now include automatic port checking and process management to prevent conflicts.

## Available Commands

### 🚀 Main Start Command (Recommended)
```bash
npm run start
```
- **What it does**: Checks ports 8000 and 5173, kills existing processes if needed, then starts both backend and frontend
- **Features**: Colored output, detailed feedback, automatic port cleanup
- **Best for**: Normal development workflow

### ⚡ Direct Start (No Port Checking)
```bash
npm run start:direct
```
- **What it does**: Starts both services directly without port checking
- **Best for**: When you're sure no conflicting processes are running

### 🎯 Individual Service Commands
```bash
npm run start:backend    # Start only backend (checks port 8000)
npm run start:frontend   # Start only frontend (checks port 5173)
```

## Port Management Features

### Automatic Port Checking
- **Backend Port**: 8000 (FastAPI server)
- **Frontend Port**: 5173 (Vite dev server)

### Process Cleanup Strategy
1. **Detection**: Checks if ports are in use using `lsof`
2. **Graceful Shutdown**: Sends SIGTERM to existing processes
3. **Force Kill**: If graceful shutdown fails, uses SIGKILL
4. **Verification**: Confirms ports are free before proceeding

### Example Output
```
🚀 Starting AgentSwarm Application...

📋 Checking required ports...
Checking if port 8000 is already in use...
⚠️  Port 8000 is already in use by process 12345 (FastAPI Backend)
🔄 Attempting to shut down existing process...
✅ Port 8000 is now free

Checking if port 5173 is already in use...
✅ Port 5173 is available

🎯 All ports are ready!
Starting services...
```

## Manual Port Management

If you need to manually check or kill processes on specific ports:

```bash
# Check and kill process on port 8000
./scripts/check-port.sh 8000 "Backend"

# Check and kill process on port 5173  
./scripts/check-port.sh 5173 "Frontend"
```

## Troubleshooting

### If Port Cleanup Fails
```bash
# Manual process identification
lsof -i :8000
lsof -i :5173

# Manual process termination
kill -9 <process_id>
```

### If Scripts Don't Execute
```bash
# Make scripts executable
chmod +x scripts/check-port.sh
chmod +x scripts/start-app.sh
```

## Files Added
- `scripts/check-port.sh` - Port checking and cleanup utility
- `scripts/start-app.sh` - Enhanced start script with port management
- Updated `package.json` with new start commands
