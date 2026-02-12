"""
Modified version of server.py with mock mode support for testing without Isaac Sim
"""

# Check if we're in mock mode (for testing without Isaac Sim)
import os
_MOCK_MODE = os.environ.get("ISAAC_MCP_MOCK_MODE", "false").lower() == "true"

class MockIsaacConnection:
    """Mock Isaac connection for testing without Isaac Sim"""
    
    def __init__(self):
        self.connected = True
    
    def connect(self) -> bool:
        """Mock connect - always succeeds"""
        print("[MOCK] Mock Isaac connection established")
        return True
    
    def disconnect(self):
        """Mock disconnect"""
        print("[MOCK] Mock Isaac connection disconnected")
    
    def send_command(self, command_type: str, params=None) -> dict:
        """Mock send command - returns simulated responses"""
        print(f"[MOCK] Sending command: {command_type} with params: {params}")
        
        # Simulated responses for different commands
        mock_responses = {
            "get_scene_info": {
                "status": "success",
                "result": {
                    "assets_root_path": "/mock/Assets/Isaac/4.2",
                    "scene": "Mock Scene",
                    "objects": []
                }
            },
            "create_physics_scene": {
                "status": "success",
                "result": "Physics scene created (mock)",
                "message": "Mock physics scene created successfully"
            },
            "create_robot": {
                "status": "success",
                "result": "Robot created (mock)",
                "message": "Mock robot created successfully"
            },
            "execute_script": {
                "status": "success",
                "result": "Script executed (mock)",
                "output": "Mock script execution completed"
            },
            "generate_3d_from_text_or_image": {
                "status": "success",
                "task_id": "mock_task_123",
                "prim_path": "/World/mock_object"
            },
            "search_3d_usd_by_text": {
                "status": "success",
                "task_id": "mock_search_456",
                "prim_path": "/World/mock_search_result"
            },
            "transform": {
                "status": "success",
                "message": "Transform applied (mock)"
            }
        }
        
        return mock_responses.get(command_type, {
            "status": "success",
            "result": "Mock response"
        })

# Now import and patch the original server
import sys
sys.path.insert(0, '/app/auto-mcp-upload/data/8720/isaac_mcp')

# Import original module
import server

# Patch get_isaac_connection
original_get_isaac_connection = server.get_isaac_connection

def patched_get_isaac_connection():
    """Patched version that returns mock connection in mock mode"""
    if _MOCK_MODE:
        if server._isaac_connection is None:
            server._isaac_connection = MockIsaacConnection()
        return server._isaac_connection
    return original_get_isaac_connection()

# Apply patch
server.get_isaac_connection = patched_get_isaac_connection

# Export main function
main = server.main

if __name__ == "__main__":
    main()
