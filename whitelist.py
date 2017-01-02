import re
from collections import OrderedDict

_TEMPLATE = r"(?<!\@)(\b|[a-zA-Z]+\.)%s\b"
REVERSE = re.compile(r"\(.*\.\)(.+)\\b")

PLAYERS_TO_HANDLE = OrderedDict([

    # EU
    (r'Pajkatt', 'PajkattDota'),
    (r'Xcalibur', 'XcaliburYe'),
    ## Ad Finem
    (r'Madara', 'madaradota2'),
    (r'ThuG', 'ThuGdota2'),
    (r'SkyLark', 'skylarkXZ'),
    (r'Maybe Next Time', 'mntdota2'),
    (r'mnt', 'mntdota2'),
    (r'SsaSpartan', 'ssaspartan'),
    ## Alliance
    (r'Loda', 'LodaBerg'),
    (r'Limmp', 'LimmpDota'),
    (r'Jonassomfan', 'jonassomfan'),
    (r'EGM', 'followEGM'),
    (r'EnterGodMode', 'followEGM'),
    (r'Handsken', 'Handsken1'),
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
    (r'TheCoon', '33Dota'),
    (r'33', '33Dota'),
    (r'FLUFFNSTUFF', 'FLUFFDota'),
    (r'FLUFF', 'FLUFFDota'),
    ## OG
    (r'n0tail', 'OG_BDN0tail'),
    (r'BDN', 'OG_BDN0tail'),
    (r'BigDaddyN0tail', 'OG_BDN0tail'),
    (r'BigDaddy', 'OG_BDN0tail'),
    (r'Ana', 'anadota99'),
    (r's4', 's4dota'),
    (r'JerAx', 'iamJERAX'),
    (r'Fly', 'Fly_dota2'),
    ## Team Liquid
    (r'MATUMBAMAN', 'LiquidMatumba'),
    (r'Miracle-', 'Liquid_Miracle'),
    (r'Miracle', 'Liquid_Miracle'),
    (r'MinD_ContRoL', 'LiquidMinD_ctrL'),
    (r'MinD ContRoL', 'LiquidMinD_ctrL'),
    (r'MinDContRoL', 'LiquidMinD_ctrL'),
    (r'Kuro', 'liquidkuroky'),
    (r'KuroKy', 'liquidkuroky'),
    (r'gh', 'LiquidGh_'),
    ## Team Secret
    (r'MidOne', 'midonedota2'),
    (r'Miduan', 'midonedota2'),
    #(r'FoREV', 'Forev_Lee'),
    (r'Puppey', 'clementinator'),
    (r'ppy', 'clementinator'),
    (r'pieliedie', 'PieLieDieDota'),
    (r'pld', 'PieLieDieDota'),

    # East
    (r'Hao', 'chantseho'),
    (r'Mu', 'NewbeeMU'),
    (r'Kphoenii', 'kpiidota'),
    (r'Kpii', 'kpiidota'),
    (r'ChuaN', 'iGChuaN'),
    (r'XtiNcT', 'XtinctDota'),
    (r'WinteR', 'WinteRDota'),
    (r'QO', 'qodota'),
    (r'Febby', 'Febbydota'),
    ## Team Faceless
    (r'Black^', 'BlackDotA2'),
    #(r'Black', 'BlackDotA2'),
    (r'iceiceice', 'iceiceicedota'),
    (r'icex3', 'iceiceicedota'),
    (r'NutZ', 'NutZdoto'),
    (r'Meracle', 'Meracleeeee'),

    ## Execration
    (r'Kim0', 'XctNKim0'),
    (r'DJ', 'DjardelJicko'),
    (r'Abed', 'abedyusop/'),

    ## Fnatic
    (r'Mushi', 'Mushi_Chai'),
    (r'Ohaiyo', 'Titan_Ohaiyo'),
    (r'Demon', 'dotademon'),

    ## Wings
    (r'Faith_bian', 'Faith_bian'),
    (r'Faithbian', 'Faith_bian'),
    (r'Faith bian', 'Faith_bian'),
    (r'innocence', 'y1122Innocence'),
    (r'y`', 'y1122Innocence'),


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
    (r'Justin', 'jkdota'),

    # NA Doto
    (r'ixmike88', 'ixmike88'),
    (r'ixmike', 'ixmike88'),
    (r'Stan King', 'StanKingDota'),
    (r'StanKing', 'StanKingDota'),
    (r'PatSoul', 'PatSoulDota2'),
    (r'Brax', 'braxlikesdota'),
    (r'CC&C', 'CCnCDotA2'),
    (r'CCnC', 'CCnCDotA2'),
    (r'CCC', 'CCnCDotA2'),
    (r'Mason', 'masondota'),
    (r'Jeyo', 'Jeyostyle'),
    (r'Ritsu', 'ritsudota'),
    (r'TC', 'TCDota'),
    (r'Cr1t-', 'Cr1tdota'),
    (r'Cr1t', 'Cr1tdota'),
    (r'USH', 'ushdota'),
    (r'zai', 'zai_2002'),
    ## col
    (r'canceL^^', 'canceldota'),
    (r'canceL', 'canceldota'),
    (r'Moo', 'moodota2'),
    (r'swindlezz', 'melonzzdota'),
    (r'swindle', 'melonzzdota'),
    (r'swindlemelonzz', 'melonzzdota'),
    (r'melonzz', ''),
    (r'melon', 'melonzzdota'),
    (r'Zfreek', 'coL_zfreek'),
    (r'Chessie', 'ChessieDota'),
    (r'monkeys-forever', 'MonkeysDota'),
    (r'monkeysforever', 'MonkeysDota'),
    (r'monkeys-', 'MonkeysDota'),
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
    (r'BuLba', 'BuLbaDotA_'),
    # Evil Geniuses
    (r'Arteezy', 'arteezy'),
    (r'rtz', 'arteezy'),
    (r'artour', 'arteezy'),
    (r'SumaiL', 'SumaaaaiL'),
    (r'UNiVeRsE', 'UniverseDota'),
    (r'ppd', 'Peterpandam'),
    (r'peter', 'Peterpandam'),
    (r'Fear', 'FearDotA'),
    (r'FearDarkness', 'FearDotA'),
    ## NP
    (r'EternaLEnVy', 'eternalenvy1991'),
    (r'EE', 'eternalenvy1991'),
    (r'Envy', 'eternalenvy1991'),
    (r'1437', '1437x'),
    (r'Theeban', '1437x'),
    (r'Aui_2000', 'Aui_2000'),
    (r'Aui', 'Aui_2000'),
    (r'MSS', 'MSSDota'),
    (r'SVG', 'SVGDota'),

    # CIS
    ## Team Empire
    (r'ALOHADANCE', 'alohad4nce'),
    #(r'G', 'GTHEMALL'),
    #(r'God', 'GTHEMALL'),
    (r'Ghostik', 'Ghostikdota'),
    (r'Miposhka', 'miposhka'),
    (r'KingR', 'R1nater'),

    ## Vega
    (r'Iceberg', 'Icebergdota'),
    (r'Mag', 'FollowMag_'),
    (r'Mag~', 'FollowMag_'),
    (r'fng', 'fnggshka'),

    ## Virtus Pro
    (r'RAMZES666', 'ramzesdoto'),
    (r'Ramzes', 'ramzesdoto'),
    (r'SIXSIXSIX', 'ramzesdoto'),
    (r'Noone', 'nooneboss'),
    (r'No[o]ne', 'nooneboss'),
    (r'9pashaebashu', '9pashka'),
    (r'9pasha', '9pashka'),
    (r'Lil', 'LilJke'),
    #(r'Solo', 'dotaSolo'),

    # FRIENDS
    (r'yoky-', 'yokydota'),
    (r'yoky', 'yokydota'),
    (r'UnderShock', 'undershock17'),
    (r'AfterLife', 'afterlifedota2'),
    (r'ALWAYSWANNAFLY', 'flydota'),

    # Fantastic Five
    (r'Illidan', 'IllidanSTRdoto'),
    (r'Illidan', 'IllidanSTRdoto'),
    (r'rmN-', 'rmN_dota'),
    (r'rmN', 'rmN_dota'),

    ## Na'Vi
    (r'Ditya Ra', 'Ditya_Ra_'),
    (r'DityaRa', 'Ditya_Ra_'),
    (r'Ditya', 'Ditya_Ra_'),
    (r'Dendi', 'DendiBoss'),
    (r'SoNNeikO', 'sonneiko_o'),
    (r'Artstyle', 'ArtStylee'),

    # Power Rangers
    (r'Bignum', 'Bignumdota'),
    (r'Afoninje', 'afoninje'),
    (r'chshrct', 'PR_chshrct'),
    (r'goddam', 'goddamDOTA'),
    (r'goddam', 'goddamDOTA'),

    # Teamless
    (r'Silent', 'Silentdota2'),
    (r'DkPhobos', 'DkPhobos'),
    (r'Phobos', 'DkPhobos'),
    (r'XBOCT', 'JustXBOCT'),
    (r'Hvost', 'JustXBOCT'),
    (r'Funn1k', 'Funn1kDota'),
    (r'Funnik', 'Funn1kDota'),
    (r'Goblak', 'arturfisura666'),
    (r'Goblak', 'arturfisura666'),
    (r'Scandal', 'scandalisback'),
])

PLAYERS = list(map(lambda name: re.compile(_TEMPLATE % name) if len(name) < 2 else re.compile(_TEMPLATE % name, flags=re.IGNORECASE), PLAYERS_TO_HANDLE.keys()))

PERSONALITIES_TO_HANDLE = OrderedDict([
    (r'2GD', 'follow2GD'),
    (r'AnneeDroid', 'AnneeDroid'),
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
    (r'grandgrant', 'GranDGranT'),
    (r'grant', 'GranDGranT'),
    (r'Hot_bid', 'Hot_Bid'),
    (r'Hotbid', 'Hot_Bid'),
    (r'kbbq', 'KBBQDotA'),
    (r'KotLGuy', 'KotLguy'),
    (r'LD', 'LDdota'),
    (r'Leafeator', 'Leafeator'),
    (r'Lumi', 'LuminousInverse'),
    (r'Luminous', 'LuminousInverse'),
    (r'LuminousInverse', 'LuminousInverse'),
    (r'Maelk', 'TheMaelk'),
    (r'Machine', 'MyNameIsMachine'),
    (r'Maut', 'MautDota'),
    (r'Merlini', 'MerliniDota'),
    (r'Monolith', 'CharlieYang'),
    (r'Nahaz', 'NahazDota'),
    (r'NoobFromUA', 'NoobFromUA'),
    (r'Noxville', 'NoxvilleZA'),
    (r'ODPixel', 'ODPixel'),
    (r'Purge', 'PurgeGamers'),
    (r'Sheever', 'sheevergaming'),
    (r'ReDeYe', 'PaulChaloner'),
    (r'SirActionSlacks', 'SirActionSlacks'),
    (r'SirBelvedere', 'BelvedereDota'),
    (r'Belvedere', 'BelvedereDota'),
    (r'Slacks', 'SirActionSlacks'),
    (r'SUNSfan', 'SUNSfanTV'),
    (r'Thorin', 'Thooorin'),
    (r'Tobi Wan', 'TobiWanDOTA'),
    (r'Tobi', 'TobiWanDOTA'),
    (r'TobiWan', 'TobiWanDOTA'),
    (r'TobiWans', 'TobiWanDOTA'),
    (r'tsunami', 'tsunami643'),
    (r'v1lat', 'v1lat'),
    (r'Wyk', 'wykrhm'),
    (r'wykrhm', 'wykrhm'),
    (r'Zyori', 'ZyoriTV'),
])

PERSONALITIES = list(map(lambda name: re.compile(_TEMPLATE % name) if len(name) < 2 else re.compile(_TEMPLATE % name, flags=re.IGNORECASE), PERSONALITIES_TO_HANDLE.keys()))

ORGS_TO_HANDLE = OrderedDict([
    # West
    (r'Ad Finem', 'AdFinemgg'),
    (r'Alliance', 'theAllianceGG'),
    (r'[A]lliance', 'theAllianceGG'),
    (r'The Alliance', 'theAllianceGG'),
    (r'BEAT Invitational', 'BEATesports'),
    (r'Code Red Esports', 'CodeRedEsport'),
    (r'CodeRedEsports', 'CodeRedEsport'),
    (r'CodeRed', 'CodeRedEsport'),
    (r'compLexity Gaming',  'compLexityLive'),
    (r'compLexity',  'compLexityLive'),
    (r'col',  'compLexityLive'),
    (r'datDota', 'datDota'),
    (r'DotaCinema', 'DotaCinema'),
    (r'Digital Chaos', 'DigitalChaosGG'),
    (r'DC', 'DigitalChaosGG'),
    (r'Dotabuff', 'DOTABUFF'),
    (r'DreamHack', 'DreamHack'),
    (r'DreamLeague', 'DHDreamLeague'),
    (r'Escape Gaming', 'TheEscapeGaming'),
    (r'Escape', 'TheEscapeGaming'),
    (r'ESL', 'ESLDota2'),
    (r'Evil Geniuses', 'EvilGeniuses'),
    (r'EG', 'EvilGeniuses'),
    (r'Fantastic Five', 'Fantastic__Five'),
    (r'FYM Hot Sauce', 'FYMHotSauce'),
    (r'FYMHotSauce', 'FYMHotSauce'),
    (r'FYM', 'FYMHotSauce'),
    (r'FDL', 'fdldota'),
    (r'Friendship, Dedication, Love', 'fdldota'),
    (r'Natus Vincere', 'NatusVincere'),
    (r'Kaipi', 'KaipiDota'),
    (r'MLG', 'MLG'),
    (r'NaVi', 'NatusVincere'),
    (r'Na Vi', 'NatusVincere'),
    (r'Na\'Vi', 'NatusVincere'),
    (r'Northern Arena', 'northernarena'),
    (r'NorthernArena', 'northernarena'),
    (r'(Team )?NP', 'NPDotA'),
    (r'OG', 'OGDota2'),
    (r'PGL', 'pglesports'),
    (r'Polarity', 'PolarityDota2'),
    (r'Power Rangers', 'prdota2'),
    (r'Red Bull', 'redbullesports'),
    (r'(Team )?Empire', 'Team_Empire'),
    (r'(Team )?Liquid', 'teamliquidpro'),
    (r'TL', 'teamliquidpro'),
    (r'(Team )?Secret', 'teamsecret'),
    (r'Team Spirit', 'Team__Spirit'),
    (r'TrackDota', 'TrackDota'),
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
    (r'YouTube Gaming', 'YouTubeGaming'),
    (r'YouTubeGaming', 'YouTubeGaming'),
    (r'YouTube', 'YouTubeGaming'),
    # Studios
    (r'BeyondTheSummit', 'beyondthesummit'),
    (r'BTS', 'beyondthesummit'),
    (r'joinDOTA', 'joinDOTA'),
    (r'jD', 'joinDOTA'),
    (r'moonduckTV', 'moonduckTV'),
    (r'moonduck', 'moonduckTV'),
])

ORGS = list(map(lambda name: re.compile(_TEMPLATE % name) if len(name) < 2 else re.compile(_TEMPLATE % name, flags=re.IGNORECASE), ORGS_TO_HANDLE.keys()))
