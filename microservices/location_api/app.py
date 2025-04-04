import logging
from multiprocessing import Process

from app import create_app
from app.udaconnect.grpc.server import init_grpc_server


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def start_grpc_server(app):
    # Initialize gRPC server
    server = init_grpc_server(app)
    server.start()
    logger.info("gRPC server started on port 5005")
    server.wait_for_termination()

def start_flask_server(app):
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    from app import create_app
    app = create_app()

    # Starte Flask und gRPC in separaten Prozessen
    flask_process = Process(target=start_flask_server, args=(app,))
    grpc_process = Process(target=start_grpc_server, args=(app,))

    flask_process.start()
    grpc_process.start()

    flask_process.join()
    grpc_process.join()
