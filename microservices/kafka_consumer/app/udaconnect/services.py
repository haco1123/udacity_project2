import logging
from typing import Dict
import json
from flask import g

from app import db
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_Point


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class LocationService:
    @staticmethod
    def save_location(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        logger.info(f"Saving location: {location}")
        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        db.session.add(new_location)
        db.session.commit()

        logger.info(f"Location saved successfully.")
        return new_location