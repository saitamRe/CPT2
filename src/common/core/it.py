from typing import TypeVar, Iterator, Iterable

T = TypeVar('T')

def batch(rows: Iterator[T], batch_size: int) -> Iterator[list[T]]:
    single_batch = []

    for row in rows:
        single_batch.append(row)
        if len(single_batch) >= batch_size:
            yield single_batch
            single_batch = []
    if single_batch:
        yield single_batch