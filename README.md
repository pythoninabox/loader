# python in a box

micropython object in a box equipped with a esp32 microcontroller

## installation

### Prerequisites

- windows, linux or mac osx
- python3
- esptool

### firmware 

Download micropython for esp32 from [here](https://micropython.org/download/esp32/), and install it on board with the following command:

```bash
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
```

```bash
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-xxx-vyyy.bin
```

## Connections (v0.1)

| **DEVICE**  | **pin** | **ESP32** |
| ----------- | ------- | --------- |
| PUSH Button | 1       | 32        |
| PUSH Button | 2       | GND       |
| POT         | V       | 3V3       |
| POT         | GND     | GND       |
| POT         | Signal  | 33        |
| SPEAKER     | +       | 25        |
| SPEAKER     | -       | GND       |

## Proposals

Insert a piezodisc as _knocker_

