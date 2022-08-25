from enum import Enum

from fastapi import WebSocket

from controllers.device_controller import DeviceController


class DeviceActionEnum(Enum):
    DEVICE_CONNECTION_OPEN = "DEVICE_CONNECTION_OPEN"
    DEVICE_CAMERA_READY = "DEVICE_CAMERA_READY"
    DEVICE_CAMERA_ERROR = "DEVICE_CAMERA_ERROR"
    DEVICE_PATTERNS_READY = "DEVICE_PATTERNS_READY"
    DEVICE_PATTERN_ERROR = "DEVICE_PATTERN_ERROR"
    DEVICE_ULTRALEAP_READY = "DEVICE_ULTRALEAP_READY"
    DEVICE_ULTRALEAP_ERROR = "DEVICE_ULTRALEAP_ERROR"
    DEVICE_SETUP_READY = "DEVICE_SETUP_READY"


class DeviceMessageHandler:

    @classmethod
    async def process(cls, websocket: WebSocket, message, manager):
        if message.action == DeviceActionEnum.DEVICE_CONNECTION_OPEN.name:
            await DeviceController.device_connection_open(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_CAMERA_READY.name:
            await DeviceController.device_camera_ready(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_CAMERA_ERROR.name:
            await DeviceController.device_camera_error(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_PATTERNS_READY.name:
            await DeviceController.device_patterns_ready(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_PATTERN_ERROR.name:
            await DeviceController.device_pattern_error(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_ULTRALEAP_READY.name:
            await DeviceController.device_ultraleap_ready(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_ULTRALEAP_ERROR.name:
            await DeviceController.device_ultraleap_error(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_SETUP_READY.name:
            await DeviceController.device_setup_ready(websocket, message, manager)
        else:
            await DeviceController.not_found_command(websocket, message, manager)
