#
# This file is part of Dragonfly.
# (c) Copyright 2007, 2008 by Christo Butcher
# Licensed under the LGPL.
#
#   Dragonfly is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License as published
#   by the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Dragonfly is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with Dragonfly.  If not, see
#   <http://www.gnu.org/licenses/>.
#




#---------------------------------------------------------------------------
from copy import copy
from dragonfire import Rule, Grammar, get_engine
from dragonfire.grammar.elements_compound import Compound, Choice

__current_grammar_id = 1
__grammar_ids = {}

__current_rule_id = 1
__rule_mapping = {}

__current_value_id = 1
__compound_values = {}

__current_list_id = 1
__list_mapping = {}


def get_remote_grammar_id(grammar):
    return __grammar_ids[grammar]


def get_remote_list_id(list):
    return __list_mapping[list]


def create_remote_grammar(grammar):
    global __current_grammar_id
    new_grammar = Grammar(__current_grammar_id)
    __grammar_ids[grammar] = __current_grammar_id
    __current_grammar_id = __current_grammar_id + 1
    new_rules = [__create_remote_rule(r) for r in grammar._rules]
    new_lists = [__create_remote_list(new_grammar, l) for l in grammar._lists]
    new_grammar._rules = new_rules
    new_grammar._lists = new_lists
    if not grammar.enabled:
        new_grammar.disable()
        
    def enable(grammar):
        grammar._enabled = True
        get_engine().on_grammar_enable(grammar)
    grammar.enable = enable
    
    def disable(grammar):
        grammar._enabled = False
        get_engine().on_grammar_disable(grammar)
    grammar.disable = disable
    return new_grammar


def __create_remote_list(new_grammar, list):
    global __current_list_id
    __list_mapping[__current_list_id] = list
    copied_list = copy(list)
    copied_list._grammar = new_grammar
    copied_list.id = __current_list_id
    __current_list_id = __current_list_id + 1
    return copied_list


def __create_remote_rule(rule):
    global __current_rule_id
    __rule_mapping[__current_rule_id] = rule
    to_return = RemoteRule(rule.name, __create_remote_element(rule._element), rule._exported, __current_rule_id)
    __current_rule_id = __current_rule_id + 1
    return to_return


def __create_remote_element(element):
    copied_element = copy(element)
    __replace_compound_values(copied_element)
    return copied_element


def __replace_compound_values(e):
    global __current_value_id
    if isinstance(e, Compound):
        __compound_values[__current_value_id] = e._value
        e._value = __current_value_id
        __current_value_id = __current_value_id + 1
    if isinstance(e, Choice):
        new_choices = copy(e._choices)
        for key, value in e._choices.iteritems():
            __compound_values[__current_value_id] = value
            new_choices[key] = __current_value_id
            __current_value_id = __current_value_id + 1
        e._choices = new_choices
    for c in e.children:
        __replace_compound_values(c)


def process_recognition(rule_id, node):
    rule = __rule_mapping[rule_id]
    node.actor = rule
    for child in node.children:
        __restore_values_in_element(child.actor)
    rule.process_recognition(node)


def __restore_values_in_element(element):
    if isinstance(element, Compound):
        element._value = __compound_values[element._value]
    if isinstance(element, Choice):
        new_choices = copy(element._choices)
        for key, value in element._choices.iteritems():
            new_choices[key] = __compound_values[value]
        element._choices = new_choices
    for c in element.children:
        __restore_values_in_element(c)
    return element


class RemoteRule(Rule):

    def __init__(self, name, element, exported, id):
        Rule.__init__(self, name, element, exported=exported)
        self.id = id

    def process_recognition(self, node):
        from dragonfire.engines.backend_remote.server import ServerEngine
        from dragonfire.engines.backend_remote.server import Action
        ServerEngine.communicate((Action.RULE_PROCESS_RECOGNITION, (self.id, node)))
