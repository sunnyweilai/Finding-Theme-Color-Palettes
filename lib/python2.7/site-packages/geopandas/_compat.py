""""""

# Pytho 2 / 3 compat

PY3 = sys.version_info[0] == 3


# Pandas compat

try:
    from pandas.util import cache_readonly
except ImportError:
    from pandas.util.decorators import cache_readonly