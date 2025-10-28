import asyncio
from summarizerbot.ambient_agent import start_ambient_loop

if __name__ == "__main__":
    print("🚀 Starting Ambient Summarizer on Render...")
    loop = asyncio.get_event_loop()
    start_ambient_loop()
    loop.run_forever()
