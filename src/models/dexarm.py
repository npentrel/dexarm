from typing import (Any, ClassVar, Dict, Final, List, Mapping, Optional,
                    Sequence, Tuple)

from typing_extensions import Self
from viam.components.arm import *
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes

from .pydexarm import Dexarm as Pydexarm


class Dexarm(Arm, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(ModelFamily("naomi", "dexarm"), "dexarm")
    port = ""
    dexarm = None
    moving = False

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Arm component.
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
        fields = config.attributes.fields
        if "port" not in fields:
            raise ValueError("port is a required configuration attribute")
        elif not fields["port"].HasField("string_value"):
            raise ValueError("port value must be a string")
        elif fields["port"].string_value == "":
            raise ValueError("port cannot be empty")
        return [], []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both required and optional)
        """
        if self.port != config.attributes.fields["port"].string_value:
            if self.dexarm:
                    self.dexarm.close()
            self.logger.info("Reconfiguring Dexarm")
            self.port = config.attributes.fields["port"].string_value
            self.dexarm = Pydexarm(self.port)
            self.dexarm.go_home()
        else:
            self.logger.info("No port change, skipping Dexarm reconfiguration")

        return super().reconfigure(config, dependencies)

    async def get_end_position(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Pose:
        pos = self.dexarm.get_current_position()
        return Pose(x=pos[0], y=pos[1], z=pos[2])

    async def move_to_position(
        self,
        pose: Pose,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ):
        self.logger.info(f"Moving to position: {pose}")
        self.dexarm.move_to(pose.x, pose.y, pose.z)

    async def move_to_joint_positions(
        self,
        positions: JointPositions,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ):
        self.logger.error("`move_to_joint_positions` is not implemented")
        raise NotImplementedError()

    async def get_joint_positions(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> JointPositions:
        pos = self.dexarm.get_current_position()
        return JointPositions(values=[pos[4], pos[5], pos[6], 0, 0, 0])

    async def stop(
        self,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ):
        self.logger.info("Moving home")
        self.dexarm.go_home()

    async def is_moving(self) -> bool:
        self.logger.error("`is_moving` is not implemented. DexArms operate with a queue.")
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
        self.logger.error("`do_command` is not implemented")
        raise NotImplementedError()

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Geometry]:
        self.logger.error("`get_geometries` is not implemented")
        raise NotImplementedError()

