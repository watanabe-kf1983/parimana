from dataclasses import dataclass

import pandas as pd
import scipy.stats

import parimana.analyse.normal_dist as nd


def _estimate_ability_gap_mtx(
    corwr_df: pd.DataFrame, uncertainty: pd.Series
) -> pd.Series:
    uncertainty = uncertainty.rename("unc")

    return (
        corwr_df.join(uncertainty, on="a")
        .join(uncertainty, on="b", rsuffix="_b")
        .apply(
            lambda r: nd.estimate_mean_delta(
                pp=r["win_rate"], sd_x=r["unc"], sd_y=r["unc_b"], cor=r["cor"]
            ),
            axis=1,
        )
        .rename("ability_gap")
    )


@dataclass(frozen=True)
class UMapScore:
    u_map: pd.Series
    score: float
    u_map_suggest: pd.Series


def _evaluate_u_map(corwr_df: pd.DataFrame, u_map: pd.Series) -> UMapScore:
    gap_mtx = _estimate_ability_gap_mtx(corwr_df, u_map)
    gap_mtx_std = gap_mtx.groupby("a").std().rename_axis("m")
    gap_mtx_std_gmean = scipy.stats.mstats.gmean(gap_mtx_std.values)
    u_map_suggest = u_map * gap_mtx_std_gmean / gap_mtx_std
    score = gap_mtx_std.std()
    return UMapScore(u_map, score, u_map_suggest)


def find_uncertainty_map(corwr_df: pd.DataFrame) -> pd.Series:
    umap_initial = pd.Series(
        data=1, index=corwr_df.index.unique(level="a"), name="unc"
    ).rename_axis("m")
    score = UMapScore(u_map=None, score=float("inf"), u_map_suggest=umap_initial)

    for i in range(50):
        score_prev, score = score, _evaluate_u_map(corwr_df, score.u_map_suggest)
        if score_prev.score <= score.score:
            return score_prev.u_map

    return score.u_map


def estimate_ability_map(corwr_df: pd.DataFrame, u_map: pd.Series) -> pd.Series:
    mtx = _estimate_ability_gap_mtx(corwr_df, u_map)
    mean = mtx.groupby("a").mean().rename("mean")
    df = mtx.to_frame().join(mean, on="a")
    std_ability_gap = df["ability_gap"] - df["mean"]
    return std_ability_gap.groupby("b").mean().rename_axis("m")
