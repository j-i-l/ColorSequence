import random
import colorsys

from .helperfcts import (
        next_gr_value,
        set_vals,
        generate_vals
        )
"""
"""


class DistinctColors(object):
    r"""
    Class that allows to generate sequences of distinct colours.

    Attributes
    ==========
    n: int (default=0)
      number of distinct colours to generate. If not specified then
      :obj:`~.DistinctColors.get_colors` will return a new generator allowing
      to draw an undetermined number of values.
    h: float, tuple(float, float) (default=(0, 1))
      determine the spectrum of hues used to generate colours. If a single
      value is provided then only this hue is used.
    s: float, tuple(float, float) (default=1.0)
      determine the spectrum of saturations used to generate colours. If a
      single value is provided then only this saturation is used.
    v: float, tuple(float, float) (default=1.0)
      determine the spectrum of values used to generate colours. If a single
      value is provided then only this colour value is used.
    \**kwargs optional parameter:
      mode: str (default='gr')
        Determines how to generate the colour sequence. By default,
        ``mode='gr'``, the golden angle is exploited to create a sequence of
        values in [0, 1] that is relatively evenly distributed.

        .. todo::

          Implement a geometric approach.

      h_init: float (default=:ref:`~.DistinctColor.rd.random`)
        initial value for the hue.
      s_init: float (default=:ref:`~.DistinctColor.rd.random`)
        initial value for the saturation.
      v_init: float (default=:ref:`~.DistinctColor.rd.random`)
        initial value for the colour value.

    """
    def __init__(self, n=0, h=(0, 1), s=1.0, v=1.0, **kwargs):
        mode = kwargs.get('mode', 'gr')
        if mode == 'gr':
            self.next_gen = next_gr_value
        else:
            raise AttributeError("mode='{0}' is not implemented".format(mode))

        # useless as initiation will happen elsewhere
        # seed = kwargs.get('seed', None)
        # rd_state = kwargs.get('random_state', None)
        self.rd = random.Random()
        # if seed is not None:
        #     self.rd.seed(seed)
        # if isinstance(rd_state, tuple):
        #     self.rd.setstate(rd_state)
        # # save the initial state of the random number generator
        # self._rd_initial = self.rd.getstate()
        self.n = n
        self.h = h
        self.s = s
        self.v = v
        self.h_init_val = kwargs.get('h_init', self.rd.random())
        self.s_init_val = kwargs.get('s_init', self.rd.random())
        self.v_init_val = kwargs.get('v_init', self.rd.random())
        if self.n:
            self._h_shuffler = None
            self._s_shuffler = None
            self._v_shuffler = None
            if kwargs.get('h_shuffle', False):
                self._h_shuffler = self.rd.shuffle
            if kwargs.get('s_shuffle', False):
                self._s_shuffler = self.rd.shuffle
            if kwargs.get('v_shuffle', False):
                self._v_shuffler = self.rd.shuffle
        self._init_vals()

    def _init_vals(self):
        if self.n:
            self.h_vals = set_vals(
                    self.next_gen,
                    self.n,
                    self.h, self.h_init_val, self._h_shuffler
            )
            self.s_vals = set_vals(
                    self.next_gen,
                    self.n,
                    self.s, self.s_init_val, self._s_shuffler
            )
            self.v_vals = set_vals(
                    self.next_gen,
                    self.n,
                    self.v, self.v_init_val, self._v_shuffler
            )
        else:
            self.h_vals = generate_vals(self.next_gen, self.h, self.h_init_val)
            self.s_vals = generate_vals(self.next_gen, self.s, self.s_init_val)
            self.v_vals = generate_vals(self.next_gen, self.v, self.v_init_val)

        self._new_vals = True

    # def get_rd_initial(self):
    #     """
    #     Returns the initial state of the used random number generator.
    #     """
    #     return self._rd_initial

    def get_colors(self, ):
        """
        Returns
        =======
        RGB-colours: list, generator
          If :attr:`~.DistinctColors.n` is set, then a list of
          colors with this length is returned. If :attr:`~.DistinctColors.n` is
          unset, i.e.  ``n=0`` then a generator is returned allowing to draw
          new colours continuously.
        """
        if not self._new_vals:
            self._init_vals()
        if self.n:
            def _get_colors():
                return [
                    colorsys.hsv_to_rgb(*dc)
                    for dc in zip(self.h_vals, self.s_vals, self.v_vals)
                ]
        else:
            def _get_colors():
                while True:
                    yield colorsys.hsv_to_rgb(
                            *map(
                                next,
                                (self.h_vals, self.s_vals, self.v_vals)
                                )
                            )
        self._new_vals = False
        return _get_colors()
