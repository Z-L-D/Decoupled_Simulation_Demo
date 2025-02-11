import asyncio
import websockets
import json
import random

GRID_SIZE = 10
clients = set()

class Grid:
    def __init__(self):
        self.grid = [[{
            "x": x,
            "y": y,
            "zone": "empty",
            "pollution": 0,
            "demand": 0,
            "changed": True  # Force initial full update
        } for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]
        
    def get_delta_updates(self):
        updates = []
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if self.grid[x][y]["changed"]:
                    updates.append({
                        "x": x,
                        "y": y,
                        "zone": self.grid[x][y]["zone"],
                        "pollution": self.grid[x][y]["pollution"],
                        "demand": self.grid[x][y]["demand"]
                    })
                    self.grid[x][y]["changed"] = False
        return updates
    
    def random_update(self):
        # Simulate some changes
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        self.grid[x][y]["pollution"] = min(100, self.grid[x][y]["pollution"] + random.randint(0, 10))
        self.grid[x][y]["zone"] = random.choice(["empty", "residential", "commercial", "industrial"])
        self.grid[x][y]["changed"] = True

grid = Grid()

async def update_clients():
    while True:
        grid.random_update()  # Simulate game state changes
        delta = grid.get_delta_updates()
        if delta:
            message = json.dumps({"type": "delta", "data": delta})
            await asyncio.gather(*[client.send(message) for client in clients])
        await asyncio.sleep(1)  # Update every 1 second

async def handler(websocket):
    clients.add(websocket)
    try:
        # Send full initial state
        initial_state = []
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                initial_state.append(grid.grid[x][y])
        await websocket.send(json.dumps({"type": "full", "data": initial_state}))
        
        async for message in websocket:
            pass  # We're not handling client input in this example
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        asyncio.create_task(update_clients())
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
    