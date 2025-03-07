#!/usr/bin/env python3
# Morrowind AI Framework - Server Runner

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import server components
from server import AIServer
from config import load_config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join("logs", "server.log"))
    ]
)

logger = logging.getLogger("run_server")

async def main():
    """Main function to run the server."""
    try:
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Load configuration
        logger.info("Loading configuration...")
        config = load_config()
        
        # Create and start server
        logger.info("Starting server...")
        server = AIServer(config)
        await server.start()
        
        # Keep the server running
        logger.info(f"Server running at ws://{config['server']['host']}:{server.port}")
        logger.info("Press Ctrl+C to stop the server")
        
        # Wait forever (or until interrupted)
        while True:
            await asyncio.sleep(3600)  # Sleep for an hour
    
    except KeyboardInterrupt:
        logger.info("Server stopping due to keyboard interrupt...")
    except Exception as e:
        logger.error(f"Error running server: {e}", exc_info=True)
    finally:
        # Stop the server if it was started
        if 'server' in locals():
            logger.info("Stopping server...")
            await server.stop()
        
        logger.info("Server stopped")

if __name__ == "__main__":
    asyncio.run(main())
