from dataclasses import dataclass
from typing import Mapping

from parimana.domain.schedule import Course
from parimana.external.kdreams.base import category_keirin


@dataclass
class KeirinStudium:
    code: str
    name: str
    name_en: str

    def to_course(self):
        return Course(id=f"kr{self.code}", name=self.name, category=category_keirin)

    @classmethod
    def from_code(cls, code: str):
        return _all_courses.get(code)


studium_list = (
    # https://keirin.kdreams.jp/stadium/?l-id=l-ti-directoryNav_link_stadium
    # https://ctc.gr.jp/link/
    "函館/hakodate/11 青森/aomori/12 いわき平/iwakitaira/13"
    " 弥彦/yahiko/21 前橋/maebashi/22 取手/toride/23 宇都宮/utsunomiya/24"
    " 大宮/omiya/25 西武園/seibuen/26 京王閣/keiokaku/27 立川/tachikawa/28"
    " 松戸/matsudo/31 川崎/kawasaki/34 平塚/hiratsuka/35"
    " 小田原/odawara/36 伊東/ito/37 静岡/shizuoka/38"
    " 名古屋/nagoya/42 岐阜/gifu/43 大垣/ogaki/44 豊橋/toyohashi/45"
    " 富山/toyama/46 松阪/matsusaka/47 四日市/yokkaichi/48"
    " 福井/fukui/51 奈良/nara/53 向日町/mukomachi/54 和歌山/wakayama/55 岸和田/kishiwada/56"
    " 玉野/tamano/61 広島/hiroshima/62 防府/hofu/63"
    " 高松/takamatsu/71 小松島/komatsushima/73 高知/kochi/74 松山/matsuyama/75"
    " 小倉/kokura/81 久留米/kurume/83 武雄/takeo/84 佐世保/sasebo/85 別府/beppu/86 熊本/kumamoto/87"
)


_all_courses: Mapping[str, KeirinStudium] = {
    code: KeirinStudium(code, name, name_en)
    for name, name_en, code in (studium.split("/") for studium in studium_list.split())
}
