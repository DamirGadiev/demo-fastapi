from enum import Enum

from controllers.experiment_controller import ExperimentController


class ExperimentActionEnum(Enum):
    EXPERIMENT_STARTED = "EXPERIMENT_STARTED"
    EXPERIMENT_PAUSED = "EXPERIMENT_PAUSED"
    EXPERIMENT_STOPED = "EXPERIMENT_STOPED"
    EXPERIMENT_ERROR = "EXPERIMENT_ERROR"
    EXPERIMENT_REPEATED = "EXPERIMENT_REPEATED"
    EXPERIMENT_FINISHED = "EXPERIMENT_FINISHED"


class ExperimentMessageHandler:

    @classmethod
    async def process(cls, websocket, message, manager):
        if message.action == ExperimentActionEnum.EXPERIMENT_STARTED.name:
            await ExperimentController.experiment_started(websocket, message.data, manager)
        elif message.action == ExperimentActionEnum.EXPERIMENT_PAUSED.name:
            await ExperimentController.experiment_paused(websocket, message.data, manager)
        elif message.action == ExperimentActionEnum.EXPERIMENT_STOPED.name:
            await ExperimentController.experiment_stoped(websocket, message.data, manager)
        elif message.action == ExperimentActionEnum.EXPERIMENT_ERROR.name:
            await ExperimentController.experiment_error(websocket, message.data, manager)
        elif message.action == ExperimentActionEnum.EXPERIMENT_REPEATED.name:
            await ExperimentController.experiment_repeated(websocket, message.data, manager)
        elif message.action == ExperimentActionEnum.EXPERIMENT_FINISHED.name:
            await ExperimentController.experiment_finished(websocket, message.data, manager)
        else:
            await ExperimentController.not_found_command(websocket, message.data, manager)
