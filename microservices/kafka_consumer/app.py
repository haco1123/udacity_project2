from app.udaconnect.consumer import KafkaConsumerWrapper
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    consumer = KafkaConsumerWrapper()
    while True:
        try:
            consumer.consume_messages()
        except Exception as e:
            logger.info(f"Error in consumer loop: {e}")
            logger.info("Restarting consumer in 5 seconds...")
            time.sleep(5)