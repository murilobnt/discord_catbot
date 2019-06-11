from catbot_database import CatbotDatabase

c_db = CatbotDatabase()
c_db.connect()
cursor = c_db.cursor

verbs = [
('transitive', 'hug', 'hugged', 'hugging', 'hugs'),
('transitive', 'marry', 'married', 'marrying', 'marries'),
('transitive', 'throw away', 'threw away', 'throwing away', 'throws away'),
('transitive', 'make', 'made', 'making', 'makes'),
('transitive', 'sell', 'sold', 'selling', 'sells'),
('transitive', 'like', 'liked', 'liking', 'likes'),
('transitive', 'fight', 'fought', 'fighting', 'fights'),
('transitive', 'watch', 'watched', 'watching', 'watches'),
('transitive', 'burn', 'burned', 'burning', 'burns'),
('transitive', 'find', 'found', 'finding', 'finds'),
('transitive', 'help', 'helped', 'helping', 'helps'),
('transitive', 'become', 'became', 'becoming', 'becomes'),
('transitive', 'leave', 'left', 'leaving', 'leaves'),
('transitive', 'draw', 'drew', 'drawing', 'draws'),
('transitive', 'hold', 'held', 'holding', 'holds'),
('transitive', 'remember', 'remembered', 'remembering', 'remembers'),
('transitive', 'eat', 'ate', 'eating', 'eats'),
('transitive', 'need', 'needed', 'needing', 'needs'),
('transitive', 'roll', 'rolled', 'rolling', 'rolls'),
('intransitive', 'sleep', 'slept', 'sleeping', 'sleeps'),
('intransitive', 'die', 'died', 'dying', 'dies'),
('intransitive', 'clap', 'clapped', 'clapping', 'claps'),
('intransitive', 'exist', 'existed', 'existing', 'exists'),
('intransitive', 'vanish', 'vanished', 'vanishing', 'vanishes'),
('intransitive', 'collapse', 'collapsed', 'collapsing', 'collapses'),
('intransitive', 'lie', 'lied', 'lying', 'lies'),
('intransitive', 'laugh', 'laughed', 'laughing', 'laughs')
]

adjectives = [
('cute',),
('happy',),
('sad',),
('black',),
('free',),
('little',),
('old',),
('young',),
('special',),
('fake',),
('fat',),
('strong',),
('salty',),
('mad',),
('high',),
('best',),
('blind',),
('deaf',),
('mute',)
]

adverbs = [
('purposely',),
('carefully',),
('carelessly',),
('purposely',),
('secretely',),
('quickly',),
('accidentally',),
('finally',)
]

nouns = [
('bear', 'bears'),
('cat', 'cats'),
('child', 'children'),
('family', 'families'),
('eye', 'eyes'),
('student', 'students'),
('money', 'moneys'),
('world', 'worlds'),
('book', 'books'),
('house', 'houses'),
('pillow', 'pillows'),
('car', 'cars'),
('hedgehog', 'hedgehogs'),
('lemonade', 'lemonades'),
('toe', 'toes'),
('spider', 'spiders'),
('chocolate bar', 'chocolate bars'),
('bot', 'bots'),
('gun', 'guns'),
('zombie', 'zombies'),
('boat', 'boats'),
('nomad', 'nomads'),
('toy', 'toys'),
('phone', 'phones'),
('computer', 'computers'),
('ground', 'grounds'),
('server', 'servers'),
('potato', 'potatoes'),
('game', 'games'),
('pokémon', 'pokémon'),
('cowboy', 'cowboys'),
('hobo', 'hobos'),
('deer', 'deers'),
('outlaw', 'outlaws'),
('sheep', 'sheeps'),
('potato chip', 'potato chips'),
('bird', 'birds'),
('plane', 'planes')
]

cursor.executemany("""INSERT INTO verbs (type, value, past, gerund, third) VALUES (%s,%s,%s,%s,%s)""", verbs)
cursor.executemany("""INSERT INTO adjectives (value) VALUES (%s)""", adjectives)
cursor.executemany("""INSERT INTO adverbs (value) VALUES (%s)""", adverbs)
cursor.executemany("""INSERT INTO nouns (value, plural) VALUES (%s,%s)""", nouns)

c_db.commit()
c_db.close()
