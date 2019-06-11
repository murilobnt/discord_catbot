import sqlite3
import random

from psycopg2.extensions import AsIs
from src.database.catbot_database import CatbotDatabase

class TemplateContainer:
    def __init__(self):
        self.cb_d = CatbotDatabase()

    def generate_random_story(self, mention):
        r_number = random.randint(1, 40)
        return self.random_story(mention, r_number)

    def random_story(self, mention, template_id):
        try:
            template = getattr(self, str("template_" + str(template_id)))
        except AttributeError:
            raise NotImplementedError("Class `{}` does not implement `{}`".format(self.__class__.__name__, "template_1"))
        self.connect_db()
        sentence = template(mention)
        self.close_db_connection()
        return sentence

    def connect_db(self):
        self.cb_d.connect()
        self.cursor = self.cb_d.cursor

    def close_db_connection(self):
        self.cb_d.close()

    def get_random_noun(self, field = "value"):
        self.cursor.execute("SELECT %s FROM nouns ORDER BY RANDOM() LIMIT 1", (AsIs(field),))
        return str(self.cursor.fetchone()[0])

    def get_random_adjective(self, field = "value"):
        self.cursor.execute("SELECT %s FROM adjectives ORDER BY RANDOM() LIMIT 1", (AsIs(field),))
        return str(self.cursor.fetchone()[0])

    def get_random_adverb(self, field = "value"):
        self.cursor.execute("SELECT %s FROM adverbs ORDER BY RANDOM() LIMIT 1", (AsIs(field),))
        return str(self.cursor.fetchone()[0])

    def get_random_t_verb(self, field = "value"):
        self.cursor.execute("SELECT %s FROM verbs WHERE type='transitive' ORDER BY RANDOM() LIMIT 1", (AsIs(field),))
        return str(self.cursor.fetchone()[0])

    def get_random_i_verb(self, field = "value"):
        self.cursor.execute("SELECT %s FROM verbs WHERE type='intransitive' ORDER BY RANDOM() LIMIT 1", (AsIs(field),))
        return str(self.cursor.fetchone()[0])

    def template_1(self, mention):
        verb = self.get_random_t_verb("third")
        noun = self.get_random_noun()
        return str(mention + " " + verb + " their " + noun + ".")

    def template_2(self, mention):
        noun = self.get_random_noun("plural")
        adjective = self.get_random_adjective()
        return str(noun.capitalize() + " are " + adjective + ", but " + mention + " didn't know it.")

    def template_3(self, mention):
        noun = self.get_random_noun()
        return str("I found \"I want to be a " + noun + "\" in " + mention + "'s browser search history.")

    def template_4(self, mention):
        adverb = self.get_random_adverb()
        verb = self.get_random_t_verb("past")
        noun = self.get_random_noun()
        return str(mention + " " + adverb + " " + verb + " their " + noun + ".")

    def template_5(self,  mention):
        verb = self.get_random_t_verb("third")
        noun = self.get_random_noun()
        return str("When life gives lemons, " + mention + " " + verb + " a " + noun + ".")

    def template_6(self, mention):
        noun = self.get_random_noun()
        adjective = self.get_random_adjective()
        return str("Hey! It's " + mention + "! a.k.a. the super " + adjective + " " + noun + ".")

    def template_7(self, mention):
        noun1 = self.get_random_noun()
        noun2 = self.get_random_noun()
        verb = self.get_random_t_verb()
        return str(mention + " sold their " + noun1 + " to " + verb + " a " + noun2 + ".")

    def template_8(self, mention):
        noun1 = self.get_random_noun("plural")
        noun2 = self.get_random_noun("plural")
        return str("I like " + noun1 + ". " + mention + " likes " + noun2 + ".")

    def template_9(self, mention):
        verb = self.get_random_t_verb()
        noun = self.get_random_noun()
        return str("Just give " + mention + " a reason and they will " + verb + " you for a " + noun + ".")

    def template_10(self, mention):
        noun1 = self.get_random_noun("plural")
        noun2 = self.get_random_noun("plural")
        adverb = self.get_random_adverb()
        verb = self.get_random_t_verb()
        return str("No, " + mention + ", " + noun1 + " don't " + adverb + " " + verb + " your " + noun2 + ".")

    def template_11(self, mention):
        adjective = self.get_random_adjective()
        noun = self.get_random_noun("plural")
        return str("It's widely known " + mention + " is " + adjective + " because of " + noun + ".")

    def template_12(self, mention):
        noun1 = self.get_random_noun()
        noun2 = self.get_random_noun()
        return str("It's a " + noun1 + "... It's a " + noun2 + "... Nah, it's just " + mention + ".")

    def template_13(self, mention):
        adjective = self.get_random_adjective()
        noun = self.get_random_noun()
        return str("Subscribe to " + mention + "'s YouTube channel. If you don't, you're a " + adjective + " " + noun + ".")

    def template_14(self, mention):
        noun = self.get_random_noun("plural")
        verb = self.get_random_t_verb()
        return str(mention + ", take the wheel. There are " + noun + " ahead, and we need to " + verb + " them.")

    def template_15(self, mention):
        verb = self.get_random_t_verb()
        return str("Hello, everyone. Bot here. " + mention + " does not " + verb + " me anymore, and I'm sad about it.")

    def template_16(self, mention):
        noun = self.get_random_noun("plural")
        return str("Get back to work, " + mention + ", the " + noun + " aren't gonna be made by themselves.")

    def template_17(self, mention):
        adjective = self.get_random_adjective()
        return str("Beep. Boop. Analysing user " + mention + ". Analysis completed. It shows they're " + adjective + ".")

    def template_18(self, mention):
        verb1 = self.get_random_t_verb()
        noun1 = self.get_random_noun()
        adverb = self.get_random_adverb()
        verb2 = self.get_random_t_verb()
        adjective = self.get_random_adjective()
        noun2 = self.get_random_noun()
        return str("From " + mention + "'s cookbook. Step 1: " + verb1 + " a " + noun1 + ". Step 2: " + adverb + " " + verb2 + " a " + adjective + " " + noun2 + ". Step 3: Profit!")

    def template_19(self, mention):
        noun = self.get_random_noun("plural")
        adjective = self.get_random_adjective()
        adjective2 = self.get_random_adjective()
        return str(noun.capitalize() + " are " + adjective + ". " + mention + " is " + adjective2 + ".")

    def template_20(self, mention):
        noun = self.get_random_noun()
        adverb = self.get_random_adverb()
        return str(mention + " said I am a " + noun + ". Do I " + adverb + " do " + noun + " stuff? Really?")

    def template_21(self, mention):
        adjective = self.get_random_adjective()
        noun = self.get_random_noun()
        return str("It's over, " + mention + "! I have the " + adjective + " " + noun + ".")

    def template_22(self, mention):
        adjective = self.get_random_adjective()
        return str("I refuse to work on this template. So, I'm just going to say " + mention + " is " + adjective + ".")

    def template_23(self, mention):
        verb = self.get_random_t_verb()
        noun = self.get_random_noun("plural")
        return str("Hey, " + mention + ", wake up! It's time to " + verb + " some " + noun + ".")

    def template_24(self, mention):
        adverb = self.get_random_adverb()
        iverb = self.get_random_i_verb()
        return str("Maybe, someday, " + mention + " will " + adverb + " " + iverb + ".")

    def template_25(self, mention):
        return str("This was supposed to be a secret, but I need to say: " + mention + " liked YouTube Rewind.")

    def template_26(self, mention):
        noun = self.get_random_noun()
        return str("What is this?! A " + noun.upper() + "?! " + mention + ", explain it. NOW.")

    def template_27(self, mention):
        noun = self.get_random_noun()
        iverb = self.get_random_i_verb("past")
        iverb2 = self.get_random_i_verb("past")
        return str("A " + noun + " " + iverb + ". And what did " + mention + " do? They " + iverb2 + ".")

    def template_28(self, mention):
        iverb = self.get_random_i_verb("past")
        noun = self.get_random_noun("plural")
        return str("This is Mr. Bot from Bot News. " + mention + " just " + iverb + ". Coming up next: Are " + noun + " real? We investigate.")

    def template_29(self, mention):
        noun = self.get_random_noun()
        verb = self.get_random_t_verb()
        return str(mention + " once told me the " + noun + " is gonna " + verb + " me.")

    def template_30(self, mention):
        adverb = self.get_random_adverb()
        verb = self.get_random_t_verb()
        noun = self.get_random_noun("plural")
        return str("Me and " + mention + " decided to team up. We plan to " + adverb + " " + verb + " " + noun + ".")

    def template_31(self, mention):
        iverb = self.get_random_i_verb()
        adjective = self.get_random_adjective()
        return str("If " + mention + " does not " + iverb + ", they will be " + adjective + ".")

    def template_32(self, mention):
        noun = self.get_random_noun()
        return str("Let me take a look at " + mention + "'s " + noun + "... I shouldn't've looked.")

    def template_33(self, mention):
        adjective = self.get_random_adjective()
        return str("Excuse me, " + mention + ", I don't speak the " + adjective + " people dialect.")

    def template_34(self, mention):
        return str("I quit. " + mention + ", you're the bot now.")

    def template_35(self, mention):
        adverb = self.get_random_adverb()
        iverb = self.get_random_i_verb("past")
        return str("I played a game with " + mention + " once. Of course I " + adverb + " " + iverb + ".")

    def template_36(self, mention):
        noun = self.get_random_noun("plural")
        return str("Can we all take a moment to talk about " + noun + "? " + mention + ", the word is yours.")

    def template_37(self, mention):
        noun = self.get_random_noun()
        return str("Thank you, " + mention + ", you've been a good " + noun + ".")

    def template_38(self, mention):
        noun = self.get_random_noun("plural")
        return str(mention + " vs " + noun + ". Who would win?")

    def template_39(self, mention):
        noun = self.get_random_noun()
        return str(mention + ", buy me a " + noun + ". Pleeease?")

    def template_40(self, mention):
        noun = self.get_random_noun()
        return str(mention + " is my favorite " + noun + " around here ;)")
