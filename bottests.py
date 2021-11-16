'''                           '''
from init import *


if __name__ == "__main__":
    #UpdateManager.clearHash()
    loop = asyncio.get_event_loop() # Make an event loop
    loop.create_task(UpdateManager.checkUpdate()) # Start up the auto-updater
    loop.run_forever() # Run forever