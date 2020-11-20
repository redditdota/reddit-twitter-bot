import re
from collections import OrderedDict

_TEMPLATE = r"(^|\W)(\@?%s)($|\W)"
REVERSE = re.compile(r"\(.*\)(.+)\\b")

def _compile(name):
    if "(" in name:
        name = name.replace("(", "(?:")

    if len(name) < 2:
        return re.compile(_TEMPLATE % name)
    else:
        return re.compile(_TEMPLATE % name, flags=re.IGNORECASE)

BLACK_LIST = ["shop", "dark moon", "darkmoon", "moon shard", "shadow demon", "black king bar", "black hole"]

PLAYERS = {
    #'BlackDotA2' : [r'Black']),
    #'dotaSolo' : [r'Solo']),
    #'Forev_Lee' : [r'FoREV']),
    #'GTHEMALL' : [r'G']),
    #'GTHEMALL' : [r'God']),
    #'scandalisback' : [r'Scandal'],
    #'WinteRDota' : [r'WinteR']),
    '1437x' : [r'1437', r'Theeban'],
    '33Dota' : [r'TheCoon', r'33'],
    'Ceb' : [r'7ckngMad', r'Seb', r'Ceb'],
    '9pashka' : [r'9pashaebashu', r'9pasha'],
    '_sneyking' : [r'Sneyking'],
    'abedyusop' : [r'Abed'],
    'AceDota' : [r'Ace'],
    'AdmiralBulldog' : [r'AdmiralBulldog', r'Bulldog', r'Bulldong', r'Donger', r'Dongerino', r'Dong'],
    'afoninje' : [r'Afoninje'],
    'afterlifedota2' : [r'AfterLife'],
    'alohad4nce' : [r'ALOHADANCE'],
    'anadota99' : [r'Ana'],
    'arteezy' : [r'Arteezy', r'rtz', r'artour'],
    'ArtStylee' : [r'Artstyle'],
    'arturfisura666' : [r'Goblak', r'Goblak'],
    'Aui_2000' : [r'Aui_2000', r'Aui'],
    'BananaSlamJamma' : [r'BSJ', 'BananaSlamJamma'],
    'Bignumdota' : [r'Bignum'],
    'BlackDotA2' : [r'Black^'],
    'bOne7dota' : [r'BOne7'],
    'boxi98' : [r'Boxi'],
    'braxlikesdota' : [r'Brax'],
    'bryledota' : [r'Bryle'],
    'BuLbaDotA_' : [r'BuLba'],
    'canceldota' : [r'canceL^^'],
    'CCnCDotA2' : [r'CC\&C', r'CCnC', r'CCC'],
    'chantseho' : [r'Hao'],
    'ChessieDota' : [r'Chessie'],
    'clairvoyance102' : [r'Clairvoyance'],
    'clementinator' : [r'Puppey', r'ppy'],
    'coL_zfreek' : [r'Zfreek'],
    'Cr1tdota' : [r'Cr1t\-', r'Cr1t'],
    'daxakdota2': [r'Daxak'],
    'DendiBoss' : [r'Dendi'],
    'Ditya_Ra_' : [r'Ditya\sRa', r'DityaRa', r'Ditya'],
    'DjardelJicko' : [r'DJ'],
    'DkPhobos' : [r'DkPhobos', r'Phobos'],
    'dotademon' : [r'Demon'],
    'DotaFata' : [r'FATA\-', r'FATA'],
    'Dusterdota' : [r'Duster'],
    'eradota' : [r'Era'],
    'eternalenvy1991' : [r'EternaLEnVy', r'EternaL\sEnVy', r'EE'],
    'Faith_bian' : [r'Faith_bian', r'Faithbian', r'Faith\sbian'],
    'FearDotA' : [r'Fear', r'FearDarkness'],
    'Febbydota' : [r'Febby'],
    'FLeeDOTA' : [r'FrancisLee', r'Francis', r'FLee'],
    'FLUFFDota' : [r'FLUFFNSTUFF', r'FLUFF'],
    'Fly_dota2' : [r'Fly'],
    'flydota' : [r'ALWAYSWANNAFLY'],
    'fnggshka' : [r'fng'],
    'FoggedDota' : [r'Fogged'],
    'FollowAkke' : [r'Akke'],
    'followEGM' : [r'EGM', r'EnterGodMode'],
    'FollowMag_' : [r'Mag', r'Mag\~'],
    'ForevDoto' : [r'Forev'],
    'fourdiar' : [r'4DR'],
    'Funn1kDota' : [r'Funn1k', r'Funnik'],
    'gabbidoto' : [r'Gabbi'],
    'Ghostikdota' : [r'Ghostik'],
    'gorgcdota' : [r'Gorgc'],
    'goddamDOTA' : [r'goddam', r'goddam'],
    'Gunnardota' : [r'Gunnar'],
    'Handsken1' : [r'Handsken'],
    'hFndot4' : [r'hFn'],
    'iamJERAX' : [r'JerAx'],
    'Icebergdota' : [r'Iceberg'],
    'iceiceicedota' : [r'iceiceice', r'icex3'],
    'IllidanSTRdoto' : [r'Illidan'],
    'insan1a' : [r'INsania', r'insan1a'],
    'ixmike88' : [r'ixmike88', r'ixmike'],
    'Jabzdota' : [r'Jabz'],
    'Jeyostyle' : [r'Jeyo'],
    'jonassomfan' : [r'Jonassomfan'],
    'JustXBOCT' : [r'Hvost', r'XBOCT'],
    'keepingitKyle' : [r'swindlezz', r'swindle', r'swindlemelonzz', r'kyle', r'melonzz', r'melon'],
    'KheZzu_' : [r'KheZu'],
    'KheZzu_' : [r'KheZzu'],
    'Kingrdxd' : [r'Kingrd'],
    'kpiidota' : [r'Kphoenii', r'Kpii'],
    'kukudota' : [r'Kuku'],
    'LilJke' : [r'Lil'],
    'LimmpDota' : [r'Limmp'],
    'lelisdota' : [r'Liposa'],
    'NigmaMiracle' : [r'Miracle\-', r'Miracle'],
    'NigmaGh' : [r'gh'],
    'NigmaKuroKy' : [r'Kuro', r'KuroKy'],
    'NikoDOTA' : [r'Niko(baby)?'],
    'MATUMBAMAN' : [r'MATUMBAMAN'],
    'NigmaMC' : [r'MinD_ContRoL', r'MinD\sContRoL', r'MinDContRoL'],
    'LodaBerg' : [r'Loda'],
    'MarchDota' : [r'March'],
    'madaradota2' : [r'Madara'],
    'masondota' : [r'Mason'],
    'Meracleeeeee' : [r'Meracle'],
    'mickeDOTA' : [r'MiCKe'],
    'midonedota2' : [r'MidOne', r'Miduan'],
    'milandota2' : [r'MiLAN'],
    'miposhka' : [r'Miposhka'],
    'MiSeRyDOTA' : [r'MiSeRy', r'moosery', r'MiSeRyTheSLAYER'],
    'mntdota' : [r'Maybe Next Time', r'mnt'],
    'MonkeysDota' : [r'Monkeys\sForever', r'Monkeys_Forever'],
    'moodota2' : [r'Moo'],
    'MoonMeanderated' : [r'MoonMeander'],
    'MSSDota' : [r'MSS'],
    'Mushi_Chai' : [r'Mushi'],
    'NewbeeChuaN' : [r'ChuaN'],
    'NewbeeMU' : [r'Mu'],
    'nishadota' : [r'Nisha'],
    'Noone_dota' : [r'Noone', r'No\[o\]ne'],
    'NutZdoto' : [r'NutZ'],
    'OG_BDN0tail' : [r'n0tail', r'notail', r'BDN', r'BigDaddyN0tail', r'BigDaddy'],
    'ohyohyohy' : [r'Ohaiyo'],
    'PajkattDota' : [r'Pajkatt'],
    'PatSoulDota2' : [r'PatSoul'],
    'Peksudota' : [r'Peksu'],
    'Peterpandam' : [r'ppd', r'peter'],
    'PieLieDieDota' : [r'pieliedie', r'pld'],
    'PR_chshrct' : [r'chshrct'],
    'qodota' : [r'QO'],
    'Qojqva1' : [r'qojqva'],
    'R1nater' : [r'KingR'],
    'ramzes' : [r'RAMZES666', r'Ramzes', r'SIXSIXSIX'],
    'Resolut1on_' : [r'Resolut1on'],
    'ritsudota' : [r'Ritsu'],
    'RobotViceDota' : [r'RobotVice'],
    'rmN_dota' : [r'rmN\-', r'rmN'],
    's4dota' : [r's4'],
    'Saksadota' : [r'Saksa'],
    'SammyboyGG' : [r'Sammyboy', r'Noblewingz'],
    'SexyBamboe' : [r'SexyBamboe', r'Bamboe'],
    'Silentdota2' : [r'Silent'],
    'SingSing' : [r'SingSing', r'Sing\sSing', r'Sing'],
    'skylarkXZ' : [r'SkyLark'],
    'sonneiko_o' : [r'SoNNeikO'],
    'ssaspartan' : [r'SsaSpartan'],
    'StanKingDota' : [r'Stan King', r'StanKing'],
    'SumaaaaiL' : [r'SumaiL'],
    'SVGDota' : [r'SVG'],
    'syndereNdota' : [r'syndereN'],
    'Taigadota' : [r'Taiga'],
    'tavodota' : [r'Tavo'],
    'TCDota' : [r'TC'],
    'ThuGdota2' : [r'ThuG'],
    'TimsDOTA' : [r'Tims'],
    'TopsonDota' : [r'Topson'],
    'undershock17' : [r'UnderShock'],
    'UniverseDota' : [r'UNiVeRsE'],
    'ushdota' : [r'USH'],
    'VANSKORdota' : [r'VANSKOR'],
    'NigmaW33' : [r'w33', r'w33haa'],
    'XcaliburYe' : [r'Xcalibur'],
    'XctNKim0' : [r'Kim0'],
    'xNovadota' : [r'xNova'],
    'XtinctDota' : [r'XtiNcT'],
    'y1122Innocence' : [r'innocence', r'y`'],
    'YapzOrdota' : [r'YapzOr'],
    'yawar_ys' : [r'YawaR'],
    'yokydota' : [r'yoky\-', r'yoky'],
    'Xibbe' : [r'Xibbe'],
    'zai_2002' : [r'zai'],
}
PLAYERS = { handle : [_compile(name) for name in names] for handle, names in PLAYERS.items()}

ARTIFACT = {
    'PlayArtifact' : [r'Artifact'],
    'Liquid_Fr0zen' : [r'fr0zen'],
    'Liquid_hsdog' : [r'dog'],
    'coL_superjj102' : [r'SuperJJ'],
    'Naiman_HS' : [r'Naiman'],
    'Lifecoach1981' : [r'Lifecoach'],
    'Wifecoach1981' : [r'Wifecoach'],
    'StanCifka' : [r'StanCifka', 'Stan', 'luckbox'],
    'OndrejStrasky' : [r'Honey'],
    'Hyped_AF' : [r'hyped'],
    'pascalmaynard' : [r'PMayne'],
    'Mryagut' : [r'Mryagut'],
    'drhippi_vp' : [r'DrHippi', r'DrHippiXD'],
    'Ekop' : [r'Ekop'],
    'GameKingHS' : [r'GameKing'],
    'dpmlicious' : [r'dpmlicious'],
    'Amaz' : [r'Amaz'],
    'coL_Petrify' : [r'Petrify'],
    'followMelo' : [r'MELO'],
    'aj_casts' : [r'Action\sJackson'],
    'fwoshy' : [r'fwosh', r'fwoshy'],
    'Savjz' : [r'Savjz'],
    'swimstrim' : [r'swim', r'swimstrim'],
    'TidesofTime' : [r'tidesoftime'],
}

ARTIFACT = { handle : [_compile(name) for name in names] for handle, names in ARTIFACT.items()}

PERSONALITIES = {
    'AnneeDroid' : [r'AnneeDroid'],
    'ayesee' : [r'Ayesee'],
    'BelvedereDota' : [r'Belvedere'],
    'BelvedereDota' : [r'SirBelvedere'],
    'Big__Blake50' : [r'Blake Martinez', r'Blake'],
    'Blitz_DotA' : [r'Blitz'],
    'breakycpk' : [r'breakycpk', r'breaky'],
    'BTSGoDz' : [r'GoDz'],
    'CharlieYang' : [r'Charlie Yang', r'Charlie', r'CharlieYang', r'Monolith'],
    'Cyborgmatt' : [r'Cyborgmatt'],
    'day9tv' : [r'day9', r'day 9', r'day\[9\]'],
    'diredude' : [r'diredude'],
    'dotabuff' : [r'dotabuff'],
    'DotaCapitalist' : [r'Cap', r'Capitalist'],
    'Draskyl' : [r'Draskyl'],
    'esportsexpress' : [r'esex', r'esportsexpress'],
    'follow2GD' : [r'2GD'],
    'Noxville' : [r'Noxville'],
    'ForsenSC2' : [r'Forsen'],
    'fwoshy' : [r'fwosh', r'fwoshy'],
    'GarethCasts' : [r'Gareth', r'Durka'],
    'GranDGranT' : [r'grandgrant', r'grant'],
    'Hot_Bid' : [r'Hot_bid', r'Hotbid'],
    'JJLiebig' : [r'PimpmuckL'],
    'KaciAitchison' : [r'Kaci'],
    'KBBQDotA' : [r'kbbq'],
    'KillerPigeon' : [r'KillerPigeon', r'Pigeon'],
    'KotLguy' : [r'KotLGuy'],
    'LacosteDota' : [r'Lacoste'],
    'LDeeep' : [r'LD'],
    'Leafeator' : [r'Leafeator'],
    'LuminousInverse' : [r'Lumi', r'Luminous', r'LuminousInverse'],
    'LyricalDota' : [r'Lyrical'],
    'Maradota2' : [r'Mara'],
    'MautDota' : [r'Maut'],
    'MerliniDota' : [r'Merlini'],
    'MoxxiCasts' : [r'Moxxi'],
    'MyNameIsMachine' : [r'Machine'],
    'NahazDota' : [r'Nahaz'],
    'NoobFromUA' : [r'NoobFromUA'],
    'ODPixel' : [r'ODPixel'],
    'PaulChaloner' : [r'ReDeYe'],
    'Phillip_Aram' : [r'EG manager', r'Phil'],
    'PurgeGamers' : [r'Purge'],
    'PyrionFlax' : [r'Pyrion', r'PyrionFlax'],
    'sheevergaming' : [r'Sheever'],
    'SirActionSlacks' : [r'SirActionSlacks', r'Slacks'],
    'skrff' : [r'skrff'],
    'StatsmanBruno' : [r'Bruno'],
    'SUNSfanTV' : [r'SUNSfan'],
    'TheMaelk' : [r'Maelk'],
    'Thooorin' : [r'Thorin'],
    'TobiWanDOTA' : [r'Tobi\sWan', r'Tobi', r'TobiWan', r'TobiWans'],
    'TonyaPredko' : [r'Tonya', r'TonyaPredko'],
    'TorteDeLini' : [r'TorteDeLini', r'Torte'],
    'TrentPax' : [r'Trent', r'TrentPax'],
    'tsunami643' : [r'tsunami', r'tsunami643'],
    'v1lat' : [r'v1lat'],
    'WagaGaming' : [r'Waga', r'Wagamama'],
    'Weppas_' : [r'Weppas_', r'Weppas'],
    'wykrhm' : [r'Wyk', r'wykrhm'],
    'Xyclopzz' : [r'xyclopz', r'xyclopzz'],
    'ZyoriTV' : [r'Zyori'],
}
PERSONALITIES = { handle : [_compile(name) for name in names] for handle, names in PERSONALITIES.items()}


ORGS = {
    #'MVP' : [r'MVP'],
    #'AdFinemgg' : [r'Ad Finem'],
    #'IcebergEsports' : [r'Iceberg'],
    #'NPDotA' : [r'(Team )?NP'],
    #'TheEscapeGaming' : [r'Escape'],
    'B8esportsGG' : [r'B8'],
    'BEATesports' : [r'BEAT Invitational'],
    'Beastcoast': [r'beastcoast'],
    'beyondthesummit' : [r'BeyondTheSummit', r'BTS'],
    'boomesportsid': [r'Boom Esports'],
    'ChaosEC' : [r'Chaos Esports Club'],
    'Cloud9' : [r'C9', r'Cloud 9', r'Cloud9'],
    'CodeRedEsport' : [r'Code Red Esports', r'CodeRed', r'CodeRedEsports'],
    'compLexity' : [r'col', r'compLexity Gaming', r'compLexity'],
    'cyblegacy' : [r'Cyber Legacy'],
    'datDota' : [r'datDota'],
    'DigitalChaosGG' : [r'Digital Chaos'],
    'DOTA2' : [r'\bDota(\s)?(2)?\b'],
    'DOTABUFF' : [r'Dotabuff'],
    'DotaCinema' : [r'DotaCinema'],
    'DotaPit' : [r'Dota\sPit', r'Dotapit'],
    'DoubleDimensio1' : [r'Double Dim(ension)?'],
    'DreamHackDota' : [r'DreamHack', r'DreamLeague'],
    'effectgg' : [r'Effect Gaming'],
    'EHOMECN' : [r'EHOME'],
    'epicentergg' : [r'EPICENTER'],
    'ESLDota2' : [r'ESL'],
    'EvilGeniuses' : [r'EG', r'Evil Geniuses'],
    'ExecrationGG' : [r'Execration', r'XctN'],
    'Fantastic__Five' : [r'Fantastic Five'],
    'fdldota' : [r'FDL', r'Friendship, Dedication, Love'],
    'FNATIC' : [r'Fnatic'],
    'FTM_dota2' : [r'FlyToMoon', r'FTM'],
    'FYMHotSauce' : [r'FYM Hot Sauce', r'FYM', r'FYMHotSauce'],
    'TeamGeekFam' : [r'GeekFam', r'Geek Fam'],
    'geschampionship' : [r'GES Champ.*', r'GES', r'GESC', r'GESC'],
    'HELLRAISERSgg' : [r'\bhr\b', r'hellraiser(s)?'],
    'HGT_Team' : [r'HGT', r'HyperGloryTeam'],
    'Immortals' : [r'Immortals', r'Imt'],
    'infamous_gg' : [r'Infamous'],
    'invgaming' : [r'IG', r'Invictus Gaming'],
    'joinDOTA' : [r'jD', r'joinDOTA'],
    'LGDgaming' : [r'LGD Gaming', r'LGD'],
    'm19official' : [r'M19'],
    'MercedesBenz' : [r'Mercedes Benz', r'Mercedes', r'MercedesBenz'],
    'Mineski' : [r'Mineski'],
    'MLG' : [r'MLG'],
    'moonduckTV' : [r'moonduck', r'moonduckTV'],
    'mousesports' : [r'mousesports', r'mouz'],
    'MVP_GG' : [r'MVP Phoenix'],
    'NatusVincere' : [r'Na Vi', r'Na\'Vi', r'Natus Vincere', r'NaVi'],
    'NewbeeCN' : [r'NB', r'Newbee'],
    'TeamNigma': [r'(Team )?Nigma'],
    'NiPGaming': [r'NiP', r'Ninjas in Pyjamas'],
    'northernarena' : [r'Northern Arena', r'NorthernArena'],
    'OGDota2' : [r'OG'],
    'OpTicGaming' : [r'Optic\bGaming', r'Optic'],
    'paingamingbr' : [r'paiN\bGaming'],
    'PENTA_Sports' : [r'PENTA'],
    'pglesports' : [r'PGL'],
    'PolarityDota2' : [r'Polarity'],
    'prdota2' : [r'Power\bRangers'],
    'PSGeSports' : [r'PSG'],
    'RealityRift_gg' : [r'Reality\bRift'],
    'redbullesports' : [r'Red\bBull'],
    'SGe_sports' : [r'SG\be\-sports', 'SG esports', 'SGesports'],
    'adroitdota' : [r'Team\bAdroit', 'Adroit Esports'],
    'Team__Spirit' : [r'Team\bSpirit'],
    'Team_Empire' : [r'(Team )?Empire'],
    'Team_VGJ' : [r'(Team )?VGJ', r'VG\.J', r'VGJ'],
    'TeamClutchGamer' : [r'CG', r'Clutch Gamer', r'Clutch Gamers'],
    'TEAMFREEDOMgg' : [r'Team Freedom'],
    'teamkinguin' : [r'(Team )?Kinguin'],
    'TeamLiquid' : [r'(Team )?Liquid', r'TL'],
    'teamsecret' : [r'(Team )?Secret'],
    'TeamTuho' : [r'(Team )?Tuho'],
    'theAllianceGG' : [r'[A]lliance', r'Alliance', r'The Alliance'],
    'TheEscapeGaming' : [r'Escape Gaming'],
    'themastersgg' : [r'(The )?Manila Master(s)?'],
    'tigers_dota' : [r'Tiger(s)?'],
    'TNCPredator' : [r'TNC Gaming', r'TNC Predator', r'TNC'],
    'TrackDota' : [r'TrackDota'],
    'Twitch' : [r'Twitch'],
    'VegaSquadron' : [r'Vega Squadron', r'Vega'],
    'VeggieEsports' : [r'VEC', r'Vegetables Esports Club', r'Veggies\bEsports', r'Veggies', r'VeggiesEsports'],
    'VICI' : [r'VG', r'VG.R', r'VG.Reborn', r'Vici Gaming Reborn', r'Vici Gaming', r'Vici'],
    'GGVikin' : [r'Vikin.gg', r'Vikingg'],
    'virtuspro' : [r'Virtus Pro', r'Virtus.Pro', r'VirtusPro', r'VP'],
    'WarriorsGamingU' : [r'WarriorsGaming', r'WarriorsGaming.Unity', r'WarriorsGamingU', r'WG.Unity', r'WGU', r'WGUnity'],
    'wingsgamingcn' : [r'Wings Gaming', r'Wings'],
    'YouTubeGaming' : [r'YouTube Gaming', r'YouTube', r'YouTubeGaming'],
}

ORGS = { handle : [_compile(name) for name in names] for handle, names in ORGS.items()}

