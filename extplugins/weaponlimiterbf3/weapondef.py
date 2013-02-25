
WEAPON_NAMES_BY_ID = {
    'AEK-971': {'type': 'assault rifle', 'name': 'AEK-971'},
    'Weapons/AK74M/AK74': {'type': 'assault rifle', 'name': 'AK-74M', 'kit': 'assault'},
    'AN-94 Abakan': {'type': 'assault rifle', 'name': 'AN-94', 'kit': 'assault'},
    'Steyr AUG': {'type': 'assault rifle', 'name': 'AUG A3', 'kit': 'assault'},
    'F2000': {'type': 'assault rifle', 'name': 'F2000', 'kit': 'assault'},
    'FAMAS': {'type': 'assault rifle', 'name': 'FAMAS', 'kit': 'assault'},
    'Weapons/G3A3/G3A3': {'type': 'assault rifle', 'name': 'G3A3', 'kit': 'assault'},
    'Weapons/KH2002/KH2002': {'type': 'assault rifle', 'name': 'KH2002', 'kit': 'assault'},
    'Weapons/XP1_L85A2/L85A2': {'type': 'assault rifle', 'name': 'L85A2', 'kit': 'assault'},
    'M16A4': {'type': 'assault rifle', 'name': 'M16A3', 'kit': 'assault'},
    'M416': {'type': 'assault rifle', 'name': 'M416', 'kit': 'assault'},
    'SCAR-L': {'type': 'assault rifle', 'name': 'SCAR-L', 'kit': 'assault'},
    'Defib': {'type': None, 'name': 'DEFIBRILLATOR', 'kit': 'assault'},
    'M320': {'type': None, 'name': 'M320', 'kit': 'assault'},
    'M26Mass': {'type': 'shotgun', 'name': 'M26 MASS', 'kit': 'assault'},

    # engineer
    'Weapons/A91/A91': {'type': 'carbines', 'name': 'A-91', 'kit': 'engineer'},
    'Weapons/XP2_ACR/ACR': {'type': 'carbines', 'name': 'ACW-R', 'kit': 'engineer'},
    'AKS-74u': {'type': 'carbines', 'name': 'AKS-74', 'kit': 'engineer'},
    'Weapons/G36C/G36C': {'type': 'carbines', 'name': 'G36C', 'kit': 'engineer'},
    'HK53': {'type': 'carbines', 'name': 'G53', 'kit': 'engineer'},
    'M4A1': {'type': 'carbines', 'name': 'M4A1', 'kit': 'engineer'},
    'Weapons/XP2_MTAR/MTAR': {'type': 'carbines', 'name': 'MTAR-21', 'kit': 'engineer'},
    'QBZ-95': {'type': 'carbines', 'name': 'QBZ-95B', 'kit': 'engineer'},
    'Weapons/SCAR-H/SCAR-H': {'type': 'carbines', 'name': 'SCAR-H', 'kit': 'engineer'},
    'SG 553 LB': {'type': 'carbines', 'name': 'SG553', 'kit': 'engineer'},

    'FIM92': {'type': 'launcher', 'name': 'FIM-92 STINGER', 'kit': 'engineer'},
    'Weapons/Sa18IGLA/Sa18IGLA': {'type': 'launcher', 'name': 'SA-18 IGLA', 'kit': 'engineer'},
    'FGM-148': {'type': 'launcher', 'name': 'FGM-148 JAVELIN', 'kit': 'engineer'},
    'RPG-7': {'type': 'launcher', 'name': 'RPG-7V2', 'kit': 'engineer'},
    'SMAW': {'type': 'launcher', 'name': 'SMAW', 'kit': 'engineer'},

    'Repair Tool': {'type': '', 'name': 'REPAIR TOOL', 'kit': 'engineer'},
    'M15 AT Mine': {'type': 'explosive', 'name': 'M15 AT MINE', 'kit': 'engineer'},
    'EOD BOT': {'type': '', 'name': 'EOD BOT', 'kit': 'engineer'},

    # supporter
    'Weapons/XP2_L86/L86': {'type': 'LMG', 'name': 'L86A2', 'kit': 'support'},
    'LSAT': {'type': 'LMG', 'name': 'LSAT', 'kit': 'support'},
    'M240': {'type': 'LMG', 'name': 'M240B', 'kit': 'support'},
    'M249': {'type': 'LMG', 'name': 'M249', 'kit': 'support'},
    'M27IAR': {'type': 'LMG', 'name': 'M27 IAR', 'kit': 'support'},
    'M60': {'type': 'LMG', 'name': 'M60E4', 'kit': 'support'},
    'MG36': {'type': 'LMG', 'name': 'MG36', 'kit': 'support'},
    'Pecheneg': {'type': 'LMG', 'name': 'PKP PECHENEG', 'kit': 'support'},
    'QBB-95': {'type': 'LMG', 'name': 'QBB-95', 'kit': 'support'},
    'RPK-74M': {'type': 'LMG', 'name': 'RPK-74M', 'kit': 'support'},
    'Type88': {'type': 'LMG', 'name': 'TYPE 88 LMG', 'kit': 'support'},

    'Weapons/Gadgets/C4/C4': {'type': 'explosive', 'name': 'C4 EXPLOSIVES', 'kit': 'support'},
    'Weapons/Gadgets/Claymore/Claymore': {'type': 'explosive', 'name': 'M18 CLAYMORE', 'kit': 'support'},

    # sniper
    'M417': {'type': 'sniper rifle', 'name': 'M417', 'kit': 'recon'},
    'JNG90': {'type': 'sniper rifle', 'name': 'JNG-90', 'kit': 'recon'},
    'L96': {'type': 'sniper rifle', 'name': 'L96', 'kit': 'recon'},
    'M39': {'type': 'sniper rifle', 'name': 'M39 EMR', 'kit': 'recon'},
    'M40A5': {'type': 'sniper rifle', 'name': 'M40A5', 'kit': 'recon'},
    'Model98B': {'type': 'sniper rifle', 'name': 'M98B', 'kit': 'recon'},
    'Mk11': {'type': 'sniper rifle', 'name': 'MK11 MOD 0', 'kit': 'recon'},
    'QBU-88': {'type': 'sniper rifle', 'name': 'QBU-88', 'kit': 'recon'},
    'SKS': {'type': 'sniper rifle', 'name': 'SKS', 'kit': 'recon'},
    'SV98': {'type': 'sniper rifle', 'name': 'SV98', 'kit': 'recon'},
    'SVD': {'type': 'sniper rifle', 'name': 'SVD', 'kit': 'recon'},
    'MAV': {'type': None, 'name': 'MAV', 'kit': 'recon'},

    # general
    '870MCS': {'type': 'shotgun', 'name': '870MCS', 'kit': 'general'},
    'DAO-12': {'type': 'shotgun', 'name': 'DAO-12', 'kit': 'general'},
    'jackhammer': {'type': 'shotgun', 'name': 'MK3A1', 'kit': 'general'},
    'M1014': {'type': 'shotgun', 'name': 'M1014', 'kit': 'general'},
    'SPAS-12': {'type': 'shotgun', 'name': 'SPAS-12', 'kit': 'general'},
    'Siaga20k': {'type': 'shotgun', 'name': 'SAIGA 12K', 'kit': 'general'},
    'USAS-12': {'type': 'shotgun', 'name': 'USAS-12', 'kit': 'general'},


    # general smg
    'Weapons/XP2_MP5K/MP5K': {'type': 'smg', 'name': 'M5K', 'kit': 'general'},
    'MP7': {'type': 'smg', 'name': 'MP7', 'kit': 'general'},
    'Weapons/P90/P90': {'type': 'smg', 'name': 'P90', 'kit': 'general'},
    'Weapons/MagpulPDR/MagpulPDR': {'type': 'smg', 'name': 'PDW-R', 'kit': 'general'},
    'PP-19': {'type': 'smg', 'name': 'PP-19', 'kit': 'general'},
    'PP-2000': {'type': 'smg', 'name': 'PP-2000', 'kit': 'general'},
    'Weapons/UMP45/UMP45': {'type': 'smg', 'name': 'UMP-45', 'kit': 'general'},
    'AS Val': {'type': 'smg', 'name': 'AS VAL', 'kit': 'general'},

    'M67': {'type': None, 'name': 'M67 GRENADE', 'kit': 'general'},
    # knifekill with animation
    'Knife_RazorBlade': {'type': 'all', 'name': 'ACB-90', 'kit': 'general'},
    # knifekill normal
    'Melee': {'type': 'all', 'name': 'ACB-90', 'kit': 'general'},
    'Weapons/Knife/Knife': {'type': 'all', 'name': 'ACB-90', 'kit': 'general'},
    'CrossBow': {'type': 'handgun', 'name': 'XBOW', 'kit': 'general'},

    # Pistols
    'M1911': {'type': 'handgun', 'name': 'M1911', 'kit': 'general'},
    'Weapons/MP412Rex/MP412REX': {'type': 'handgun', 'name': 'MP412 REX', 'kit': 'general'},
    'M9': {'type': 'handgun', 'name': 'M9', 'kit': 'general'},
    'M93R': {'type': 'handgun', 'name': '93R', 'kit': 'general'},
    'Weapons/MP443/MP443': {'type': 'handgun', 'name': 'MP443', 'kit': 'general'},
    'MP443SUPP': {'type': 'handgun', 'name': 'MP443 SUPP.', 'kit': 'general'},
    'Taurus .44': {'type': 'handgun', 'name': '.44 MAGNUM', 'kit': 'general'},
    'Glock18': {'type': 'handgun', 'name': 'G18', 'kit': 'general'},

    # others
    'Death': {'type': '', 'name': 'Death', 'kit': ''},
    'SoldierCollision': {'type': '', 'name': 'SoldierCollision', 'kit': ''},
    'RoadKill': {'type': '', 'name': 'RoadKill', 'kit': ''},
    'DamageArea': {'type': '', 'name': 'DamageArea', 'kit': ''},
    'Suicide': {'type': '', 'name': 'Suicide', 'kit': ''},

    # gunmaster weapons
    'Weapons/MP443/MP443_GM': {'type': 'handgun', 'name': 'MP443 (Gunmster mode)', 'kit': 'general'},
    'Weapons/P90/P90_GM': {'type': 'smg', 'name': 'P90 (Gunmaster Mode)', 'kit': 'general'},
}

WEAPONS_GROUPS = {
    'shotguns': ('870MCS', 'DAO-12', 'jackhammer', 'M1014', 'SPAS-12', 'Siaga20k', 'USAS-12', 'M26Mass'),
    'explosives': ('Weapons/Gadgets/Claymore/Claymore', 'M15 AT Mine', 'Weapons/Gadgets/C4/C4'),
    }
