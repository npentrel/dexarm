import asyncio
from viam.module.module import Module
try:
    from models.dexarm import Dexarm
except ModuleNotFoundError:
    # when running as local module with run.sh
    from .models.dexarm import Dexarm


if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
