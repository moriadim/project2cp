import asyncio
import sys
import websockets
import traceback
import logging

# Setup more detailed logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more verbose output
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
WS_URL = "ws://localhost:8000/ws/assistant/notifications/"
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MjkxMTAxLCJpYXQiOjE3NDU2ODYzMDEsImp0aSI6IjRmM2U0YjEzOTRjNDQ3MmFhODQ4ODBmZTdkNGU3MjUyIiwidXNlcl9pZCI6MTd9.vUINAeoFTlw7OSluueNXOIE3rLBFYHaYz5KZSSsTkPo"  # Replace with your actual token


async def test_connection():
    """Simple test to connect to WebSocket server"""
    try:
        logger.debug(f"Attempting to connect to {WS_URL}")
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else None

        # Log connection attempt details
        logger.debug(f"Using headers: {headers}")
        logger.debug(f"Using websockets version: {websockets.__version__}")

        # Connect with headers
        async with websockets.connect(
            WS_URL,
            extra_headers=headers,
            ping_interval=30,
            ping_timeout=10
        ) as ws:
            logger.info("Connected successfully!")

            # Send a simple test message
            test_message = '{"type": "ping", "message": "Hello server"}'
            logger.debug(f"Sending test message: {test_message}")
            await ws.send(test_message)

            # Wait for a response with timeout
            logger.debug("Waiting for response...")
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=5.0)
                logger.info(f"Received response: {response}")
            except asyncio.TimeoutError:
                logger.warning("No response received within timeout period")

            logger.info("Test completed successfully")

    except Exception as e:
        logger.error(f"Connection test failed with error: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

    return True


async def main():
    try:
        logger.info("Starting WebSocket connection test")

        # Check Python and OS details
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Platform: {sys.platform}")

        # Test connection
        result = await test_connection()
        if result:
            logger.info("Connection test passed")
        else:
            logger.error("Connection test failed")

    except Exception as e:
        logger.error(f"Main error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
    finally:
        logger.info("Exiting...")

if __name__ == "__main__":
    # Set up proper event loop policy for Windows
    if sys.platform == 'win32':
        logger.info("Setting Windows-specific event loop policy")
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        logger.critical(f"Traceback: {traceback.format_exc()}")
