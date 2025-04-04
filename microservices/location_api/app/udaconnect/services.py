import logging
from typing import Dict
import json
from flask import g

from app import db
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_Point
from kafka import KafkaProducer


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        KAFKA_SERVER = 'kafka-service:9092'
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
        kafka_data = json.dumps(location).encode()
        #producer = g.kafka_producer
        producer.send("location", kafka_data)
        producer.flush()