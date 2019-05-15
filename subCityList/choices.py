# server team tags - this is for my personal team, but if it were for profit, I would have the alliance host
# enter these choices in on a setup screen, then dynamically set the alliance team names with a loop
# what team they're on allows you to query what subcities belong to a team
DOA = 'DOA'
GRY = 'GRY'
GHO = 'GHO'
RIP = 'RIP'
BOB = 'BOB'
GNX = 'BOB'
EAD = 'EAD'
VN1 = 'VN1'
UTO = 'UTO'
TAGLESS = ' '  # it is possible for someone to be alone, not on a team. We call this being tagless.

TEAM_NAMES = (
    (DOA, 'DOA'),
    (GRY, 'GRY'),
    (GHO, 'GHO'),
    (RIP, 'RIP'),
    (BOB, 'BOB'),
    (GNX, 'GNX'),
    (EAD, 'EAD'),
    (VN1, 'VN1'),
    (UTO, 'UTO'),
    (TAGLESS, ' '),
)

# Every player has a ranking they have earned. The ranking earns you the ability to hold a certain number of
# subcities outside your main. For each rank, this is the maximum number of cities you can hold.
# Need this for checks - flag a person that has too many subs
ARCHDUKE = 8
DUKE = 7
EARL = 6
VISCOUNT = 5
BARON = 4
KNIGHT = 3
RANKS = (
    (ARCHDUKE, 'ARCHDUKE'),
    (DUKE, 'DUKE'),
    (EARL, 'EARL'),
    (VISCOUNT, 'VISCOUNT'),
    (BARON, 'BARON'),
    (KNIGHT, 'KNIGHT'),
)

# There are seven cultures in the game. I will save by country abbr.
ARABIA = 'SA'
AMERICA = 'US'
CHINA = 'CN'
EUROPE = 'EU'
JAPAN = 'JP'
KOREA = 'KR'
RUSSIA = 'RU'
SUB_CULTURE = (
    (ARABIA, 'ARABIA'),
    (AMERICA, 'AMERICA'),
    (CHINA, 'CHINA'),
    (EUROPE, 'EUROPE'),
    (JAPAN, 'JAPAN'),
    (KOREA, 'KOREA'),
    (RUSSIA, 'RUSSIA'),
)

# There are five levels, but no one saves white sub coords. most don't even save green, though I'm including
# The color indicates if it is an epic, legendary, excellent, or common quality
EPIC = 'GLD'
LEGENDARY = 'PUR'
EXCELLENT = 'BLU'
COMMON = 'GRN'
SUB_QUALITY = (
    (EPIC, 'GOLD'),
    (LEGENDARY, 'PURPLE'),
    (EXCELLENT, 'BLUE'),
    (COMMON, 'GREEN'),
)
