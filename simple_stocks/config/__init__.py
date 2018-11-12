from munch import Munch

from simple_stocks.config import default


config = Munch()

default.configure(config)

try:
    from simple_stocks.config import local

    local.configure(config)
except ImportError:
    print("No local config found, skipping...")
