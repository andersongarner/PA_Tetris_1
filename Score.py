# keeps track of combos, t spins, back to backs, and other scoring information
def get_guideline_scoring(n, level, b2b, combo=0, t_spin=False, mini_t_spin=False):
    new_score = 0
    if not mini_t_spin:
        if n == 1:
            combo += 1
            new_score += 100 * (level + 1)
            b2b = False
        if n == 2:
            combo += 1
            new_score += 300 * (level + 1)
            b2b = False
        if n == 3:
            combo += 1
            new_score += 500 * (level + 1)
            b2b = False
        if n == 4:
            combo += 1
            new_score += 800 * (level + 1)
            b2b = True
    if mini_t_spin:
        if n == 0:
            combo += 1
            new_score += 100 * (level + 1)
            b2b = False
        if n == 1:
            combo += 1
            new_score += 200 * (level + 1)
            b2b = True
        if n == 2:
            combo += 1
            new_score += 400 * (level + 1)
            b2b = True
    elif t_spin:
        if n == 0:
            combo += 1
            new_score += 400 * (level + 1)
            b2b = False
        if n == 1:
            combo += 1
            new_score += 800 * (level + 1)
            b2b = True
        if n == 2:
            combo += 1
            new_score += 1200 * (level + 1)
            b2b = True
        if n == 3:
            combo += 1
            new_score += 1600 * (level + 1)
            b2b = True

    if b2b:
        new_score = int(new_score * 1.5)

    if new_score != 0:
        new_score += combo * 50 * (level+1)

    return [new_score, combo, b2b]
