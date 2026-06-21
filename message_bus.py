import redis
import json
import logging

logger = logging.getLogger("FSE.MessageBus")

class MessageBus:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )

    def publish_signal(self, channel, signal: dict):
        try:
            message = json.dumps(signal)
            self.client.publish(channel, message)
            logger.info(f"📡 Signal published to {channel}")
        except Exception as e:
            logger.error(f"❌ Redis Publish Failed: {e}")

    def subscribe(self, channel):
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel)
        logger.info(f"👂 Subscribed to {channel}")
        return pubsub

    def listen(self, pubsub):
        """Blocking listener for execution layer"""
        for message in pubsub.listen():
            if message['type'] == 'message':
                yield json.loads(message['data'])
