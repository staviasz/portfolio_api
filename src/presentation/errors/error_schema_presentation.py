from typing_extensions import TypedDict, List


class ErrorSchema(TypedDict):
    field: str
    type: str
    message: str


def error_schema(errors: str) -> List[ErrorSchema]:
    formated_erros = []
    error_lines = errors.split("\n")
    ignore_list = ["validation error", "/"]
    field = ""
    for error in error_lines:

        if any(e in error for e in ignore_list):
            continue

        if not any(e in error for e in ignore_list) and "[" not in error:
            field = error
            continue

        if "[" in error:
            message, teste = error.split("[")
            error_dict: ErrorSchema = {
                "field": field,
                "type": teste.split(",")[0].split("=")[1],
                "message": message.strip(),
            }

            formated_erros.append(error_dict)

    return formated_erros
