from src.common.template_applier import TemplateApplier
import random

class RWYRTemplateApplier(TemplateApplier):
    def __init__(self):
        super().__init__()

    def generate_random_wyr(self):
        r_number = random.randint(1, 17)
        return self.random_wyr(r_number)

    def random_wyr(self, template_id):
        try:
            template = getattr(self, str("template_" + str(template_id)))
        except AttributeError:
            raise NotImplementedError("Class `{}` does not implement `{}`".format(self.__class__.__name__, str("template_" + str(template_id))))
        self.connect_db()
        sentence = template()
        self.close_db_connection()
        return sentence

    def format_to_message(self, question, choicea, choiceb):
        return question + "\n:regional_indicator_a: `" + choicea + "`\nOR\n:b: `" + choiceb + "`"

    def template_1(self):
        verb = self.get_random_t_verb()
        verb2 = self.get_random_t_verb()
        noun = self.get_random_noun()
        noun2 = self.get_random_noun('plural')
        return self.format_to_message('Would you rather...', verb.capitalize() + ' a ' + noun, verb2.capitalize() + noun2)

    def template_2(self):
        verb = self.get_random_t_verb()
        noun = self.get_random_noun()
        verb2 = self.get_random_t_verb()
        noun2 = self.get_random_noun()
        return self.format_to_message('Would you rather...', verb.capitalize() + ' a ' + noun, verb2.capitalize() + ' a ' + noun2)

    def template_3(self):
        verb = self.get_random_i_verb()
        verb2 = self.get_random_i_verb()
        return self.format_to_message('Would you rather...', verb.capitalize(), verb2.capitalize())

    def template_4(self):
        verb = self.get_random_t_verb()
        noun = self.get_random_noun()
        verb2 = self.get_random_t_verb('past')
        noun2 = self.get_random_noun()
        verb3 = self.get_random_t_verb()
        return self.format_to_message('Would you rather...',
        verb.capitalize() + ' a ' + noun + ' who just ' + verb2 + ' your ' + noun2, verb3.capitalize() + ' them')

    def template_5(self):
        noun = self.get_random_noun()
        verb = self.get_random_t_verb()
        noun2 = self.get_random_noun()
        adjective = self.get_random_adjective()
        return self.format_to_message('Would you rather become...',
        'A ' + noun + ', but you will ' + verb + ' your ' + noun2, adjective.capitalize())

    def template_6(self):
        verb = self.get_random_t_verb('past')
        verb2 = self.get_random_t_verb()
        return self.format_to_message('Would you rather...', 'Be ' + verb, verb2.capitalize())

    def template_7(self):
        noun = self.get_random_noun()
        verb = self.get_random_t_verb()
        noun2 = self.get_random_noun()
        adjective = self.get_random_adjective()
        adjective2 = self.get_random_adjective()
        adjective3 = self.get_random_adjective()
        noun3 = self.get_random_noun()
        return self.format_to_message('Would you rather name a movie you direct as...',
        noun.capitalize() + ' ' + verb + ' ' + noun2, 'The ' +
        adjective + ' ' + adjective2 + ' ' + adjective3 + ' ' + noun3)

    def template_8(self):
        verb = self.get_random_t_verb('gerund')
        noun = self.get_random_noun('plural')
        verb2 = self.get_random_t_verb('gerund')
        noun2 = self.get_random_noun('plural')
        return self.format_to_message('Would you rather have your work related to...',
        verb.capitalize() + ' ' + noun, verb2.capitalize() + ' ' + noun2)

    def template_9(self):
        noun = self.get_random_noun('plural')
        adjective = self.get_random_adjective()
        adjective2 = self.get_random_adjective()
        noun2 = self.get_random_noun('plural')
        adjective3 = self.get_random_adjective()
        return self.format_to_message('Would you rather have...',
        noun.capitalize() + ' to be ' + adjective, adjective2.capitalize() +
        ' ' + noun2 + ' to be ' + adjective3)

    def template_10(self):
        verb = self.get_random_t_verb()
        noun = self.get_random_noun('plural')
        verb2 = self.get_random_t_verb()
        noun2 = self.get_random_noun('plural')
        return self.format_to_message('Would you rather...',
        'Never be able to ' + verb + ' ' + noun,
        'Never be able to ' + verb2 + ' ' + noun2)

    def template_11(self):
        verb = self.get_random_t_verb()
        noun = self.get_random_noun('plural')
        verb2 = self.get_random_t_verb('past')
        return self.format_to_message('Would you rather...',
        verb.capitalize() + ' your ' + noun, 'Be ' + verb2 + ' by your ' + noun)

    def template_12(self):
        noun = self.get_random_noun('plural')
        noun2 = self.get_random_noun('plural')
        return self.format_to_message('Would you rather clean a room full of...',
        noun.capitalize(), noun2.capitalize())

    def template_13(self):
        adjective = self.get_random_adjective()
        noun = self.get_random_noun('plural')
        adjective2 = self.get_random_adjective()
        noun2 = self.get_random_noun('plural')
        return self.format_to_message('Would you rather be...',
        adjective.capitalize() + ' with no ' + noun,
        adjective2.capitalize() + ' with no ' + noun2)

    def template_14(self):
        noun = self.get_random_noun('plural')
        noun2 = self.get_random_noun('plural')
        return self.format_to_message('Would you rather afraid of...', noun.capitalize(), noun2.capitalize())

    def template_15(self):
        adverb = self.get_random_adverb()
        verb = self.get_random_t_verb('past')
        noun = self.get_random_noun()
        verb2 = self.get_random_t_verb('past')
        noun2 = self.get_random_noun()
        return self.format_to_message('Would you rather be...',
        adverb.capitalize() + ' ' + verb + ' by a ' + noun,
        verb2.capitalize() + ' by a ' + noun2)

    def template_16(self):
        noun = self.get_random_noun()
        noun2 = self.get_random_noun()
        return self.format_to_message('Would you rather become a...', noun.capitalize(), noun2.capitalize())

    def template_17(self):
        verb = self.get_random_t_verb()
        adjective = self.get_random_adjective()
        noun = self.get_random_noun('plural')
        verb2 = self.get_random_t_verb()
        adjective2 = self.get_random_adjective()
        noun2 = self.get_random_noun('plural')
        return self.format_to_message('Would you rather only be able to...',
        verb.capitalize() + ' ' + adjective + ' ' + noun,
        verb2.capitalize() + ' ' + adjective2 + ' ' + noun2)
