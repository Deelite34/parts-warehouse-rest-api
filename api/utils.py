from flask import abort, make_response


def detailed_abort(code, details: str | Exception) -> None:
    """Abort response with additional 'details' key and value"""
    abort(
        make_response(
            {"code": code, "status": "Bad Request", "details": str(details)}, code
        )
    )
