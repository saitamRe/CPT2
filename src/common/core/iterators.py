from typing import Iterator

def batch(it: Iterator, batch_size: int) -> Iterator[Iterator]:
    single_butch = []

    for row in it:
        single_butch.append(row)

        if len(single_butch) >= batch_size:
            yield single_butch
            single_butch.clear()
    
    if single_butch:
        yield single_butch