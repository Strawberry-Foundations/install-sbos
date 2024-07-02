def parse_size(input_str):
    input_str = input_str.strip().lower()

    if input_str.endswith('g'):
        size_in_gb = float(input_str[:-1])
        size_in_mb = int(size_in_gb * 1024)
    elif input_str.endswith('m'):
        size_in_mb = int(float(input_str[:-1]))
    else:
        return None

    return size_in_mb
