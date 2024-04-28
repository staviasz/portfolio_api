def clean_dict_return(data: dict):
    return {key: value for key, value in data.items() if value and value != "None"}
