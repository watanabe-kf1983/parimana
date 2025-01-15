from typing import Any, AsyncGenerator, Optional, Sequence
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from parimana.tasks import AnalyseTaskOptions
from parimana.ui.web.model.analyse import EyeExpectedValue, Result, Status
from parimana.context import context as cx


router = APIRouter()

if not cx.settings.auto_analyse_mode:

    @router.post("/{race_id}/start")
    def start_analyse(race_id: str):
        options = AnalyseTaskOptions(race_id, analyser_names=["no_cor", "ppf_mtx"])
        task_id = cx.analyse_tasks.scrape_and_analyse(options).delay().id
        return {"task_id": task_id}

    @router.get("/{race_id}/progress", response_class=StreamingResponse)
    async def get_progress(race_id: str):
        return _eventStreamResponse(
            cx.publish_center.get_channel(f"analyse_{race_id}").alisten()
        )


@router.get("/{race_id}/status")
def get_status(race_id: str) -> Status:
    race = cx.race_selector.select(race_id)
    return Status(
        is_processing=cx.ps_manager.load_status(f"analyse_{race_id}").is_processing,
        has_analysis=cx.analyse_app.has_analysis(race),
        is_odds_confirmed=cx.analyse_app.is_odds_confirmed(race),
    )


@router.get("/{race_id}/{analyser_name}")
def get_analysis(race_id: str, analyser_name: str) -> Result:
    race = cx.race_selector.select(race_id)
    return Result.from_base(*cx.analyse_app.get_analysis(race, analyser_name))


@router.get("/{race_id}/{analyser_name}/candidates")
def get_candidates(
    race_id: str, analyser_name: str, query: Optional[str] = Query(None)
) -> Sequence[EyeExpectedValue]:
    race = cx.race_selector.select(race_id)
    charts, _, __ = cx.analyse_app.get_analysis(race, analyser_name)
    return [
        EyeExpectedValue.from_base(eev) for eev in charts.result.recommend2(query=query)
    ]


def _eventStreamResponse(generator: AsyncGenerator[str, Any]):
    return StreamingResponse(
        (f"data: {msg}\n\n" async for msg in generator),
        media_type="text/event-stream",
    )
