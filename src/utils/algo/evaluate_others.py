import logging


def eval_fear_factor(our_bot: dict, ref_bot: dict):
    """ Evaluate the fear_factor for each bot"""
    # extract values
    df, mmd, ld, ad = our_bot['DIST_PENALTY'], our_bot['MAP_MAX_DISTANCE'], \
        our_bot['LIFE_PENALTY'], our_bot['AMMO_PENALTY']
    dist, ammo, life = ref_bot['distance'], ref_bot['ammo'], ref_bot['life']
    # find out the max factor:
    # penalize if bot is far away:
    # We may encounter random events that could harm us on the way
    # [ DIST >>]
    dist_factor = df * (dist / mmd)

    # penalize if bot has high life values. Strong target means HIGH risks
    # [LIFE >>]
    life_factor = ld * (life / 100)

    # penalize if bot has low ammo
    # [<< AMMO]
    ammo_factor = ad * (ammo / 100)
    max_factor = ((df / mmd) * (ld + ad))
    fear_factor = (dist_factor * ((life_factor + ammo_factor) * 2))
    logging.log(logging.DEBUG, f"""Eval complete =>
          max  fact : {max_factor:.5f}
          dist fact : ({dist}) = {dist_factor:.2f}
          life fact : ({life}) = {life_factor:.2f}
          ammo fact : ({ammo}) = {ammo_factor:.2f}
          fear_factor : {fear_factor:.3f}
          potential accomodation : { fear_factor * max_factor}""")
    return min(fear_factor, 1)
