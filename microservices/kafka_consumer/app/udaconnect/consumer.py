import logging
from datetime import datetime
import json
from kafka import KafkaConsumer

from app import create_app
from app.udaconnect.services import LocationService


TOPIC_NAME = 'location'
BOOTSTRAP_SERVER = 'kafka-service:9092'

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class KafkaConsumerWrapper:
    def  __init__(self):
        self.app = create_app()
        # Create a Kafka consumer
        self.consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=BOOTSTRAP_SERVER)
        logger.info("Kafka consumer initialized.")

    
    def consume_messages(self):
        try:
            with self.app.app_context():
                logger.info("Kafka consumer started. Listening for messages...")

                # Consume messages in an infinite loop
                for message in self.consumer:
                    location_data = message.value.decode('utf-8')
                    logger.info(f"Raw message: {location_data}")

                    # Parse the message as JSON
                    location_dict = json.loads(location_data)

                    # Format the location data to match LocationSchema
                    formatted_location = {
                        "person_id": int(location_dict["person_id"]),  # Convert to int
                        "creation_time": datetime.strptime(location_dict["creation_time"], "%Y-%m-%dT%H:%M:%S"),  # Convert to datetime
                        "creation_time": location_dict["creation_time"],  # Convert to datetime
                        "latitude": location_dict["latitude"], 
                        "longitude": location_dict["longitude"]
                    }
                    logger.info(f"formated: {formatted_location}")
                    LocationService.save_location(formatted_location)
        
        except Exception as e:
            logger.error(f"An error occurred: {e}")