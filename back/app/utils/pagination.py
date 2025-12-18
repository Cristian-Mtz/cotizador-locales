from __future__ import annotations

from math import ceil


def total_pages(total: int, page_size: int) -> int:
    if total <= 0:
        return 0
    return int(ceil(total / page_size))
