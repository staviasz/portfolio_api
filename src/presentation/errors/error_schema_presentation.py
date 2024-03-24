from typing_extensions import TypedDict, List

from src.presentation.errors.exception_custom_errors_presentation import (
    ExceptionCustomPresentation,
)


class ErrorSchema(TypedDict):
    field: str
    type: str
    message: str


def error_schema(errors: str) -> List[ErrorSchema]:
    try:
        formated_erros = []
        error_lines = errors.split("\n")
        ignore_list = ["validation error", "/"]
        field = ""
        for error in error_lines:
            if "[" in error:
                message, teste, *rest = error.split("[")
                error_dict: ErrorSchema = {
                    "field": field,
                    "type": teste.split(",")[0].split("=")[1],
                    "message": message.strip(),
                }
                formated_erros.append(error_dict)
                continue

            if any(e in error for e in ignore_list):
                continue

            if not any(e in error for e in ignore_list) and "[" not in error:
                field = error
                continue

        return formated_erros
    except Exception:
        raise ExceptionCustomPresentation(
            status_code=500, message="Error on error_schema", type="Server Error"
        )
