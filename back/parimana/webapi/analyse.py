from typing import Any, AsyncGenerator, Optional
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

import parimana.app.realtime as rt


router = APIRouter()


# @router.post("/start-wait-30/")
# def start_wait_30():
#     return {"task_id": rt.start_wait_30()}


# @router.get("/wait-30-result/{task_id}")
# def get_wait_30_result(task_id: str):
#     return rt.get_wait_30_result(task_id)


@router.post("/{race_id}/start")
def start_analyse(race_id: str):
    return {"task_id": rt.start_analyse(race_id)}


@router.get("/{race_id}/status")
def get_status(race_id: str):
    return rt.get_status(race_id)


@router.get("/{race_id}/progress", response_class=StreamingResponse)
async def get_progress(race_id: str):
    return eventStreamResponse(rt.get_progress(race_id))


@router.get("/{race_id}/{analyser_name}")
def get_analysis(race_id: str, analyser_name: str):
    return rt.get_analysis(race_id, analyser_name)


@router.get("/{race_id}/{analyser_name}/candidates")
def get_candidates(
    race_id: str, analyser_name: str, query: Optional[str] = Query(None)
):
    return rt.get_candidates(race_id, analyser_name, query or "")


# @router.get("/analysis/{race_id}/{analyser_name}/box.png")
# def get_box_image(race_id: str, analyser_name: str):
#     img = rt.get_box_image(race_id, analyser_name)
#     return Response(content=img, media_type="image/png")


# @router.get("/analysis/{race_id}/{analyser_name}/oc.png")
# def get_oc_image(race_id: str, analyser_name: str):
#     img = rt.get_oc_image(race_id, analyser_name)
#     return Response(content=img, media_type="image/png")


def eventStreamResponse(generator: AsyncGenerator[str, Any]):
    return StreamingResponse(
        (f"data: {msg}\n\n" async for msg in generator), media_type="text/event-stream"
    )
