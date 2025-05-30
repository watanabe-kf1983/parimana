from enum import Enum
from itertools import combinations, permutations, chain
from typing import Collection, Sequence, Callable, TypeVar
from dataclasses import dataclass
from functools import cached_property
import re

T = TypeVar("T")


class BettingType(Enum):
    WIN = (1, True, 1, 1)
    PLACE = (2, False, 1, 2, "[P]")
    SHOW = (3, False, 1, 3, "[S]")
    EXACTA = (4, True, 2, 2)
    QUINELLA = (5, False, 2, 2)
    WIDE = (6, False, 2, 3, "[W]")
    TRIFECTA = (7, True, 3, 3)
    TRIO = (8, False, 3, 3)

    def __init__(
        self,
        id: int,
        sequencial: bool,
        size: int,
        place: int,
        suffix: str = "",
    ):
        self.id: int = id
        self.sequencial: bool = sequencial
        self.size: int = size
        self.place: int = place
        self.suffix: str = suffix

    @classmethod
    def from_size_and_type(
        cls, sequencial: bool, size: int, place: int
    ) -> "BettingType":
        for bt in BettingType:
            if (sequencial == bt.sequencial) and size == bt.size and place == bt.place:
                return bt

        raise ValueError(f"{sequencial} {size} {place} type not exists.")

    @classmethod
    def from_suffix(cls, suffix: str) -> "BettingType":
        for bt in BettingType:
            if suffix == bt.suffix:
                return bt

        raise ValueError(f"suffix {suffix} type not exists.")


pattern = re.compile(r"^(?P<body>[^\[]*)(?P<suffix>(\[[PSW]\])?)$")


@dataclass(frozen=True)
class Eye:
    """
    Eye = 賭け目

    私
    日本語だと「賭け目」「出目」といった言葉に含まれる、「目」という言葉は 一般に「賭けの対象の数字」を意味しますが、
    英語でそれに相当する言葉はないのですね。

    ChatGPT
    そうです、英語で「賭け目」や「出目」という特定の文脈における意味を直訳する一般的な言葉はありません。
    日本語の「目」が、賭けやギャンブルの文脈で特定の数字や結果を指す用語として一般的であるのに対し、
    英語ではそのような言葉が特に一般的ではありません。英語では、具体的な文脈に応じて数字や結果を指す適切な用語を使うことが一般的です。
    例えば、「number」や「outcome」がそのような文脈で使われます。

    私
    プログラミングで変数やクラスの命名をするときに、「number」や「outcome」だと意味がぼやけすぎて困りますね。

    ChatGPT
    理解します。

    私
    いっそのこと、十分にコメントを残したうえで、 Eye という単語を使ってしまおうと思います。

    ChatGPT
    コメントを使って、変数やクラスの目的や内容を明確に説明するのは素晴らしいアプローチです。
    また、"Eye" という単語を使って、より具体的でわかりやすい名前を付けることも良いアイデアです。
    良いコードの実装を目指して、頑張ってください！

    """

    text: str

    @cached_property
    def suffix(self) -> str:
        m = pattern.match(self.text)
        return m.group("suffix") if m else ""

    @cached_property
    def body(self) -> str:
        m = pattern.match(self.text)
        return m.group("body") if m else ""

    @cached_property
    def names(self) -> Collection[str]:
        name_list = re.split("[=-]", self.body)
        name_set = set(name_list)
        if not (len(name_list) == len(name_set)):
            raise ValueError(f"names duplicated: {name_list}")

        return name_set if self.suffix or ("=" in self.body) else name_list

    @cached_property
    def type(self) -> BettingType:
        if self.suffix:
            return BettingType.from_suffix(self.suffix)

        sequencial: bool = isinstance(self.names, Sequence)
        size: int = len(self.names)
        return BettingType.from_size_and_type(sequencial, size, size)

    def map(self, mapper: Callable[[str], T]) -> Collection[T]:
        if self.type.sequencial:
            return [mapper(n) for n in self.names]
        else:
            return {mapper(n) for n in self.names}

    def __str__(self):
        return self.text

    @classmethod
    def eyes_from_places(cls, places: Sequence[str]) -> Collection["Eye"]:
        return list(
            chain.from_iterable(cls.from_places(places, t) for t in BettingType)
        )

    @classmethod
    def all_eyes(cls, names: Sequence[str], t: BettingType) -> Sequence["Eye"]:
        if t.sequencial:
            return [cls.from_names(p, t) for p in permutations(names, t.size)]
        else:
            return [cls.from_names(p, t) for p in combinations(names, t.size)]

    @classmethod
    def from_names(cls, names: Sequence[str], t: BettingType) -> "Eye":
        won = names[: t.size]
        if t.sequencial:
            return Eye("-".join(won) + t.suffix)
        else:
            won = sorted(won)
            return Eye("=".join(won) + t.suffix)

    @classmethod
    def from_places(cls, places: Sequence[str], t: BettingType) -> Sequence["Eye"]:
        return [
            cls.from_names(names, t)
            for names in combinations(places[: t.place], t.size)
        ]
