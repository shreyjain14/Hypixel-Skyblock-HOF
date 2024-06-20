def db_response(vals):
    res = []

    for val in vals:

        if val[1] == 'skyblock_xp':
            res.append([val[0], val[1], val[9], val[2], val[3], '{0:,}'.format(val[4]/100),
                        val[5], '{0:,}'.format(val[6]/100), val[7], '{0:,}'.format(val[8]/100)])
        else:
            res.append([val[0], val[1], val[9], val[2], val[3], '{0:,}'.format(val[4]),
                        val[5], '{0:,}'.format(val[6]), val[7], '{0:,}'.format(val[8])])

    return res
