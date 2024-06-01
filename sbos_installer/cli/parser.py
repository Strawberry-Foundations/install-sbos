def parse_bool(user_input: str) -> bool:
    match user_input.lower():
        case "yes":
            return True
        case "no":
            return False
        case _:
            return False
