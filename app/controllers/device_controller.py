from fastapi import WebSocket


class DeviceController:

    @classmethod
    async def generate_response(cls, websocket: WebSocket, action, message, manager):
        await manager.broadcast(websocket, str({
            "type": "DEVICE",
            "action": action,
            "data": message.data,
            "status": message.status,
            "message": message.message
        }))

    @classmethod
    async def device_connection_open(cls, websocket: WebSocket, message, manager):
        action = "DEVICE_CONNECTION_OPEN"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def device_camera_ready(cls, websocket: WebSocket, message, manager):
        action = "DEVICE_CAMERA_READY"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def device_camera_error(cls, websocket: WebSocket, message, manager):
        action = "DEVICE_CAMERA_ERROR"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def device_patterns_ready(cls, websocket: WebSocket, message, manager):
        action = "DEVICE_PATTERNS_READY"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def device_patterns_error(cls, websocket: WebSocket, message, manager):
        action = "DEVICE_PATTERNS_ERROR"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def device_ultraleap_ready(cls, websocket: WebSocket, message, manager):
        action = "DEVICE_ULTRALEAP_READY"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def device_ultraleap_stopped(cls, websocket: WebSocket, message, manager):
        action = "DEVICE_ULTRALEAP_STOPPED"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def device_setup_ready(cls, websocket: WebSocket, message, manager):
        action = "DEVICE_SETUP_READY"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def device_camera_stopped(cls, websocket: WebSocket, message, manager):
        action = "DEVICE_CAMERA_STOPPED"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def device_camera_detected(cls, websocket: WebSocket, message, manager):
        action = "DEVICE_CAMERA_DETECTED"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def device_camera_not_detected(cls, websocket: WebSocket, message, manager):
        action = "DEVICE_CAMERA_NOT_DETECTED"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def device_active_pattern_error(cls, websocket: WebSocket, message, manager):
        action = "DEVICE_ACTIVE_PATTERN_ERROR"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def device_active_pattern_ready(cls, websocket: WebSocket, message, manager):
        action = "DEVICE_ACTIVE_PATTERN_READY"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def not_found_command(cls, websocket: WebSocket, message, manager):
        action = ""
        message.status = {"type": "error", "description": "NOT  FOUND COMMAND"}
        await cls.generate_response(websocket, action, message, manager)
