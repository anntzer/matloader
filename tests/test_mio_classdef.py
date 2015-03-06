from __future__ import division, print_function, absolute_import

from os.path import join as pjoin, dirname
import sys

import numpy as np
from numpy.testing import assert_array_equal, run_module_suite

from matloader.mio import loadmat


test_data_path = pjoin(dirname(__file__), "data")
def _load_var(ver, name):
    return loadmat(pjoin(dirname(__file__), "data",
                         "testclass_{}_{}.mat".format(name, ver)))[name]


def test_load():
    for ver in ["6"]: # 7, 7.3 not supported
        simple = _load_var(ver, "simple")
        hdl = _load_var(ver, "hdl")
        array = _load_var(ver, "array")
        ref = _load_var(ver, "ref")
        assert_array_equal(ref["any_field_3"].item()["a"].item(),
                           np.array([[1.]]))
        hdl_ref = _load_var(ver, "hdl_ref")


if __name__ == "__main__":
    run_module_suite(argv=sys.argv)
