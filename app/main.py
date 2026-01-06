import json
import sys

def decode_bencoded(bencoded_value: bytes, start: int=0):
    if bencoded_value[start] == ord('i'):
        end_index = bencoded_value.find(b'e', start)
        if end_index == -1:
            raise ValueError("Invalid encoded value")
        return bencoded_value[start+1: end_index], end_index+1

    if chr(bencoded_value[start]).isdigit():
        first_colon_index = bencoded_value.find(b":", start)
        if first_colon_index == -1:
            raise ValueError("Invalid encoded value")
        lenos = int(bencoded_value[start:first_colon_index].decode())
        return bencoded_value[first_colon_index+1: first_colon_index+1+lenos], first_colon_index+1+lenos

    if bencoded_value[start] == ord('d'):
        start += 1
        result = {}
        while bencoded_value[start] != ord('e'):
            key, start = decode_bencoded(bencoded_value, start)
            value, start = decode_bencoded(bencoded_value, start)
            result[key] = value
        return result, start+1

    if bencoded_value[start] == ord('l'):
        start += 1
        result = []

        while bencoded_value[start] != ord('e'):
            element, start = decode_bencoded(bencoded_value, start)
            result.append(element)

        return result, start+1

    raise ValueError("Invalid encoded value")

def main():
    command = sys.argv[1]

    print("Logs from your program will appear here!", file=sys.stderr)

    if command == "decode":
        bencoded_value = sys.argv[2].encode()

        def bytes_to_str(data):
            if isinstance(data, bytes):
                return data.decode()

            raise TypeError(f"Type not serializable: {type(data)}")

        print(json.dumps(decode_bencoded(bencoded_value), default=bytes_to_str))
    else:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()
