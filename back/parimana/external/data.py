from parimana.domain.base import BettingType


# https://www.meti.go.jp/shingikai/sankoshin/seizo_sangyo/sharyo_kyogi/pdf/002_02_01.pdf p.14 # noqa
ratio_keirin = {
    BettingType.WIN: 0.0,
    BettingType.QUINELLA: 0.02,
    BettingType.EXACTA: 0.13,
    BettingType.TRIO: 0.08,
    BettingType.TRIFECTA: 0.74,
}

# https://www.meti.go.jp/shingikai/sankoshin/seizo_sangyo/sharyo_kyogi/pdf/002_02_01.pdf p.14 # noqa
ratio_auto = {
    BettingType.WIN: 0.01,  # Win,Show,Place,Wide,重勝の合計で0.02 なので 0.01とした
    BettingType.QUINELLA: 0.03,
    BettingType.EXACTA: 0.08,
    BettingType.TRIO: 0.08,
    BettingType.TRIFECTA: 0.79,
}
