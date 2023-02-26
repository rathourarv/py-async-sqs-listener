"""
a sample daemonization script for the sqs listener
"""

import asyncio
import sys
from sqs_listener.daemon import Daemon
from sqs_listener import SqsListener


class MyListener(SqsListener):
    async def handle_message(self, body, attributes, messages_attributes):
        # run your code here
        print(f"message received {body}")


class MyDaemon(Daemon):
    def run(self):
        print("Initializing listener")
        listener = MyListener("test-queue", interval=5, max_number_of_messages=5)
        asyncio.run(listener.listen())


if __name__ == "__main__":
    daemon = MyDaemon("/tmp/sqs_daemon.pid")
    if len(sys.argv) == 2:
        if "start" == sys.argv[1]:
            print("Starting listener daemon")
            daemon.start()
        elif "stop" == sys.argv[1]:
            print("Attempting to stop the daemon")
            daemon.stop()
        elif "restart" == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
