# Module dexarm

This module adds support for the Rotrics DexArm. Support is currently limited to only the arm itself, without any end effectors.

## Model naomi:dexarm:dexarm

The arm model, with which you can move the DexArm around.

### Configuration
The following attribute template can be used to configure this model:

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
