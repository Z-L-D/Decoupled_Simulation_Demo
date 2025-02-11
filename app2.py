import json
import random
import asyncio
import websockets
import time

class Building:
    def __init__(self):
        self.type = random.choice(["Residential", "Commercial", "Industrial", "Civic"])
        self.density = random.choice(["Low", "Medium", "High"])
        self.wealth = random.choice(["Low", "Medium", "High"])
        self.pollution = random.randint(0, 100)
    
    def to_dict(self):
        return {
            "type": self.type,
            "density": self.density,
            "wealth": self.wealth,
            "pollution": self.pollution
        }

class Citizen:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.suggestion = random.choice([
            "Build a statue",
            "Rezone to commercial",
            "Add a park",
            "Upgrade roads"
        ])
    
    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "suggestion": self.suggestion
        }

async def simulation_loop(websocket, path):  # Now includes 'path' parameter
    # Initialize a 10x10 grid
    grid = [[Building() for _ in range(10)] for _ in range(10)]
    
    # Initialize some citizens
    citizens = []
    for _ in range(10):
        citizens.append(Citizen(random.randint(0, 9), random.randint(0, 9)))
    
    while True:
        # Collect grid and citizen data
        grid_data = [[building.to_dict() for building in row] for row in grid]
        citizens_data = [citizen.to_dict() for citizen in citizens]
        
        # Create the data package
        data = {
            "grid": grid_data,
            "citizens": citizens_data,
            "timestamp": time.time()
        }
        
        # Send updates to the client
        await websocket.send(json.dumps(data))
        
        # Simulate a suggestion being generated
        if random.random() < 0.1:
            citizens.append(Citizen(random.randint(0, 9), random.randint(0, 9)))
        
        # Sleep for a second before next update
        await asyncio.sleep(1)

async def main():
    # Create the WebSocket server
    start_server = websockets.serve(simulation_loop, 'localhost', 8765)  # No longer using
    
    # Start the server and run indefinitely
    async with start_server:
        await asyncio.sleep(10**9)  # Keep the server running

# Start the async main function
asyncio.run(main())