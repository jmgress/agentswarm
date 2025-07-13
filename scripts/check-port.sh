#!/bin/bash

#!/bin/bash

# Function to check if a port is in use and kill the process
check_and_kill_port() {
    local port=$1
    local service_name=$2
    local max_attempts=3
    local attempt=1
    
    echo "Checking if port $port is already in use..."
    
    while [ $attempt -le $max_attempts ]; do
        # Find ALL processes using the port
        local pids=$(lsof -t -i:$port 2>/dev/null)
        
        if [ -z "$pids" ]; then
            echo "✅ Port $port is available"
            return 0
        fi
        
        echo "⚠️  Port $port is in use by process(es): $pids ($service_name)"
        echo "🔄 Attempt $attempt/$max_attempts - Shutting down processes..."
        
        # Kill each process
        for pid in $pids; do
            if kill -0 $pid 2>/dev/null; then
                echo "  Terminating process $pid..."
                
                # Get process info for debugging
                local process_info=$(ps -p $pid -o comm= 2>/dev/null || echo "unknown")
                echo "    Process: $process_info (PID: $pid)"
                
                # Try graceful shutdown first
                if kill -TERM $pid 2>/dev/null; then
                    echo "    Sent SIGTERM to $pid"
                else
                    echo "    Failed to send SIGTERM to $pid, trying SIGKILL..."
                    kill -KILL $pid 2>/dev/null
                fi
            fi
        done
        
        # Wait for processes to die
        echo "  Waiting for processes to terminate..."
        sleep 3
        
        # Check if any processes are still running
        local remaining_pids=$(lsof -t -i:$port 2>/dev/null)
        if [ -n "$remaining_pids" ]; then
            echo "  Some processes still running: $remaining_pids"
            
            # Force kill remaining processes
            for pid in $remaining_pids; do
                echo "  Force killing process $pid..."
                kill -KILL $pid 2>/dev/null
                sleep 1
            done
        fi
        
        attempt=$((attempt + 1))
    done
    
    # Final check
    local final_check=$(lsof -t -i:$port 2>/dev/null)
    if [ -n "$final_check" ]; then
        echo "❌ Failed to free port $port after $max_attempts attempts."
        echo "   Remaining processes: $final_check"
        echo "   Manual intervention required:"
        echo "   lsof -i :$port"
        echo "   kill -9 $final_check"
        exit 1
    else
        echo "✅ Port $port is now free"
    fi
}

# Check the port passed as argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <port> [service_name]"
    exit 1
fi

PORT=$1
SERVICE_NAME=${2:-"service"}

check_and_kill_port $PORT "$SERVICE_NAME"
