# Module dexarm

This module adds support for the Rotrics DexArm. Support is currently limited to only the arm itself and the pen-style end-effector.

## Model naomi:dexarm:dexarm

The arm model, with which you can move the DexArm around.

### Configuration

Use the following attribute table to configure this model:

```json
{
  "port": <string>
}
```

#### Attributes

The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `port`        | string | Required  | The port for your arm.     |

#### Example Configuration

```json
{
  "port": "/dev/tty.usbmodem2053398E47531"
}
```

## Model naomi:dexarm:rotary-gripper

A gripper model for the Rotrics DexArm pen-style end-effector. The pneumatic options for gripping and releasign are untested as they are non-functional on my device. I believe it's a firmware issue. If anyone reads this and knows how to use it please reach out in the issues.

### Configuration

Use the following attribute table to configure this model:

```json
{
  "arm_name": "<arm-name>"
}
```

#### Attributes

The following attributes are available for this model:

| Name        | Type   | Inclusion | Description                                             |
|-------------|--------|-----------|---------------------------------------------------------|
| `rotary_gripper`  | string | Required  | The arm resource the pen-style end-effector depends on. |

#### Example Configuration

```json
{
  "arm_name": "arm-1"
}
```

### DoCommand: `rotate_wrist`

| Name            | Type    | Inclusion | Description                                             |
|-----------------|---------|-----------|---------------------------------------------------------|
| `speed`         | integer | Optional  | Speed of rotation (default: 1000).                      |
| `direction`     | string  | Optional  | Direction of rotation: "clockwise" or "counter-clockwise" (default: "clockwise") |
| `to_degrees`    | integer | Optional  | Target angle in degrees for absolute rotation. Will ignore all other settings.            |
| `keep_rotating` | boolean | Optional  | Whether to keep rotating continuously (default: `false`). Use the `stop()` method to stop.   |

### DoCommand examples

Rotate counter clockwise:

```json
{
  "rotate_wrist": {
    "speed": 1000,
    "direction": "clockwise"
  }
}
```

Continuously rotate counter-clockwise:

```json
{
  "rotate_wrist": {
    "speed": 1000,
    "direction": "counter-clockwise",
    "keep_rotating": true
  }
}
```

Rotate to 60 degrees:

```json
{
  "rotate_wrist": {
    "to_degrees": 60
  }
}
```
