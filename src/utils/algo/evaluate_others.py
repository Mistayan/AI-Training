def smart_eval(our_bot, ref_bot):
    """ Evaluate the fear_factor for each bot"""
    # find out the max factor:
    max_factor = our_bot.DIST_PENALTY + our_bot.LIFE_PENALTY + our_bot.AMMO_PENALTY
    # penalize if bot is far away:
    # We may encounter random events that could harm us on the way
    # [ DIST >>]
    print("#" * 12, "Eval distance")

    dist_factor = our_bot.DIST_PENALTY / (ref_bot.distance /
                                          our_bot.MAP_MAX_DISTANCE + 1)

    # penalize if bot has high life values. Strong target means HIGH risks
    # [LIFE >>]
    life_factor = our_bot.LIFE_PENALTY / (ref_bot.vie / 100)

    # penalize if bot has low ammo
    # [<< AMMO]
    ammo_factor = our_bot.AMMO_PENALTY * (ref_bot.ammo / 100)
    print(f"Eval complete for {ref_bot.name} => \n",
          f"df({ref_bot.distance}) = {dist_factor:.2f}\n",
          f"lf({ref_bot.vie}) = {life_factor:.2f}\n",
          f"af({ref_bot.ammo}) = {ammo_factor:2f}")
    # ref_bot.__set_score(fear_factor)
    return (dist_factor + life_factor + ammo_factor) / (max_factor * 3)
