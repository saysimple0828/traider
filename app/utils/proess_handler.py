from collections.abc import Callable
from multiprocessing import Process
from typing import Any

from app.api.error import Exception500
from app.utils.logger import make_logger

pool: dict[str, Process] = {}
max_count = 4

logger = make_logger(__name__)


def set_process(func: Callable, args: tuple[Any], kwargs: dict[Any, Any]):
    try:
        if len(pool.keys()) > max_count:
            logger.error(
                f"Process already allocated over max count. count: {max_count}"
            )
            return True
        process = Process(target=func, args=args, kwargs=kwargs)
        pool[process.name] = process
        process.start()
        return True
    except Exception as e:
        raise Exception500(f"Failed to allocate the process: {e} ")


def get_process(process_name: str):
    return pool[process_name]


def close_process(process_name: str):
    try:
        pool[process_name].close()
        del pool[process_name]
        return True
    except Exception as e:
        Exception500(f"Failed to delete the process {process_name}: {e} ")
