from models.evaluation_experiments import create_evaluation_experiment
from models.experiments import create_experiment
from models.profiles import create_profile
from schemas.web_app_shemas import ExperimentDataModel


class WebAppController:
    @classmethod
    async def storing_data(cls, websocket, data, manager):
        try:
            profile_id = await create_profile(gender=data.gender, age=data.age, identifier=data.identifier)
            experiment_id = await create_experiment(
                pattern_name=data.pattern_name,
                pattern_id=data.pattern_id,
                profile_id=profile_id
            )
            evaluation_experiment_id = await create_evaluation_experiment(
                sensitivity_assessment=data.sensitivity_assessment,
                mood_assessment=data.mood_assessment,
                description=data.description,
                profile_id=profile_id,
                experiment_id=experiment_id,
            )
        except Exception as e:
            await manager.broadcast(websocket, str({"type": "WEB_APP", "action": "WEB_APP_EVALUATION_FORM",
                                                    "data": {"type": "error"}, "message": f"{e}"}))

    @classmethod
    async def register_profile(cls, websocket, data, manager):
        # message = ProfileModel(**data)
        # profile_id = await create_profile(message)
        # await websocket.send_text(str({"data": {"message": "register_profile", "profile_id": profile_id}}))
        await manager.broadcast(websocket,
                                str({"type": "WEB_APP", "action": "WEB_APP_REGISTRATION", "data": data,
                                     "message": "#WEB APP REGISTRATION"}))

    @classmethod
    async def evaluation_form(cls, websocket, data, manager):
        message = ExperimentDataModel(**data)
        await cls.storing_data(websocket, message, manager)
        await manager.broadcast(websocket,
                                str({"type": "WEB_APP", "action": "WEB_APP_EVALUATION_FORM", "data": data,
                                     "message": "#WEB APP EVALUATION FORM"}))
    @classmethod
    async def experiment_evaluate(cls, websocket, data, manager):
        await manager.broadcast(websocket,
                                str({"type": "WEB_APP", "action": "WEB_APP_EXPERIMENT_EVALUATE", "data": data,
                                     "message": "#WEB APP EXPERIMENT EVALUATE"}))

    @classmethod
    async def start_experiment(cls, websocket, data, manager):
        # message = ExperimentModel(**data)
        # experiment_id = await create_experiment(message)
        # await websocket.send_text(str({"data": {"message": "start_experiment", "experiment_id": experiment_id}}))
        await manager.broadcast(websocket,
                                str({"type": "WEB_APP", "action": "WEB_APP_EXPERIMENT_START", "data": data,
                                     "message": "#WEB APP EXPERIMENT START"}))

    @classmethod
    async def stop_experiment(cls, websocket, data, manager):
        # message = ExperimentStatusModel(**data)
        # experiment_id = await update_experiment_status(
        #     message.experiment_id, message.profile_id, ExperimentStatusEnum.stopped
        # )
        # await websocket.send_text(str({"data": {"message": "stop_experiment", "experiment_id": experiment_id}}))
        await manager.broadcast(websocket,
                                str({"type": "WEB_APP", "action": "WEB_APP_EXPERIMENT_STOP", "data": data,
                                     "message": "#WEB APP EXPERIMENT STOP"}))

    @classmethod
    async def repeat_experiment(cls, websocket, data, manager):
        # message = ExperimentStatusModel(**data)
        # experiment_id = await update_experiment_status(
        #     message.experiment_id, message.profile_id, ExperimentStatusEnum.repeat
        # )
        # await websocket.send_text(str({"data": {"message": "repeat_experiment", "experiment_id": experiment_id}}))
        await manager.broadcast(websocket, str({"type": "WEB_APP", "action": "WEB_APP_EXPERIMENT_REPEAT", "data": data,
                                                "message": "#WEB APP EXPERIMENT REPEAT"}))

    @classmethod
    async def fail_experiment(cls, websocket, data, manager):
        # message = ExperimentStatusModel(**data)
        # experiment_id = await update_experiment_status(
        #     message.experiment_id, message.profile_id, ExperimentStatusEnum.failed
        # )
        # await websocket.send_text(str({"data": {"message": "fail_experiment", "experiment_id": experiment_id}}))
        await manager.broadcast(websocket,
                                str({"type": "WEB_APP", "action": "WEB_APP_EXPERIMENT_FAIL", "data": data,
                                     "message": "#WEB APP EXPERIMENT FAIL"}))

    @classmethod
    async def finished_experiment(cls, websocket, data, manager):
        # message = ExperimentStatusModel(**data)
        # experiment_id = await update_experiment_status(
        #     message.experiment_id, message.profile_id, ExperimentStatusEnum.finished
        # )
        # await websocket.send_text(str({"data": {"message": "finished_experiment", "experiment_id": experiment_id}}))
        await manager.broadcast(websocket, str({"type": "WEB_APP", "action": "WEB_APP_EXPERIMENT_FINISH", "data": data,
                                                "message": "#WEB APP EXPERIMENT FINISH"}))

    @classmethod
    async def not_found_command(cls, websocket, data, manager):
        await manager.broadcast(websocket, str({"type": "WEB_APP", "action": "", "data": {"type": "error"},
                                                "message": "Not  Found Command"}))
