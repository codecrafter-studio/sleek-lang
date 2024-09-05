import sleek

while True:
    result = input(">>> ")
    parse_result = sleek.parser(result)
    if parse_result is not None:
        print(parse_result)
