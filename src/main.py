import asyncio
from viam.module.module import Module
try:
    from models.dexarm import Dexarm
except ModuleNotFoundError:
    # when running as local module with run.sh
    from .models.dexarm import Dexarm
try:
    from models.rotary_gripper import RotaryGripper
except ModuleNotFoundError:
    # when running as local module with run.sh
    from .models.rotary_gripper import RotaryGripper


if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
