from fastapi import APIRouter, Response

import parimana.app.realtime as rt


router = APIRouter()


@router.post("/start-wait-30/")
def start_wait_30():
    return {"task_id": rt.start_wait_30()}


@router.get("/wait-30-result/{task_id}")
def get_wait_30_result(task_id: str):
    return rt.get_wait_30_result(task_id)


@router.post("/analyse/start/{race_id}")
def start_analyse(race_id: str):
    return {"task_id": rt.start_analyse(race_id)}


@router.get("/analyse/status/{race_id}")
def get_status(race_id: str):
    return rt.get_status(race_id)


@router.get("/analysis/{race_id}/{analyser_name}")
def get_analysis(race_id: str, analyser_name: str):
    return rt.get_analysis(race_id, analyser_name)


@router.get("/analysis/{race_id}/{analyser_name}/box.png")
def get_box_image(race_id: str, analyser_name: str):
    img = rt.get_box_image(race_id, analyser_name)
    return Response(content=img, media_type="image/png")


@router.get("/analysis/{race_id}/{analyser_name}/oc.png")
def get_oc_image(race_id: str, analyser_name: str):
    img = rt.get_oc_image(race_id, analyser_name)
    return Response(content=img, media_type="image/png")
