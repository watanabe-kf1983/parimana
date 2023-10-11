from fastapi import APIRouter, Response

import parimana.webapi.model as model


router = APIRouter()


@router.post("/start-wait-30/")
def start_wait_30():
    return {"task_id": model.start_wait_30()}


@router.get("/wait-30-result/{task_id}")
def get_wait_30_result(task_id: str):
    return model.get_wait_30_result(task_id)


@router.post("/start-analyse/{race_id}")
def start_analyse(race_id: str):
    return {"task_id": model.start_analyse(race_id)}


@router.get("/analysis/{race_id}/{analyser_name}")
def get_analysis(race_id: str, analyser_name: str):
    return model.get_analysis(race_id, analyser_name)


@router.get("/analysis/{race_id}/{analyser_name}/box.png")
def get_box_image(race_id: str, analyser_name: str):
    if img := model.get_box_image(race_id, analyser_name):
        return Response(content=img, media_type="image/png")
    else:
        return {"Status": "Not Analysed yet."}


@router.get("/analysis/{race_id}/{analyser_name}/oc.png")
def get_oc_image(race_id: str, analyser_name: str):
    if img := model.get_oc_image(race_id, analyser_name):
        return Response(content=img, media_type="image/png")
    else:
        return {"Status": "Not Analysed yet."}
