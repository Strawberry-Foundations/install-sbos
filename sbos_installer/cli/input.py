def parse_size(input_str):
    input_str = input_str.strip().lower()

    if input_str.endswith('g'):
        size_in_gb = float(input_str[:-2])
        size_in_mb = int(size_in_gb * 1024)
    elif input_str.endswith('m'):
        size_in_mb = int(float(input_str[:-2]))
    else:
        raise ValueError("Invalid format")

    return size_in_mb
