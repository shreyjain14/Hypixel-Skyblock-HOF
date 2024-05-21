def db_response(vals):
    res = []

    for val in vals:

        if val[1] == 'skyblock_xp':
            res.append([val[0], val[1], val[2], val[3], val[4], '{0:,}'.format(val[5]/100),
                        val[6], '{0:,}'.format(val[7]/100), val[8], '{0:,}'.format(val[9]/100)])
        else:
            res.append([val[0], val[1], val[2], val[3], val[4], '{0:,}'.format(val[5]),
                        val[6], '{0:,}'.format(val[7]), val[8], '{0:,}'.format(val[9])])

    return res
