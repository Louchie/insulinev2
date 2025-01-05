import asyncio
from src.event_bus import publish_event, consume_event

async def callback(message):
    assert message.decode() == "Test Event"

async def test_publish_and_consume_event():
    await asyncio.to_thread(publish_event, "test_queue", "Test Event")
    await asyncio.to_thread(consume_event, "test_queue", callback)
