from network import NetworkManager
import asyncio
from time import sleep

class Server:
    def __init__(self) -> None:
        self.network = NetworkManager()

    async def update(self):
        messages = self.network.read_queue()
        if messages:
            print(messages)

    async def run(self):
        while True:
            await self.update()


async def main():
    server = Server()
    await asyncio.gather(
        server.network.start('localhost', 8765),
        server.run()
    )

if __name__ == "__main__":
    asyncio.run(main())
