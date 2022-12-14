from enum import Enum


class Items(Enum):
    PICKAXE = {
        'inventory_icon': 'assets/image/items/pickaxe.png',
        'drop_icon': 'assets/image/items/pickaxe.png',
        'mining_speed': 4,
        'durability': 17,
        'power': 1,
        'name': 'pickaxe',
        'capacity': 1
    }

    IRON_ORE = {
        'inventory_icon': 'assets/image/items/iron_icon.png',
        'drop_icon': 'assets/image/items/iron_icon.png',
        'name': 'iron ore',
        'capacity': 20
    }
