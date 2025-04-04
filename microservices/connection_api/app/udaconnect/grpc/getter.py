import grpc
import location_pb2
import location_pb2_grpc
import logging

from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

def get_locations(person_id: int, start_date: datetime, end_date: datetime, meters=5):
    logger.info("Sending sample payload...")

    channel = grpc.insecure_channel("microservice-location-api:5005")
    stub = location_pb2_grpc.LocationServiceStub(channel)

    response = stub.Get(location_pb2.LocationReqMessage(
        person_id = person_id,
        start_date = start_date.strftime("%Y-%m-%d"),
        end_date = end_date.strftime("%Y-%m-%d")
    ))
    
    logger.info(f"response : {response}")

    # Prepare arguments for queries
    locations_list = []
    for location in response.locations:
        locations_list.append(
            {
                "person_id": location.person_id,
                "meters": meters,
                "start_date": location.start_date,
                "end_date": location.end_date,
                "latitude": location.latitude,
                "longitude": location.longitude,
            }
        )
    
    logger.info(f"locations: {locations_list}")

    return locations_list