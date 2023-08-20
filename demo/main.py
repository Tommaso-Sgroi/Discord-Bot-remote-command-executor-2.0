import logging
import threading

import discord

from demo.bot import new_client
from drce.distroy import DiscordRemoteCommandExecutor
from drce.distroy_loop import execute_drce
from drce.options import fetch_options

LOGGER_NAME = "drce_logger"


# def signal_handler(sig, _):
#     # Raise the custom exception to interrupt the threads
#     logging.info(f"received sig {sig}, all threads will be interrupted")
#     raise ThreadInterrupt


def new_drce(client: discord.Client, options):
    import demo.utils
    return DiscordRemoteCommandExecutor(
        # drce_executor=drce.utils.new_command_executor(),
        # drce_interpreter=drce.utils.new_command_interpreter(),
        options=options,
        client=client,
        logger=demo.utils.create_custom_logger(LOGGER_NAME, options.log_file),
    )


def start(client, options):
    drce = new_drce(client, options)

    drce_thread = threading.Thread(target=execute_drce, args=(drce,))

    # Start the threads
    drce.logger.info("DRCE starting...")
    drce_thread.start()

    drce.logger.info("your bot is starting...")

    drce.run_client()

    # try:
    #     # Wait for both threads to finish
    #     drce_thread.join()
    # except ThreadInterrupt:
    #     # If a signal is received, interrupt the threads and wait for them to finish
    #     drce_thread.join()

    logging.info("exiting")


if __name__ == "__main__":
    start(new_client(), fetch_options())
