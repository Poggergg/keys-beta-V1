import io
import contextlib
# Third party libraries
import textwrap
from traceback import format_exception

class CEPLID:
  def _eval(code):
        local_variables = {
        "test" : "oog"
      }

        stdout = io.StringIO()

        try:
          with contextlib.redirect_stdout(stdout):
              exec(
                  f"def func():\n{textwrap.indent(code, '    ')}", local_variables,
              )

              obj = local_variables["func"]()
              result = f"{stdout.getvalue()}\n-- {obj}\n"
        except Exception as e:
          result = "".join(format_exception(e, e, e.__traceback__))
          return result