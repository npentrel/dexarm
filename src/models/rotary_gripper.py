from dataclasses import dataclass
from typing import (Any, ClassVar, Dict, Final, List, Mapping, Optional,
                    Sequence, Tuple, cast)

from typing_extensions import Self
from viam.components.component_base import ComponentBase
from viam.components.gripper import *
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes
from viam.components.arm import *



class RotaryGripper(Gripper, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(ModelFamily("naomi", "dexarm"), "rotary-gripper")
    arm_name: str = ""
    arm: Arm = None
    is_holding: bool = False

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Gripper component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both required and optional)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any required dependencies or optional dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Tuple[Sequence[str], Sequence[str]]: A tuple where the
                first element is a list of required dependencies and the
                second element is a list of optional dependencies
        """
        req_deps = []
        fields = config.attributes.fields
        if "arm_name" not in fields:
            raise Exception("missing required arm_name attribute")
        elif not fields["arm_name"].HasField("string_value"):
            raise Exception("arm_name must be a string")
        arm_name = fields["arm_name"].string_value
        req_deps.append(arm_name)
        return req_deps, []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both required and optional)
        """
        if self.arm_name != config.attributes.fields["arm_name"].string_value:
            self.arm_name = config.attributes.fields["arm_name"].string_value
            dexarm_resource = dependencies[Arm.get_resource_name(self.arm_name)]
            self.arm = cast(Arm, dexarm_resource)

        else:
            self.logger.error("arm_name has not changed, skipping reconfiguration")

        return super().reconfigure(config, dependencies)

    @dataclass
    class HoldingStatus(Gripper.HoldingStatus):
        pass

    async def open(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ):
        self.logger.info("opening rotary gripper")
        self.is_holding = False

        await self.arm.do_command({"command": "M1000\r"})

    async def grab(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> bool:
        self.logger.info("picking up object with rotary gripper")
        self.is_holding = True
        await self.arm.do_command({"command": "M1001\r"})

    async def is_holding_something(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> HoldingStatus:
        if self.is_holding:
            return self.HoldingStatus.HOLDING
        else:
            return self.HoldingStatus.OPEN

    async def stop(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ):
        self.logger.info("picking up object with rotary gripper")
        self.is_holding = False
        await self.arm.do_command({"command": "M2101 STOP\r"})
        await self.arm.do_command({"command": "M1003\r"})

    async def is_moving(self) -> bool:
        self.logger.error("`is_moving` is not implemented")
        raise NotImplementedError()

    async def get_kinematics(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Tuple[KinematicsFileFormat.ValueType, bytes]:
        self.logger.error("`get_kinematics` is not implemented")
        raise NotImplementedError()

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        if "rotate_wrist" in command:
            speed = 1000
            direction = "clockwise"
            keep_rotating = False
            if "speed" in command["rotate_wrist"]:
                speed = command["rotate_wrist"]["speed"]
            else:
                self.logger.info("speed not set, using default speed of 1000")

            if "direction" in command["rotate_wrist"]:
                direction = command["rotate_wrist"]["direction"]
            else:
                self.logger.info("direction not set, using default direction of clockwise")

            if "keep_rotating" in command["rotate_wrist"]:
                keep_rotating = command["rotate_wrist"]["keep_rotating"]
            else:
                self.logger.info("direction not set, using default direction of clockwise")


            self.logger.info(f"Rotating wrist {direction} at {speed} speed")

            if "to_degrees" in command["rotate_wrist"]:
                to_degrees = command["rotate_wrist"]["to_degrees"]
                await self.arm.do_command({"command": "M2101 P" + str(to_degrees) + "\r"})

            if keep_rotating:
                if direction == "clockwise":
                    await self.arm.do_command({"command": "M2101 S" + str(speed) + "\r"})
                else:
                    await self.arm.do_command({"command": "M2101 S-" + str(speed) + "\r"})
            else:
                if direction == "clockwise":
                    await self.arm.do_command({"command": "M2101 R" + str(speed) + "\r"})
                else:
                    await self.arm.do_command({"command": "M2101 R-" + str(speed) + "\r"})



    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Geometry]:
        self.logger.error("`get_geometries` is not implemented")
        raise NotImplementedError()

