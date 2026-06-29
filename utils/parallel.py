from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Iterable, TypeVar, List

T = TypeVar("T")
R = TypeVar("R")


def run_parallel(
    items: Iterable[T],
    worker: Callable[[T], R | None],
    max_workers: int = 5,
) -> List[R]:
    """
    Execute a worker function on multiple items in parallel.

    Parameters
    ----------
    items : iterable
        Collection of items to process.

    worker : callable
        Function that processes one item.

    max_workers : int
        Maximum number of worker threads.

    Returns
    -------
    list
        Successful results only.
    """

    items = list(items)

    if not items:
        return []

    workers = min(max_workers, len(items))

    results: List[R] = []

    with ThreadPoolExecutor(max_workers=workers) as executor:

        futures = [
            executor.submit(worker, item)
            for item in items
        ]

        for future in as_completed(futures):

            try:

                result = future.result()

                if result is not None:
                    results.append(result)

            except Exception as e:

                print(f"\nParallel task failed:\n{e}\n")

    return results