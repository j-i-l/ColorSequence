from itertools import cycle


def next_gr_value(initial_value):
    """
    Generator providing then next value in [0,1].

    This approach exploits the fact that successively adding the golden ratio
    followed by a modulo 1 operation leads to evenly distributed values in the
    interval [0, 1].

    Parameters
    ==========
    val: float
      A value in [0, 1] to which the golden ratio will be added.

    """
    g_ratio = (1 + 5 ** 0.5) / 2
    old = initial_value
    while True:
        old = (old + g_ratio) % 1
        yield old


def _get_distinct(distincts, n, next_generator, shuffler=None):
    if len(distincts) < n:
        distincts.append(next(next_generator))
        return _get_distinct(distincts, n, next_generator, shuffler)
    else:
        if shuffler is not None:
            shuffler(distincts)
        return distincts


def set_vals(next_generator, n, param, init_val, shuffler):
    """
    Set a defined number of values with the option to shuffle the order.


    Parameters
    ==========
    n: int
      number of different colours to generate.
    """
    if isinstance(param, (list, tuple)):
        start = param[0]
        diff = param[1] - start
        next_g = next_generator(init_val)
        _vals = map(
                lambda x: start + x * diff,
                _get_distinct([], n, next_g, shuffler)
                    )
        vals = iter(_vals)
    else:
        vals = cycle([param])
    return vals


def generate_vals(next_generator, value_range, init_val):
    """
    Generator to yield values within a permitted range.

    Parameters
    ==========
    next_generator: generator
      must yield a value within [0, 1].
    value_range: tuple, float
      specify the range within which values will be generated. If a single
      value is provided then only this value will be returned by the generator.
    init_val: float
      The first value to return. It must lay within the value_range provided.
      If value_range is a single value, then this parameter is ignored.
    """
    if isinstance(value_range, (tuple, list)):
        start = min(value_range)
        stop = max(value_range)
        assert start <= init_val <= stop
        next_g = next_generator(init_val)
        diff = start - start
        def to_yield(): return start + next(next_g) * diff
    elif isinstance(value_range, (float, int)):
        def to_yield(): return value_range
    else:
        raise ValueError('value_range must either be a tuple or a float')
    while True:
        yield to_yield()
