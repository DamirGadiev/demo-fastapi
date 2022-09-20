from enum import Enum

from fastapi import WebSocket

from controllers.device_controller import DeviceController


class DeviceActionEnum(Enum):
    DEVICE_ULTRALEAP_READY = "DEVICE_ULTRALEAP_READY"
    DEVICE_ULTRALEAP_ERROR = "DEVICE_ULTRALEAP_STOPPED"
    DEVICE_PATTERNS_READY = "DEVICE_PATTERNS_READY"
    DEVICE_PATTERNS_ERROR = "DEVICE_PATTERNS_ERROR"
    DEVICE_ACTIVE_PATTERN_ERROR = "DEVICE_ACTIVE_PATTERN_ERROR"
    DEVICE_ACTIVE_PATTERN_READY = "DEVICE_ACTIVE_PATTERN_READY"
    DEVICE_CONNECTION_OPEN = "DEVICE_CONNECTION_OPEN"
    DEVICE_CAMERA_READY = "DEVICE_CAMERA_READY"
    DEVICE_CAMERA_STOPPED = "DEVICE_CAMERA_STOPPED"
    DEVICE_CAMERA_DETECTED = "DEVICE_CAMERA_DETECTED"
    DEVICE_CAMERA_NOT_DETECTED = "DEVICE_CAMERA_NOT_DETECTED"
    DEVICE_SETUP_READY = "DEVICE_SETUP_READY"


class DeviceMessageHandler:

    @classmethod
    async def process(cls, websocket: WebSocket, message, manager):
        if message.action == DeviceActionEnum.DEVICE_CONNECTION_OPEN.name:
            await DeviceController.device_connection_open(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_CAMERA_READY.name:
            await DeviceController.device_camera_ready(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_PATTERNS_READY.name:
            await DeviceController.device_patterns_ready(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_PATTERNS_ERROR.name:
            await DeviceController.device_patterns_error(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_ULTRALEAP_READY.name:
            await DeviceController.device_ultraleap_ready(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_ULTRALEAP_ERROR.name:
            await DeviceController.device_ultraleap_error(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_SETUP_READY.name:
            await DeviceController.device_setup_ready(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_CAMERA_STOPPED.name:
            await DeviceController.device_camera_stopped(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_CAMERA_DETECTED.name:
            await DeviceController.device_camera_detected(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_CAMERA_NOT_DETECTED.name:
            await DeviceController.device_camera_not_detected(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_ACTIVE_PATTERN_ERROR.name:
            await DeviceController.device_active_pattern_error(websocket, message, manager)
        elif message.action == DeviceActionEnum.DEVICE_ACTIVE_PATTERN_READY.name:
            await DeviceController.device_active_pattern_ready(websocket, message, manager)
        else:
            await DeviceController.not_found_command(websocket, message, manager)
