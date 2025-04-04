
import logging
import time

from app import create_app
from app.udaconnect.consumer import KafkaConsumer


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)




