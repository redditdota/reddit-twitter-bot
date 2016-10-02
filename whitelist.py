import re
from collections import OrderedDict

_TEMPLATE = r"(?<!\@)(\b|[a-zA-Z]+\.)%s\b"
REVERSE = re.compile(r"\(.*\.\)(.+)\\b")

PLAYERS_TO_HANDLE = OrderedDict([

    # EU
    (r'Chessie', 'ChessieDota'),
    (r'Limmp', 'LimmpDota'),
    (r'Handsken', 'Handsken1'),
    (r'Pajkatt', 'PajkattDota'),
    (r'Xcalibur', 'XcaliburYe'),
    ## Alliance
    (r'Loda', 'LodaBerg'),
    (r'EGM', 'followEGM'),
    (r'EnterGodMode', 'followEGM'),
    # Escape Gaming
    (r'Era', 'eradota'),
    (r'qojqva', 'Qojqva1'),
    (r'KheZu', 'KheZzu_'),
    (r'KheZzu', 'KheZzu_'),
    (r'YapzOr', 'YapzOrdota'),
    (r'syndereN', 'syndereNdota'),
    ## Kaipi
    (r'BOne7', 'bOne7dota'),
    (r'SingSing', 'Sing2X'),
    (r'SexyBamboe', 'SexyBamboe'),
    (r'Bamboe', 'SexyBamboe'),
    ## OG
    (r'n0tail', 'OG_BDN0tail'),
    (r'BDN', 'OG_BDN0tail'),
    (r'BigDaddyN0tail', 'OG_BDN0tail'),
    (r'BigDaddy', 'OG_BDN0tail'),
    (r's4', 's4dota'),
    (r'JerAx', 'liquidjerax'),
    (r'Fly', 'Fly_dota2'),
    ## Team Liquid
    (r'MATUMBAMAN', 'LiquidMatumba'),
    (r'Miracle-', 'Miracle_Dota2'),
    (r'Miracle', 'Miracle_Dota2'),
    (r'MinD_ContRoL', 'LiquidMinD_ctrL'),
    (r'MinD ContRoL', 'LiquidMinD_ctrL'),
    (r'MinDContRoL', 'LiquidMinD_ctrL'),
    (r'BuLba', 'BuLbaDotA'),
    (r'Kuro', 'liquidkuroky'),
    (r'KuroKy', 'liquidkuroky'),
    ## Team Secret
    (r'MidOne', 'midonedota2'),
    (r'Miduan', 'midonedota2'),
    #(r'FoREV', 'Forev_Lee'),
    (r'Puppey', 'clementinator'),
    (r'ppy', 'clementinator'),
    (r'pieliedie', 'PieLieDieDota'),
    (r'pld', 'PieLieDieDota'),
    ## Ex-Secret
    (r'Arteezy', 'arteezy'),
    (r'rtz', 'arteezy'),
    (r'artour', 'arteezy'),
    (r'EternaLEnVy', 'eternalenvy1991'),
    (r'EE', 'eternalenvy1991'),
    (r'Envy', 'eternalenvy1991'),
    (r'1437', '1437x'),
    (r'Theeban', '1437x'),
    (r'Aui_2000', 'Aui_2000'),
    (r'Aui', 'Aui_2000'),

    # East
    (r'Hao', 'chantseho'),
    (r'Mu', 'NewbeeMU'),
    (r'Kphoenii', 'kpiidota'),
    (r'Kpii', 'kpiidota'),
    (r'ChuaN', 'iGChuaN'),
    (r'XtiNcT', 'XtinctDota'),
    (r'WinteR', 'WinteRDota'),
    (r'DJ', 'DjardelJicko'),
    (r'QO', 'qodota'),
    (r'Febby', 'Febbydota'),
    ## Team Faceless
    (r'Black^', 'BlackDotA2'),
    (r'Black', 'BlackDotA2'),
    (r'iceiceice', 'iceiceicedota'),
    (r'icex3', 'iceiceicedota'),
    (r'NutZ', 'NutZdoto'),
    ## Fnatic
    (r'Mushi', 'Mushi_Chai'),
    (r'Ohaiyo', 'Titan_Ohaiyo'),

    # Free Agents
    (r'Fogged', 'FoggedDota'),
    (r'FATA-', 'liquidfata'),
    (r'FATA', 'liquidfata'),
    (r'AdmiralBulldog', 'AdmiralBulldog'),
    (r'Bulldog', 'AdmiralBulldog'),
    (r'Bulldong', 'AdmiralBulldog'),
    (r'Donger', 'AdmiralBulldog'),
    (r'Dongerino', 'AdmiralBulldog'),
    (r'Dong', 'AdmiralBulldog'),
    (r'Akke', 'FollowAkke'),
    (r'Fear', 'FearDotA'),
    (r'FearDarkness', 'FearDotA'),

    # NA Dota
    (r'SVG', 'SVGDota'),
    (r'ixmike88', 'ixmike88'),
    (r'ixmike', 'ixmike88'),
    (r'FLUFFNSTUFF', 'FLUFFDota'),
    (r'FLUFF', 'FLUFFDota'),
    (r'Stan King', 'StanKingDota'),
    (r'StanKing', 'StanKingDota'),
    (r'PatSoul', 'PatSoulDota2'),
    (r'Brax', 'braxlikesdota'),
    (r'CC&C', 'CCnCDotA2'),
    (r'CCnC', 'CCnCDotA2'),
    (r'CCC', 'CCnCDotA2'),
    (r'Demon', 'dotademon'),
    (r'Mason', 'masondota'),
    (r'Moo', 'moodota2'),
    (r'MSS', 'MSSDota'),
    (r'Jeyo', 'Jeyostyle'),
    (r'Ritsu', 'ritsudota'),
    (r'TC', 'TCDota'),
    (r'Cr1t-', 'Cr1tdota'),
    (r'Cr1t', 'Cr1tdota'),
    (r'USH', 'ushdota'),
    (r'zai', 'zai_2002'),
    ## col
    (r'swindlezz', 'swindlezz'),
    (r'swindle', 'swindlezz'),
    (r'swindlemelonzz', 'swindlezz'),
    (r'melonzz', 'swindlezz'),
    (r'melon', 'swindlezz'),
    (r'Zfreek', 'coL_zfreek'),
    ## Digital Chaos
    (r'Resolut1on', 'Resolut1on_'),
    (r'w33', 'w33haa'),
    (r'w33haa', 'w33haa'),
    (r'MoonMeander', 'MoonMeanderated'),
    (r'Moon', 'MoonMeanderated'),
    (r'Saksa', 'Saksadota'),
    (r'MiSeRy', 'MiSeRyDOTA'),
    (r'moosery', 'MiSeRyDOTA'),
    (r'MiSeRyTheSLAYER', 'MiSeRyDOTA'),
    # Evil Geniuses
    (r'SumaiL', 'SumaaaaiL'),
    (r'UNiVeRsE', 'UniverseDota'),
    (r'ppd', 'Peterpandam'),
    (r'peter', 'Peterpandam'),

    # CIS
    (r'UnderShock', 'undershock17'),
    (r'Miposhka', 'miposhka'),
    (r'KingR', 'R1nater'),
    (r'Illidan', 'IllidanSTRdoto'),
    (r'Illidan', 'IllidanSTRdoto'),
    (r'Silent', 'Silentdota2'),
    (r'Iceberg', 'Icebergdota'),
    (r'DkPhobos', 'DkPhobos'),
    (r'Phobos', 'DkPhobos'),
    (r'Lil', 'LilJke'),
    (r'ALWAYSWANNAFLY', 'flydota'),
    (r'goddam', 'goddamDOTA'),
    (r'goddam', 'goddamDOTA'),
    (r'ALOHADANCE', 'alohad4nce'),
    #(r'G', 'GTHEMALL'),
    #(r'God', 'GTHEMALL'),
    (r'yoky-', 'yokydota'),
    (r'yoky', 'yokydota'),
    (r'fng', 'fnggshka'),
    (r'XBOCT', 'JustXBOCT'),
    (r'Hvost', 'JustXBOCT'),
    (r'Funn1k', 'Funn1kDota'),
    (r'Funnik', 'Funn1kDota'),
    (r'Goblak', 'arturfisura666'),
    (r'Goblak', 'arturfisura666'),
    (r'Noone', 'nooneboss'),
    (r'No[o]ne', 'nooneboss'),
    (r'Mag', 'FollowMag_'),
    (r'Mag~', 'FollowMag_'),
    #(r'Solo', 'dotaSolo'),
    (r'Scandal', 'scandalisback'),
    ## Na'Vi
    (r'Ditya Ra', 'Ditya_Ra_'),
    (r'DityaRa', 'Ditya_Ra_'),
    (r'Ditya', 'Ditya_Ra_'),
    (r'Dendi', 'DendiBoss'),
    (r'SoNNeikO', 'sonneiko_o'),
    (r'Artstyle', 'ArtStylee'),

])

PLAYERS = map(lambda name: re.compile(_TEMPLATE % name) if len(name) < 2 else re.compile(_TEMPLATE % name, flags=re.IGNORECASE), PLAYERS_TO_HANDLE.keys())

PERSONALITIES_TO_HANDLE = OrderedDict([
    (r'2GD', 'follow2GD'),
    (r'Ayesee', 'ayesee'),
    (r'Blitz', 'Blitz_DotA'),
    (r'Bruno', 'StatsmanBruno'),
    (r'Cap', 'DotaCapitalist'),
    (r'Capitalist', 'DotaCapitalist'),
    (r'Charlie Yang', 'CharlieYang'),
    (r'Charlie', 'CharlieYang'),
    (r'CharlieYang', 'CharlieYang'),
    (r'Cyborgmatt', 'Cyborgmatt'),
    (r'diredude', 'diredude'),
    (r'dotabuff', 'dotabuff'),
    (r'Draskyl', 'Draskyl'),
    (r'esex', 'esportsexpress'),
    (r'esportsexpress', 'esportsexpress'),
    (r'GoDz', 'BTSGoDz'),
    (r'Hot_bid', 'Hot_Bid'),
    (r'Hotbid', 'Hot_Bid'),
    (r'KotLGuy', 'KotLguy'),
    (r'LD', 'LDdota'),
    (r'Leafeator', 'Leafeator'),
    (r'Lumi', 'LuminousInverse'),
    (r'Luminous', 'LuminousInverse'),
    (r'LuminousInverse', 'LuminousInverse'),
    (r'Maelk', 'TheMaelk'),
    (r'Maut', 'MautDota'),
    (r'Merlini', 'MerliniDota'),
    (r'Monolith', 'CharlieYang'),
    (r'Nahaz', 'NahazDota'),
    (r'NoobFromUA', 'NoobFromUA'),
    (r'Noxville', 'NoxvilleZA'),
    (r'ODPixel', 'ODPixel'),
    (r'Purge', 'PurgeGamers'),
    (r'Sheever', 'sheevergaming'),
    (r'SirActionSlacks', 'SirActionSlacks'),
    (r'Slacks', 'SirActionSlacks'),
    (r'SUNSfan', 'SUNSfanTV'),
    (r'Tobi Wan', 'TobiWanDOTA'),
    (r'Tobi', 'TobiWanDOTA'),
    (r'TobiWan', 'TobiWanDOTA'),
    (r'tsunami', 'tsunami643'),
    (r'Wyk', 'wykrhm'),
    (r'wykrhm', 'wykrhm'),
    (r'Zyori', 'ZyoriTV'),
])

PERSONALITIES = map(lambda name: re.compile(_TEMPLATE % name) if len(name) < 2 else re.compile(_TEMPLATE % name, flags=re.IGNORECASE), PERSONALITIES_TO_HANDLE.keys())

ORGS_TO_HANDLE = OrderedDict([
    # West
    (r'Alliance', 'theAllianceGG'),
    (r'[A]lliance', 'theAllianceGG'),
    (r'The Alliance', 'theAllianceGG'),
    (r'compLexity Gaming',  'compLexityLive'),
    (r'compLexity',  'compLexityLive'),
    (r'col',  'compLexityLive'),
    (r'Digital Chaos', 'DigitalChaosGG'),
    (r'DC', 'DigitalChaosGG'),
    (r'Escape Gaming', 'TheEscapeGaming'),
    (r'Escape', 'TheEscapeGaming'),
    (r'Evil Geniuses', 'EvilGeniuses'),
    (r'EG', 'EvilGeniuses'),
    (r'FDL', 'fdldota'),
    (r'Friendship, Dedication, Love', 'fdldota'),
    (r'Kaipi', 'KaipiDota'),
    (r'Natus Vincere', 'NatusVincere'),
    (r'NaVi', 'NatusVincere'),
    (r'Na Vi', 'NatusVincere'),
    (r'Na\'Vi', 'NatusVincere'),
    (r'(Team )?NP', 'NPDotA'),
    (r'OG', 'OGDota2'),
    (r'Polarity', 'PolarityDota2'),
    (r'(Team )?Empire', 'Team_Empire'),
    (r'(Team )?Liquid', 'teamliquidpro'),
    (r'TL', 'teamliquidpro'),
    (r'(Team )?Secret', 'teamsecret'),
    (r'Team Spirit', 'Team__Spirit'),
    (r'Twitch', 'Twitch'),
    (r'Vega Squadron', 'VegaSquadron'),
    (r'Vega', 'VegaSquadron'),
    (r'Vegetables Esports Club', 'VeggieEsports'),
    (r'Veggies Esports', 'VeggieEsports'),
    (r'VeggiesEsports', 'VeggieEsports'),
    (r'Veggies', 'VeggieEsports'),
    (r'VEC', 'VeggieEsports'),
    (r'Virtus.Pro', 'TeamVirtuspro'),
    (r'Virtus Pro', 'TeamVirtuspro'),
    (r'VirtusPro', 'TeamVirtuspro'),
    (r'VP', 'TeamVirtuspro'),
    # East
    (r'LGD Gaming', 'LGDgaming'),
    (r'LGD', 'LGDgaming'),
    (r'HyperGloryTeam', 'HGT_Team'),
    (r'HGT', 'HGT_Team'),
    (r'Vici Gaming', 'vici_gaming'),
    (r'Vici Gaming Reborn', 'vici_gaming'),
    (r'Vici', 'vici_gaming'),
    (r'VG.Reborn', 'vici_gaming'),
    (r'VG.R', 'vici_gaming'),
    (r'VG', 'vici_gaming'),
    (r'EHOME', 'EHOMECN'),
    (r'Invictus Gaming', 'invgaming'),
    (r'IG', 'invgaming'),
    (r'Newbee', 'NewbeeCN'),
    (r'NB', 'NewbeeCN'),
    (r'Mineski', 'Mineski'),
    (r'Fnatic', 'FNATIC'),
    (r'MVP Phoenix', 'MVP_GG'),
    (r'MVP', 'MVP'),
    (r'Wings Gaming', 'wingsgamingcn'),
    (r'Wings', 'wingsgamingcn'),
    (r'TNC Gaming', 'tncproteam'),
    (r'TNC Pro Team', 'tncproteam'),
    (r'TNC Pro', 'tncproteam'),
    (r'TNC', 'tncproteam'),
    (r'Execration', 'ExecrationGG'),
    (r'XctN', 'ExecrationGG'),
    # Studios
    (r'BeyondTheSummit', 'beyondthesummit'),
    (r'BTS', 'beyondthesummit'),
    (r'joinDOTA', 'joinDOTA'),
    (r'jD', 'joinDOTA'),
    (r'moonduckTV', 'moonduckTV'),
    (r'moonduck', 'moonduckTV'),
])

ORGS = map(lambda name: re.compile(_TEMPLATE % name) if len(name) < 2 else re.compile(_TEMPLATE % name, flags=re.IGNORECASE), ORGS_TO_HANDLE.keys())
