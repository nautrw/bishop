import hashlib
import itertools


def encode_text(text: str) -> bytes:
    text_bytes = text.encode()
    md5_hash = hashlib.md5(text_bytes)
    return md5_hash.digest()

def bytes_to_pairs(bytes: bytes) -> list[str]:
    result = []

    for byte in bytes:
        binary_str = bin(byte)[2:]
        padding = '0' * (8 - len(binary_str))
        padded_binary = padding + binary_str

        binary_pairs = list(itertools.batched(padded_binary, 2))
        flattened_pairs = [pair[0] + pair[1] for pair in binary_pairs]

        for pair in flattened_pairs:
            result.append(pair) # noqa: PERF402

    return result
