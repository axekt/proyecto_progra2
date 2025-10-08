# menu_catalog.py
from typing import List
from ElementoMenu import CrearMenu
from Ingrediente import Ingrediente
from IMenu import IMenu

def get_default_menus() -> List[IMenu]:
    return [
        CrearMenu(
            "Completo",
            [
                Ingrediente("Vienesa","unid", 1),
                Ingrediente("Pan de completo","unid", 1),
                Ingrediente("Palta","kg",0.5),
                Ingrediente("Tomate","kg",0.2),
            ],
            precio=1800,
            icono_path="IMG/icono_hotdog_sin_texto_64x64.png",
        ),
    ]