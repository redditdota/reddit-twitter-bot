import re

_TEMPLATE = r"(?<!\@)(\b|[a-zA-Z]+\.)%s\b"
REVERSE = re.compile(r"\(.*\)(.+)\\b")

PLAYERS_TO_HANDLE = {
    # Alliance
    r'Loda' : 'LodaBerg',
    r's4' : 's4dota',
    r'AdmiralBulldog' : 'AdmiralBulldog',
    r'Bulldog' : 'AdmiralBulldog',
    r'Bulldong' : 'AdmiralBulldog',
    r'Donger' : 'AdmiralBulldog',
    r'Dongerino' : 'AdmiralBulldog',
    r'Dong' : 'AdmiralBulldog',
    r'Akke' : 'FollowAkke',
    r'EGM' : 'followEGM',
    r'EnterGodMode' : 'followEGM',
    # coL
    r'Chessie' : 'ChessieDota',
    r'Limmp' : 'LimmpDota',
    r'swindlezz' : 'swindlezz',
    r'swindle' : 'swindlezz',
    r'swindlemelonzz' : 'swindlezz',
    r'melonzz' : 'swindlezz',
    r'melon' : 'swindlezz',
    r'Zfreek' : 'coL_zfreek',
    r'Handsken' : 'Handsken1',
    # Digital Chaos
    r'Resolut1on' : 'Resolut1on_',
    r'w33' : 'w33haa',
    r'w33haa' : 'w33haa',
    r'Moo' : 'moodota2',
    r'Saksa' : 'Saksadota',
    r'MiSeRy' : 'MiSeRyDOTA',
    r'moosery' : 'MiSeRyDOTA',
    r'MiSeRyTheSLAYER' : 'MiSeRyDOTA',
    r'USH' : 'ushdota',
    # Escape Gaming
    r'Era' : 'eradota',
    r'qojqva' : 'Qojqva1',
    r'KheZu' : 'KheZzu_',
    r'KheZzu' : 'KheZzu_',
    r'YapzOr' : 'YapzOrdota',
    r'syndereN' : 'syndereNdota',
    # Evil Geniuses
    r'Fear' : 'FearDotA',
    r'FearDarkness' : 'FearDotA',
    r'SumaiL' : 'SumaaaaiL',
    r'UNiVeRsE' : 'UniverseDota',
    r'zai' : 'zai_2002',
    r'ppd' : 'Peterpandam',
    r'peter' : 'Peterpandam',
    # Kaipi
    r'BOne7' : 'bOne7dota',
    r'SingSing': 'Sing2X',
    r'SexyBamboe' : 'SexyBamboe',
    r'Bamboe' : 'SexyBamboe',
    # Na'Vi
    r'Ditya Ra' : 'Ditya_Ra_',
    r'DityaRa' : 'Ditya_Ra_',
    r'Ditya' : 'Ditya_Ra_',
    r'Dendi' : 'DendiBoss',
    r'SoNNeikO' : 'sonneiko_o',
    r'Artstyle' : 'ArtStylee',
    # OG
    r'n0tail' : 'OG_BDN0tail',
    r'BDN' : 'OG_BDN0tail',
    r'BigDaddyN0tail' : 'OG_BDN0tail',
    r'BigDaddy' : 'OG_BDN0tail',
    r'Miracle-' : 'Miracle_Dota2',
    r'Miracle' : 'Miracle_Dota2',
    r'MoonMeander' : 'MoonMeanderated',
    r'Moon' : 'MoonMeanderated',
    r'Cr1t-' : 'Cr1tdota',
    r'Cr1t' : 'Cr1tdota',
    r'Fly' : 'Fly_dota2',
    # Polarity
    r'Silent' : 'Silentdota2',
    r'Iceberg' : 'Icebergdota',
    r'DkPhobos' : 'DkPhobos',
    r'Phobos' : 'DkPhobos',
    r'Lil' : 'LilJke',
    r'ALWAYSWANNAFLY' : 'flydota',
    # Team Empire
    r'Miposhka' : 'miposhka',
    # Team Liquid
    r'MATUMBAMAN' : 'LiquidMatumba',
    r'FATA-' : 'liquidfata',
    r'FATA' : 'liquidfata',
    r'MinD_ContRoL' : 'LiquidMinD_ctrL',
    r'MinD ContRoL' : 'LiquidMinD_ctrL',
    r'MinDContRoL' : 'LiquidMinD_ctrL',
    r'JerAx' : 'liquidjerax',
    r'Kuro' : 'liquidkuroky',
    r'KuroKy' : 'liquidkuroky',
    # Team Secret
    r'Arteezy' : 'arteezy',
    r'rtz' : 'arteezy',
    r'artour' : 'arteezy',
    r'EternaLEnVy' : 'eternalenvy1991',
    r'EE' : 'eternalenvy1991',
    r'Envy': 'eternalenvy1991',
    r'BuLba' : 'BuLbaDotA',
    r'Puppey' : 'clementinator',
    r'ppy' : 'clementinator',
    r'pieliedie' : 'PieLieDieDota',
    r'pld' : 'PieLieDieDota',
    r'1437' : '1437x',
    r'Theeban' : '1437x',
    r'Aui_2000' : 'Aui_2000',
    r'Aui' : 'Aui_2000',
    # Team Spirit
    r'XBOCT' : 'JustXBOCT',
    r'Hvost' : 'JustXBOCT',
    r'Funn1k' : 'Funn1kDota',
    r'Funnik' : 'Funn1kDota',
    r'Goblak' : 'arturfisura666',
    r'Goblak' : 'arturfisura666',
    # Vega Squadron
    r'Noone' : 'nooneboss',
    r'No[o]ne' : 'nooneboss',
    r'Mag' : 'FollowMag_',
    r'Mag~' : 'FollowMag_',
    r'Solo' : 'dotaSolo',
    # Virtus Pro
    r'ALOHADANCE' : 'alohad4nce',
    r'G' : 'GTHEMALL',
    r'God' : 'GTHEMALL',
    r'yoky-' : 'yokydota',
    r'yoky' : 'yokydota',
    r'fng' : 'fnggshka',

    # East
    r'iceiceice' : 'iceiceicedota',
    r'icex3' : 'iceiceicedota',
    r'Hao' : 'chantseho',
    r'Mu' : 'NewbeeMU',
    r'Kphoenii' : 'kpiidota',
    r'Kpii' : 'kpiidota',
    r'ChuaN' : 'iGChuaN',
    r'XtiNcT' : 'XtinctDota',
    r'WinteR' : 'WinteRDota',
    r'Mushi' : 'Mushi_Chai',
    r'Miduan' : 'midonedota2',
    r'Ohaiyo' : 'Titan_Ohaiyo',
    r'DJ' : 'DjardelJicko',
    r'QO' : 'qodota',
    r'FoREV' : 'Forev_Lee',
    r'Febby' : 'Febbydota',
    r'Demon' : 'dotademon',

    # Free
    r'Black^' : 'BlackDotA2',
    r'Black' : 'BlackDotA2',
    r'Fogged' : 'FoggedDota',
}

PLAYERS = map(lambda name : re.compile(_TEMPLATE % name) if len(name) > 2 else re.compile(_TEMPLATE % name, re.IGNORECASE), PLAYERS_TO_HANDLE.keys())

PERSONALITIES_TO_HANDLE = {
    r'SirActionSlacks' : 'SirActionSlacks',
    r'Slacks' : 'SirActionSlacks',
    r'Merlini' : 'MerliniDota',
    r'Blitz' : 'Blitz_DotA',
    r'Capitalist' : 'DotaCapitalist',
    r'Cap' : 'DotaCapitalist',
    r'Monolith' : 'CharlieYang',
    r'Charlie Yang' : 'CharlieYang',
    r'CharlieYang' : 'CharlieYang',
    r'Charlie' : 'CharlieYang',
    r'Maelk' : 'TheMaelk',
    r'Purge' : 'PurgeGamers',
    r'LD' : 'LDdota',
    r'2GD' : 'follow2GD',
    r'Ayesee' : 'ayesee',
    r'Bruno' : 'StatsmanBruno',
    r'Draskyl' : 'Draskyl',
    r'GoDz' : 'BTSGoDz',
    r'KotLGuy' : 'KotLguy',
    r'LuminousInverse' : 'LuminousInverse',
    r'Luminous' : 'LuminousInverse',
    r'Lumi' : 'LuminousInverse',
    r'Maut' : 'MautDota',
    r'Nahaz' : 'NahazDota',
    r'Noxville' : 'NoxvilleZA',
    r'ODPixel' : 'ODPixel',
    r'Sheever' : 'sheevergaming',
    r'SUNSfan' : 'SUNSfanTV',
    r'Tobi Wan' : 'TobiWanDOTA',
    r'TobiWan' : 'TobiWanDOTA',
    r'Tobi' : 'TobiWanDOTA',
    r'Zyori': 'ZyoriTV',
    r'Wyk': 'wykrhm',
    r'wykrhm' : 'wykrhm',
}

PERSONALITIES = map(lambda name : re.compile(_TEMPLATE % name) if len(name) > 2 else re.compile(_TEMPLATE % name, re.IGNORECASE), PERSONALITIES_TO_HANDLE.keys())

ORGS_TO_HANDLE = {
    # West
    r'Alliance' : 'theAllianceGG',
    r'[A]lliance' : 'theAllianceGG',
    r'The Alliance' : 'theAllianceGG',
    r'compLexity Gaming' :  'compLexityLive',
    r'compLexity' :  'compLexityLive',
    r'col' :  'compLexityLive',
    r'Digital Chaos' : 'DigitalChaosGG',
    r'DC' : 'DigitalChaosGG',
    r'Escape Gaming' : 'TheEscapeGaming',
    r'Escape' : 'TheEscapeGaming',
    r'Evil Geniuses' : 'EvilGeniuses',
    r'EG' : 'EvilGeniuses',
    r'Kaipi' : 'KaipiDota',
    r'Natus Vincere' : 'NatusVincere',
    r'NaVi' : 'NatusVincere',
    r'Na Vi' : 'NatusVincere',
    r'Na\'Vi' : 'NatusVincere',
    r'OG' : 'OGDota2',
    r'Polarity' : 'PolarityDota2',
    r'(Team )?Empire' : 'Team_Empire',
    r'(Team )?Liquid' : 'teamliquidpro',
    r'TL' : 'teamliquidpro',
    r'(Team )?Secret' : 'teamsecret',
    r'Team Spirit' : 'Team__Spirit',
    r'Vega Squadron' : 'VegaSquadron',
    r'Vega' : 'VegaSquadron',
    r'Vegetables Esports Club' : 'VeggieEsports',
    r'Veggies Esports' : 'VeggieEsports',
    r'VeggiesEsports' : 'VeggieEsports',
    r'Veggies' : 'VeggieEsports',
    r'VEC' : 'VeggieEsports',
    r'Virtus.Pro' : 'TeamVirtuspro',
    r'Virtus Pro' : 'TeamVirtuspro',
    r'VirtusPro' : 'TeamVirtuspro',
    r'VP' : 'TeamVirtuspro',
    # East
    r'LGD Gaming' : 'LGDgaming',
    r'LGD' : 'LGDgaming',
    r'HyperGloryTeam' : 'HGT_Team',
    r'HGT' : 'HGT_Team',
    r'Vici Gaming' : 'vici_gaming',
    r'Vici Gaming Reborn' : 'vici_gaming',
    r'Vici' : 'vici_gaming',
    r'VG.Reborn' : 'vici_gaming',
    r'VG.R' : 'vici_gaming',
    r'VG' : 'vici_gaming',
    r'EHOME' : 'EHOMECN',
    r'Invictus Gaming' : 'invgaming',
    r'IG' : 'invgaming',
    r'Newbee' : 'NewbeeCN',
    r'NB' : 'NewbeeCN',
    r'Mineski' : 'Mineski',
    r'Fnatic' : 'FNATIC',
    r'MVP Phoenix' : 'MVP_GG',
    r'MVP' : 'MVP',
    r'Wings Gaming' : 'wingsgamingcn',
    r'Wings' : 'wingsgamingcn',
    r'TNC Gaming' : 'tncproteam',
    r'TNC Pro Team' : 'tncproteam',
    r'TNC Pro' : 'tncproteam',
    r'TNC' : 'tncproteam',
    r'Execration' : 'ExecrationGG',
    r'XctN' : 'ExecrationGG',
    # Studios
    r'BeyondTheSummit' : 'beyondthesummit',
    r'BTS': 'beyondthesummit',
    r'joinDOTA': 'joinDOTA',
    r'jD' : 'joinDOTA',
    r'moonduckTV' : 'moonduckTV',
    r'moonduck' : 'moonduckTV',
}

ORGS = map(lambda name : re.compile(_TEMPLATE % name) if len(name) > 2 else re.compile(_TEMPLATE % name, re.IGNORECASE), ORGS_TO_HANDLE.keys())
