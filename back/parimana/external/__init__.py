from parimana.external.boatrace import category_boat
from parimana.external.netkeiba import category_jra, category_nar
from parimana.external.kdreams import category_keirin
from parimana.external.autorace import category_moto


categories = {
    cat.id: cat
    for cat in [
        category_boat,
        category_jra,
        category_nar,
        category_keirin,
        category_moto,
    ]
}

__all__ = ["categories"]
