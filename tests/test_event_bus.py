from src.event_bus import publish_event, consume_event

def test_publish_and_consume_event():
    def callback(message):
        assert message.decode() == "Test Event"

    publish_event("test_queue", "Test Event")
    consume_event("test_queue", callback)
