from fastapi import WebSocket


class ExperimentController:

    @classmethod
    async def generate_response(cls, websocket: WebSocket, action: str, message, manager):
        await manager.broadcast(websocket, str({
            "type": "EXPERIMENT",
            "action": action,
            "data": message.data,
            "status": message.status,
            "message": message.message
        }))

    @classmethod
    async def experiment_started(cls, websocket: WebSocket, message, manager):
        action = "EXPERIMENT_STARTED"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def experiment_paused(cls, websocket: WebSocket, message, manager):
        action = "EXPERIMENT_PAUSED"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def experiment_stoped(cls, websocket: WebSocket, message, manager):
        action = "EXPERIMENT_STOPED"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def experiment_error(cls, websocket: WebSocket, message, manager):
        action = "EXPERIMENT_ERROR"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def experiment_repeated(cls, websocket: WebSocket, message, manager):
        action = "EXPERIMENT_REPEATED"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def experiment_finished(cls, websocket: WebSocket, message, manager):
        action = "EXPERIMENT_FINISHED"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def not_found_command(cls, websocket: WebSocket, message, manager):
        action = ""
        message.status = {"type": "error", "description": "NOT  FOUND COMMAND"}
        await cls.generate_response(websocket, action, message, manager)
