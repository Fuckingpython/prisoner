#!/usr/bin/env python

# Coconut Header: --------------------------------------------------------------

from __future__ import with_statement, print_function, absolute_import, unicode_literals, division
try:
    from future_builtins import *
except ImportError:
    pass

import sys as _coconut_sys
import os.path as _coconut_os_path
_coconut_sys.path.append(_coconut_os_path.dirname(_coconut_os_path.abspath(__file__)))
import __coconut__

reduce = __coconut__.reduce
itemgetter = __coconut__.itemgetter
attrgetter = __coconut__.attrgetter
methodcaller = __coconut__.methodcaller
takewhile = __coconut__.takewhile
dropwhile = __coconut__.dropwhile
tee = __coconut__.tee
recursive = __coconut__.recursive

# Compiled Coconut: ------------------------------------------------------------

# IMPORTS:

from .dilemma import random, pd_bot, simulate, winnings, decide

# BOTS:

def cooperate(self_hist=None, opp_hist=None, opp_bot=None): return True
cooperate_bot = pd_bot(cooperate)

def defect(self_hist=None, opp_hist=None, opp_bot=None): return False
defect_bot = pd_bot(defect)

def coin_flip(self_hist=None, opp_hist=None, opp_bot=None):
    return __coconut__.pipe(random.getrandbits(1), bool)
coin_flip_bot = pd_bot(coin_flip)

def tit_for_tat(self_hist, opp_hist, opp_bot=None):
    if opp_hist:
        return opp_hist[-1]
    else:
        return None
tit_for_tat_bot = pd_bot(tit_for_tat) + cooperate_bot

def nice_tft(self_hist, opp_hist, opp_bot=None):
    if not opp_hist or opp_hist[-1] or random.random() < .05:
        return cooperate()
    else:
        return defect()
nice_tft_bot = pd_bot(nice_tft)

def delayed_tft(self_hist, opp_hist, opp_bot=None):
    if opp_hist:
        return random.choice(opp_hist)
    else:
        return None
delayed_tft_bot = pd_bot(delayed_tft) + cooperate_bot

def punisher(self_hist, opp_hist, opp_bot=None):
    if opp_hist and not all(opp_hist):
        return defect()
    else:
        return None
punisher_bot = pd_bot(punisher) + cooperate_bot

def switcher(self_hist, opp_hist, opp_bot=None):
    if not opp_hist or not self_hist:
        return None
    elif self_hist[-1] == opp_hist[-1]:
        return cooperate()
    else:
        return defect()
mean_switcher_bot = pd_bot(switcher)
nice_switcher_bot = mean_switcher_bot + cooperate_bot

def exploiter(self_hist, opp_hist, opp_bot):
    if next(__coconut__.islice(simulate(defect_bot, self_hist, opp_bot, opp_hist, False), 1, (1) + 1))[1]:
        return defect()
    elif not next(__coconut__.islice(simulate(cooperate_bot, self_hist, opp_bot, opp_hist, True), 1, (1) + 1))[1]:
        return defect()
    else:
        return None
exploit_or_tft_bot = pd_bot(exploiter) + tit_for_tat_bot
exploit_or_switch_bot = pd_bot(exploiter) + nice_switcher_bot
exploit_or_punish_bot = pd_bot(exploiter) + punisher_bot
exploit_or_nice_tft_bot = pd_bot(exploiter) + nice_tft_bot
exploit_or_delayed_tft_bot = pd_bot(exploiter) + delayed_tft_bot

def mirror(self_bot, self_hist, opp_hist, opp_bot):
    return opp_bot(opp_hist, self_hist, self_bot)

def mirror_or_cooperate(self_hist, opp_hist, opp_bot):
    return mirror(mirror_bot, self_hist, opp_hist, opp_bot)
mirror_bot = pd_bot(mirror_or_cooperate) + cooperate_bot

justice_mirror = __coconut__.partial(mirror, cooperate_bot)
justice_mirror_bot = pd_bot(justice_mirror)

def mirror_or_tft(self_hist, opp_hist, opp_bot):
    return mirror(mirror_or_tft_bot, self_hist, opp_hist, opp_bot)
mirror_or_tft_bot = pd_bot(mirror_or_tft) + tit_for_tat_bot
exploit_or_mirror_bot = pd_bot(exploiter) + mirror_or_tft_bot

def tft_or_mirror(self_hist, opp_hist, opp_bot):
    return mirror(tft_or_mirror_bot, self_hist, opp_hist, opp_bot)
tft_or_mirror_bot = pd_bot(tit_for_tat) + pd_bot(tft_or_mirror) + cooperate_bot

def switch_or_mirror(self_hist, opp_hist, opp_bot):
    return mirror(switch_or_mirror_bot, self_hist, opp_hist, opp_bot)
switch_or_mirror_bot = pd_bot(switcher) + pd_bot(switch_or_mirror) + cooperate_bot

def punish_or_mirror(self_hist, opp_hist, opp_bot):
    return mirror(punish_or_mirror_bot, self_hist, opp_hist, opp_bot)
punish_or_mirror_bot = pd_bot(punisher) + pd_bot(punish_or_mirror) + cooperate_bot

def nice_tft_or_mirror(self_hist, opp_hist, opp_bot):
    return mirror(nice_tft_or_mirror_bot, self_hist, opp_hist, opp_bot)
nice_tft_or_mirror_bot = pd_bot(nice_tft) + pd_bot(nice_tft_or_mirror) + cooperate_bot

def delayed_tft_or_mirror(self_hist, opp_hist, opp_bot):
    return mirror(delayed_tft_or_mirror_bot, self_hist, opp_hist, opp_bot)
delayed_tft_or_mirror_bot = pd_bot(delayed_tft) + pd_bot(delayed_tft_or_mirror) + cooperate_bot

def lookahead_or_tft(self_hist, opp_hist, opp_bot):
    c_response, d_response = simulate(lookahead_or_tft_bot, self_hist, opp_bot, opp_hist)
    if next(__coconut__.islice(d_response, 1, (1) + 1)):
        return defect()
    elif next(__coconut__.islice(c_response, 1, (1) + 1)):
        return cooperate()
    else:
        return defect()
lookahead_or_tft_bot = pd_bot(lookahead_or_tft) + tit_for_tat_bot

def simulate_or_tft(self_hist, opp_hist, opp_bot):
    c_simulation, d_simulation = winnings(tft_or_mirror_bot, self_hist, opp_bot, opp_hist)
    c_scores = next(__coconut__.islice(c_simulation, 3, (3) + 1))
    d_scores = next(__coconut__.islice(d_simulation, 3, (3) + 1))
    return decide(c_scores, d_scores)
simulate_or_tft_bot = pd_bot(simulate_or_tft) + tft_or_mirror_bot

def simulate_or_mirror(self_hist, opp_hist, opp_bot):
    c_simulation, d_simulation = winnings(mirror_or_tft_bot, self_hist, opp_bot, opp_hist)
    c_scores = next(__coconut__.islice(c_simulation, 3, (3) + 1))
    d_scores = next(__coconut__.islice(d_simulation, 3, (3) + 1))
    return decide(c_scores, d_scores)
simulate_or_mirror_bot = pd_bot(simulate_or_mirror) + mirror_or_tft_bot
