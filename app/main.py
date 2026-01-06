import json
import sys

BDECODING_VALUE_ERROR = "Invalid encoded value"

def _decode_bencode(bencoded_value: bytes, start: int = 0):
    if bencoded_value[start] == ord('i'):
        end_index = bencoded_value.find(b'e', start)
        if end_index == -1:
            raise ValueError(BDECODING_VALUE_ERROR)
        return int(bencoded_value[start+1: end_index].decode()), end_index+1

    if chr(bencoded_value[start]).isdigit():
        first_colon_index = bencoded_value.find(b":", start)
        if first_colon_index == -1:
            raise ValueError(BDECODING_VALUE_ERROR)
        lenos = int(bencoded_value[start:first_colon_index].decode())
        return bencoded_value[first_colon_index+1: first_colon_index+1+lenos].decode(), first_colon_index+1+lenos

    if bencoded_value[start] == ord('d'):
        start += 1
        result = {}
        while bencoded_value[start] != ord('e'):
            key, start = _decode_bencode(bencoded_value, start)
            value, start = _decode_bencode(bencoded_value, start)
            result[key] = value
        return result, start+1

    if bencoded_value[start] == ord('l'):
        start += 1
        result = []

        while bencoded_value[start] != ord('e'):
            element, start = _decode_bencode(bencoded_value, start)
            result.append(element)

        return result, start+1

    raise ValueError(BDECODING_VALUE_ERROR)

def decode_bencode(bencoded):
    return _decode_bencode(bencoded)[0]

def main():
    command = sys.argv[1]

    print("Logs from your program will appear here!", file=sys.stderr)

    if command == "decode":
        bencoded_value = sys.argv[2].encode()
        print(json.dumps(decode_bencode(bencoded_value)))
    else:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
