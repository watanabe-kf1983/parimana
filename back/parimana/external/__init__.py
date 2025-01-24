from parimana.external.boatrace import category_boat
from parimana.external.netkeiba import category_jra, category_nar
from parimana.external.kdreams import category_keirin


categories = {
    cat.id: cat
    for cat in [
        category_boat,
        category_jra,
        category_nar,
        category_keirin,
    ]
}

__all__ = ["categories"]
