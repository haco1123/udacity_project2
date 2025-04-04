import logging
from concurrent import futures
from typing import Dict, List
from datetime import timedelta

from app import db
from app.udaconnect.models import Location, Person
from app.udaconnect.schemas import LocationSchema

import grpc
import location_pb2
import location_pb2_grpc

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def __init__(self, app):
        self.app = app

    def Get(self, request, context):
        with self.app.app_context():
            result = location_pb2.LocationMessageList()

            logger.info(f"Received request: {request}")

            locations: List = db.session.query(Location).filter(
                Location.person_id == request.person_id
            ).filter(Location.creation_time < request.end_date).filter(
                Location.creation_time >= request.start_date
            ).all()

            logger.info(f"Locations found: {locations}")

            for location in locations:
                location_message = location_pb2.LocationResMessage(
                    person_id=location.person_id,
                    longitude=str(location.longitude),
                    latitude=str(location.latitude),
                    start_date=location.creation_time.strftime("%Y-%m-%d"),
                    end_date=(location.creation_time + timedelta(days=1)).strftime("%Y-%m-%d"),
                )
                result.locations.append(location_message)
    
            logger.info(f"Returning MessageList: {result}")
            return result
    

def init_grpc_server(app):
    # Initialize gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(app), server)

    server.add_insecure_port("[::]:5005")

    return server