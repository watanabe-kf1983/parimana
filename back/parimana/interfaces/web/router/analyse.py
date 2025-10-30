from typing import Annotated, Any, AsyncGenerator, Optional, Sequence
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from parimana.app.exception import ResultNotExistError
from parimana.domain.race import OddsTimeStamp, Race
from parimana.tasks import AnalyseTaskOptions
from parimana.interfaces.web.model.analyse import (
    EyeExpectedValue,
    Result,
    Status,
    # NoModelResult,
)
from parimana.context import context as cx


def get_race(race_id: str) -> Race:
    try:
        return cx.race_selector.select(race_id)
    except Exception:
        raise ResultNotExistError(f"race_id {race_id} is not valid")


def get_timestamp(timestamp_id: str) -> OddsTimeStamp:
    try:
        return OddsTimeStamp.from_str(timestamp_id)
    except Exception:
        raise ResultNotExistError(f"timestamp_id {timestamp_id} is not valid")


RaceDeps = Annotated[Race, Depends(get_race)]
TimestampDeps = Annotated[OddsTimeStamp, Depends(get_timestamp)]

router = APIRouter()

if not cx.settings.auto_analyse_mode:

    @router.post("/{race_id}/start")
    def start_analyse(race_id: str):
        options = AnalyseTaskOptions(
            race_id, analyser_names=["no_cor", "ppf_mtx", "yurayura"]
        )
        task_id = cx.analyse_tasks.scrape_and_analyse(options).delay().id
        return {"task_id": task_id}

    @router.get("/{race_id}/progress", response_class=StreamingResponse)
    async def get_progress(race_id: str):
        return _eventStreamResponse(
            cx.publish_center.get_channel(f"analyse_{race_id}").alisten()
        )


@router.get("/{race_id}/status")
def get_status(race: RaceDeps) -> Status:
    return Status(
        is_processing=cx.ps_manager.load_status(
            f"analyse_{race.race_id}"
        ).is_processing,
        has_analysis=cx.analyse_app.has_analysis(race),
        is_odds_confirmed=cx.analyse_app.is_odds_confirmed(race),
    )


@router.get("/{race_id}/latest/list")
def get_latest_list(race: RaceDeps) -> Sequence[str]:
    items, _ = cx.analyse_app.list_latest_analysis(race)
    return items


# @router.get("/{race_id}/latest/combined")
# def get_latest_combined(race: RaceDeps) -> NoModelResult:
#     ots = cx.analyse_app.get_latest_time_stamp(race)
#     candidates = cx.analyse_app.get_combined_candidates(race, ots)
#     return NoModelResult.from_base(candidates=candidates, race=race, ots=ots)


@router.get("/{race_id}/latest/{analyser_name}")
def get_latest_analysis(race: RaceDeps, analyser_name: str) -> Result:
    charts, ots = cx.analyse_app.get_latest_analysis(race, analyser_name)
    return Result.from_base(charts=charts, race=race, ots=ots)


# @router.get("/{race_id}/{timestamp_id}/combined/candidates")
# def get_combined_candidates(
#     race: RaceDeps, timestamp: TimestampDeps, query: Optional[str] = Query(None)
# ) -> Sequence[EyeExpectedValue]:

#     candidates = cx.analyse_app.get_combined_candidates(race, timestamp, query)
#     return [EyeExpectedValue.from_base(eev) for eev in candidates]


@router.get("/{race_id}/{timestamp_id}/{analyser_name}/candidates")
def get_candidates(
    race: RaceDeps,
    timestamp: TimestampDeps,
    analyser_name: str,
    query: Optional[str] = Query(None),
) -> Sequence[EyeExpectedValue]:

    candidates = cx.analyse_app.get_candidates(race, timestamp, analyser_name, query)
    return [EyeExpectedValue.from_base(eev) for eev in candidates]


def _eventStreamResponse(generator: AsyncGenerator[str, Any]):
    return StreamingResponse(
        (f"data: {msg}\n\n" async for msg in generator),
        media_type="text/event-stream",
    )
