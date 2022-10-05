from fastapi import WebSocket

from models.evaluation_experiments import create_evaluation_experiment
from models.experiments import create_experiment
from models.profiles import create_profile
from schemas.web_app_shemas import ExperimentDataModel


class WebAppController:
    @classmethod
    async def storing_data(cls, websocket: WebSocket, data, manager):
        try:
            profile_id = await create_profile(gender=data.gender, age=data.age, identifier=data.identifier)
            experiment_id = await create_experiment(
                pattern_name=data.pattern_name,
                pattern_id=data.pattern_id,
                profile_id=profile_id
            )
            evaluation_experiment_id = await create_evaluation_experiment(
                valence=data.valence,
                arousal=data.arousal,
                intensity=data.intensity,
                sharpness=data.sharpness,
                roughness=data.roughness,
                regularity=data.regularity,
                shape_recognition=data.shape_recognition,
                description=data.description,
                question_1=data.question_1,
                question_2=data.question_2,
                correct_hand_position_procentage=data.correct_hand_position_procentage,
                profile_id=profile_id,
                experiment_id=experiment_id,
            )
        except Exception as e:
            await manager.broadcast(websocket, str({
                "type": "WEB_APP",
                "action": "WEB_APP_EVALUATION_FORM",
                "data": {},
                "status": {"type": "error", "description": f"{e}"},
                "message": ""
            }))

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
    async def web_app_registration(cls, websocket: WebSocket, message, manager):
        action = "WEB_APP_REGISTRATION"
        message.status = {"type": "success", "description": "Web app registration"}
        message.message = "#WEB APP REGISTRATION"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def evaluation_form(cls, websocket: WebSocket, message, manager):
        data = ExperimentDataModel(**message.data)
        await cls.storing_data(websocket, data, manager)

        action = "WEB_APP_EVALUATION_FORM"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def experiment_evaluate(cls, websocket: WebSocket, message, manager):
        action = "WEB_APP_EXPERIMENT_EVALUATE"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def new_session(cls, websocket: WebSocket, message, manager):
        action = "WEB_APP_NEW_SESSION"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def start_experiment(cls, websocket: WebSocket, message, manager):
        action = "WEB_APP_EXPERIMENT_START"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def stop_experiment(cls, websocket: WebSocket, message, manager):
        action = "WEB_APP_EXPERIMENT_STOP"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def pause_experiment(cls, websocket: WebSocket, message, manager):
        action = "WEB_APP_EXPERIMENT_PAUSE"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def repeat_experiment(cls, websocket: WebSocket, message, manager):
        action = "WEB_APP_EXPERIMENT_REPEAT"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def fail_experiment(cls, websocket: WebSocket, message, manager):
        action = "WEB_APP_EXPERIMENT_FAIL"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def finished_experiment(cls, websocket: WebSocket, message, manager):
        action = "WEB_APP_EXPERIMENT_FINISH"
        await cls.generate_response(websocket, action, message, manager)

    @classmethod
    async def not_found_command(cls, websocket: WebSocket, message, manager):
        action = ""
        message.status = {"type": "error", "description": "NOT FOUND COMMAND"}
        await cls.generate_response(websocket, action, message, manager)
