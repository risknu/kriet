from __future__ import annotations

import sys
import logging

def configure_logs() -> None:
    logger = logging.getLogger('kriet')
    logger.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler('kriet_logs.log')
    file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
