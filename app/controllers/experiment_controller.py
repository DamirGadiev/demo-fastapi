class ExperimentController:

    @classmethod
    async def experiment_started(cls, websocket, data, manager):
        await manager.broadcast(websocket,
                                str({"type": "EXPERIMENT", "action": "EXPERIMENT_STARTED", "data": data,
                                     "message": "#EXPERIMENT STARTED"}))

    @classmethod
    async def experiment_paused(cls, websocket, data, manager):
        await manager.broadcast(websocket,
                                str({"type": "EXPERIMENT", "action": "EXPERIMENT_PAUSED", "data": data,
                                     "message": "#EXPERIMENT PAUSED"}))

    @classmethod
    async def experiment_stoped(cls, websocket, data, manager):
        await manager.broadcast(websocket,
                                str({"type": "EXPERIMENT", "action": "EXPERIMENT_STOPED", "data": data,
                                     "message": "#EXPERIMENT STOPED"}))

    @classmethod
    async def experiment_error(cls, websocket, data, manager):
        await manager.broadcast(websocket,
                                str({"type": "EXPERIMENT", "action": "EXPERIMENT_ERROR", "data": data,
                                     "message": "#EXPERIMENT ERROR"}))

    @classmethod
    async def experiment_repeated(cls, websocket, data, manager):
        await manager.broadcast(websocket, str({"type": "EXPERIMENT", "action": "EXPERIMENT_REPEATED", "data": data,
                                                "message": "#EXPERIMENT REPEATED"}))

    @classmethod
    async def experiment_finished(cls, websocket, data, manager):
        await manager.broadcast(websocket, str({"type": "EXPERIMENT", "action": "EXPERIMENT_FINISHED", "data": data,
                                                "message": "#EXPERIMENT FINISHED"}))

    @classmethod
    async def not_found_command(cls, websocket, data, manager):
        await manager.broadcast(websocket, str({"type": "EXPERIMENT", "action": "",
                                                "data": {"type": "error", "message": "Not  Found Command"},
                                                "message": ""}))
