import os
import warnings

from RestrictedPython import compile_restricted, diagram_builtins

from utility import find_png


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
        except SyntaxError as e:
            res = e
        except SyntaxWarning as e:
            res = e
        except NameError as e:
            res = e
        except TypeError as e:
            res = e
        except ImportError as e:
            res = e

    return res

