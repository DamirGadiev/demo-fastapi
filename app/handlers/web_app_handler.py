from enum import Enum

from controllers.web_app_controller import WebAppController


class WebAppActionEnum(Enum):
    WEB_APP_REGISTRATION = "WEB_APP_REGISTRATION"
    WEB_APP_EVALUATION_FORM = "WEB_APP_EVALUATION_FORM"
    WEB_APP_EXPERIMENT_EVALUATE = "WEB_APP_EXPERIMENT_EVALUATE"
    WEB_APP_EXPERIMENT_START = "WEB_APP_EXPERIMENT_START"
    WEB_APP_EXPERIMENT_STOP = "WEB_APP_EXPERIMENT_STOP"
    WEB_APP_EXPERIMENT_PAUSE = "WEB_APP_EXPERIMENT_PAUSE"
    WEB_APP_EXPERIMENT_REPEAT = "WEB_APP_EXPERIMENT_REPEAT"
    WEB_APP_EXPERIMENT_FINISH = "WEB_APP_EXPERIMENT_FINISH"
    WEB_APP_EXPERIMENT_ERROR = "WEB_APP_EXPERIMENT_ERROR"
    WEB_APP_NEW_SESSION = "WEB_APP_NEW_SESSION"


class WebAppMessageHandler:

    @classmethod
    async def process(cls, websocket, message,  manager):
        if message.action == WebAppActionEnum.WEB_APP_REGISTRATION.name:
            await WebAppController.web_app_registration(websocket, message,  manager)
        elif message.action == WebAppActionEnum.WEB_APP_EVALUATION_FORM.name:
            await WebAppController.evaluation_form(websocket, message,  manager)
        elif message.action == WebAppActionEnum.WEB_APP_NEW_SESSION.name:
            await WebAppController.new_session(websocket, message,  manager)
        elif message.action == WebAppActionEnum.WEB_APP_EXPERIMENT_EVALUATE.name:
            await WebAppController.experiment_evaluate(websocket, message,  manager)
        elif message.action == WebAppActionEnum.WEB_APP_EXPERIMENT_START.name:
            await WebAppController.start_experiment(websocket, message,  manager)
        elif message.action == WebAppActionEnum.WEB_APP_EXPERIMENT_STOP.name:
            await WebAppController.stop_experiment(websocket, message,  manager)
        elif message.action == WebAppActionEnum.WEB_APP_EXPERIMENT_PAUSE.name:
            await WebAppController.pause_experiment(websocket, message,  manager)
        elif message.action == WebAppActionEnum.WEB_APP_EXPERIMENT_REPEAT.name:
            await WebAppController.repeat_experiment(websocket, message,  manager)
        elif message.action == WebAppActionEnum.WEB_APP_EXPERIMENT_ERROR.name:
            await WebAppController.fail_experiment(websocket, message,  manager)
        elif message.action == WebAppActionEnum.WEB_APP_EXPERIMENT_FINISH.name:
            await WebAppController.finished_experiment(websocket, message,  manager)
        else:
            await WebAppController.not_found_command(websocket, message,  manager)
