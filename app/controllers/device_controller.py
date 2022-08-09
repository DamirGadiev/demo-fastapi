class DeviceController:

    @classmethod
    async def device_connection_open(cls, websocket, data, manager):
        await manager.broadcast(websocket, str({"type": "DEVICE", "action": "DEVICE_CONNECTION_OPEN", "data": data,
                                                "message": "#DEVICE CONNECTION OPEN"}))

    @classmethod
    async def device_camera_ready(cls, websocket, data, manager):
        await manager.broadcast(websocket,
                                str({"type": "DEVICE", "action": "DEVICE_CAMERA_READY", "data": data,
                                     "message": "#DEVICE CAMERA READY"}))

    @classmethod
    async def device_camera_error(cls, websocket, data, manager):
        await manager.broadcast(websocket,
                                str({"type": "DEVICE", "action": "DEVICE_CAMERA_ERROR", "data": data,
                                     "message": "#DEVICE CAMERA ERROR"}))

    @classmethod
    async def device_patterns_ready(cls, websocket, data, manager):
        await manager.broadcast(websocket,
                                str({"type": "DEVICE", "action": "DEVICE_PATTERNS_READY", "data": data,
                                     "message": "#DEVICE PATTERNS READY"}))

    @classmethod
    async def device_pattern_error(cls, websocket, data, manager):
        await manager.broadcast(websocket,
                                str({"type": "DEVICE", "action": "DEVICE_PATTERN_ERROR", "data": data,
                                     "message": "#DEVICE PATTERN ERROR"}))

    @classmethod
    async def device_ultraleap_ready(cls, websocket, data, manager):
        await manager.broadcast(websocket, str({"type": "DEVICE", "action": "DEVICE_ULTRALEAP_READY", "data": data,
                                                "message": "#DEVICE ULTRALEAP READY"}))

    @classmethod
    async def device_ultraleap_error(cls, websocket, data, manager):
        await manager.broadcast(websocket, str({"type": "DEVICE", "action": "DEVICE_ULTRALEAP_ERROR", "data": data,
                                                "message": "#DEVICE ULTRALEAP ERROR"}))

    @classmethod
    async def device_setup_ready(cls, websocket, data, manager):
        await manager.broadcast(websocket,
                                str({"type": "DEVICE", "action": "DEVICE_SETUP_READY", "data": data,
                                     "message": "#DEVICE SETUP READY"}))

    @classmethod
    async def not_found_command(cls, websocket, data, manager):
        await manager.broadcast(websocket, str({"type": "DEVICE", "action": "",
                                                "data": {"type": "error", "message": "Not  Found Command"},
                                                "message": ""}))
