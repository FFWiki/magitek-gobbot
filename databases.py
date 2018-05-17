LEVE_ITEMS = {"name": {}, "id": {}}
QUEST_TEXT = {"text": {}}
QUESTS = {"name": {}, "genre_name": {}, "npc_name": {}, "patch": {"name": {}, "number": {}}}
ITEM_CLASSES = {} # TODO: Add all item classes.

def items(args):
    d = {}
    for cls in ITEM_CLASSES:
        sd = {}
        for subcls in cls:
            sd[subcls] = args
        d[cls] = sd
    return d

table = {
    # TODO: Gathering, crafting
	"achievement": {
		"url": "https://api.xivdb.com/achievement",
		"keys": {
			'name': {},
                        'name_ja': {},
			'patch': {'number': {}},
			'kind_name': {},
                        'type_name': {},
                        'category_name': {},
                        'help': {},
                        'item': {},
                        'title': {}
		}
	},
        "action": {
            "url": "https://api.xivdb.com/action",
            "keys": {
                'name': {},
                'name_jp': {},
                'help_en': {},
                'level': {},
                'cost_cp': {},
                'cost_hp': {},
                'cost_mp': {},
                'cost_tp': {},
                'cast_range': {},
                'cast_time': {},
                'recast_time': {},
                'is_trait': {},
                'type_name': {},
                'patch': {'number': {}},
            },
        },
        "emote": {
            "url": "https://api.xivdb.com/emote",
            "keys": {
                'name': {},
                'name_jp': {},
                'text_command': {'command_1': {}, 'command_2': {}, 'command_3': {}, 'command_4': {}},
                'patch': {'number': {}},
            },
        },
        "enemy": {
            "url": "https://api.xivdb.com/enemy",
            "keys": {
                'name': {},
                'name_jp': {},
                'map_data': {
                    'maps': {"placename_name": {}, "zone_name": {}},
                    'stats': {'hpAvg': {}, 'hpMax': {}, 'hpMin': {}, 'levelMax': {}, 'levelMin': {}, 'mpAvg': {}, 'mpMax': {}, 'mpMin': {}},
                },
                'patch': {'number': {}},
            },
        },
        "fate": {
            "url": "https://api.xivdb.com/fate",
            "keys": {
                'name': {},
                'name_jp': {},
                'help_en': {},
                'class_level': {},
                'class_level_max': {},
                'map': {'placename': {'name': {}}},
                'patch': {'number': {}},
            },
        },
        "instance": {
            "url": "https://api.xivdb.com/instance",
            "keys": {
                'name': {},
                'name_ja': {},
                'help_en': {},
                'level': {},
                'level_sync': {},
                'time_limit': {},
                'tanks_per_party': {},
                'healers_per_party': {},
                'dps_per_party': {},
                'item_level': {},
                'item_level_sync': {},
                'content_name': {},
                'patch': {'number': {}},
            },
        },
        "item": {
            "url": "https://api.xivdb.com/item",
            "keys": {
                'name': {},
                'name_ja': {},
                'help_en': {},
                'classjob_category': {},
                'level_equip': {},
                'level_item': {},
                'category_name': {},
                'attributes_base': {'auto_attack': {}, 'auto_attack_hq': {}, 'block_rate': {}, 'block_rate_hq': {}, 'block_strength': {}, 'block_strength_hq': {},
                    'damage': {}, 'damage_hq': {}, 'defense': {}, 'defense_hq': {}, 'delay': {}, 'delay_hq': {}, 'magic_damage': {}, 'magic_damage_hq': {},
                    'magic_defense': {}, 'magic_defense_hq': {}},
                'attributes_params': {"name": {}, "value": {}, "value_hq": {}},
                'patch': {'number': {}},
            },
        },
        "leve": {
            "url": "https://api.xivdb.com/leve",
            "keys": {
                'name': {},
                'name_ja': {},
                'help_en': {},
                'gil_reward': {},
                'exp_reward': {},
                'leve_client': {},
                'class_level': {},
                'classjob_category': {},
                'time_limit': {},
                'placename': {'name': {}},
                'patch': {'number': {}},
                #'items': items(LEVE_ITEMS),
                #TODO: This
            },
        },
        "minion": {
            "url": "https://api.xivdb.com/minion",
            "keys": {
                'name': {},
                'name_ja': {},
                'info1': {},
                'info2': {},
                'summon': {},
                'behavior': {},
                'action': {},
                'attack': {},
                'cost': {},
                'hp': {},
                'defense': {},
                'skill_cost': {},
                'speed': {},
                'patch': {'number': {}},
            },
        },
        "npc": {
            "norepeat": True,
            "url": "https://api.xivdb.com/npc",
            "keys": {
                'name': {},
                'name_jp': {},
                'title': {},
                'title_de': {},
                'title_fr': {},
                'title_jp': {},
                'patch': {'number': {}},
            },
        },
        "placename": {
            "url": "https://api.xivdb.com/placename",
            "keys": {
                'name': {},
                'name_jp': {},
                'enemies': {"name": {}, "positions": {"hp": {}, "level": {}, "x": {}, "y": {}}},
                'instances': {"name": {}, "level": {}, "content_type": {}, "help": {}},
                'npcs': {"name": {}, "position": {"x": {}, "y": {}}},
                'quests': QUESTS,
                'patch': {'number': {}},
            },
        },
        "quest": {
            "url": "https://api.xivdb.com/quest",
            "keys": {
                'category_name': {},
                'exp_reward': {},
                'genre_name': {},
                'gil_reward': {},
                'name': {},
                'name_jp': {},
                'npc_start': {'name': {}},
                'npc_end': {'name': {}},
                'patch': {'number': {}},
                'pre_quests': QUESTS,
                'post_quests': QUESTS,
                'text': {'journal': QUEST_TEXT, 'todo': QUEST_TEXT},
            },
        },
        "status": {
            "url": "https://api.xivdb.com/status",
            "keys": {
                'name': {},
                'name_jp': {},
                'help': {},
                'patch': {'number': {}},
            },
        },
        "title": {
            "url": "https://api.xivdb.com/title",
            "keys": {
                'name': {},
                'name_jp': {},
                'name_female': {},
                'name_female_jp': {},
                'achivements': {"name": {}},
                'patch': {'number': {}},
            },
        },
        "weather": {
            "url": "https://api.xivdb.com/weather",
            "keys": {
                'name': {},
                'name_jp': {},
            },
        },
}

def databases():
	return table
