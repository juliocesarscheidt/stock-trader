from datetime import datetime

from tenacity import Retrying, RetryError, stop_after_attempt, wait_exponential
from typing import Callable

from stock.common.logger import log


def get_datetime_now_iso() -> str:
    return datetime.utcnow().isoformat()


def convert_value_to_float(value: str) -> float:
    return float(value.replace(",", "."))


def retry(fn: Callable):
    try:
        for attempt in Retrying(
            stop=stop_after_attempt(3), wait=wait_exponential(), reraise=True
        ):
            with attempt:
                fn()

    except RetryError as e:
        log(e.last_attempt.attempt_number)
        return None
