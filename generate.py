import warnings

from RestrictedPython import compile_restricted, diagram_builtins

from utils import find_png


def generate_diagram(source_code):
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            byte_code = compile_restricted(
                source_code,
                filename='<inline code>',
                mode='exec'
            )
            exec(byte_code, {"__builtins__": diagram_builtins}, None)
            res = find_png()
        except (SyntaxError, SyntaxWarning, NameError, TypeError, ImportError) as e:
            return e

    return res

