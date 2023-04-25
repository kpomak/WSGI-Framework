def parse_request_params(params):
    data = {}
    if params:
        for param in params.split("&"):
            key, value = param.split("=")
            data[key] = value
    return data


if __name__ == "__main__":
    print(parse_request_params("key=value&spam=eggs"))
    print(parse_request_params(""))
