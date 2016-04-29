""" Testing

"""
from __future__ import division, print_function, absolute_import

import sys

from io import BytesIO
cStringIO = BytesIO

import numpy as np

from nose.tools import assert_true, assert_false, \
     assert_equal, assert_raises

from numpy.testing import assert_array_equal, assert_array_almost_equal, \
     run_module_suite

import matloader.byteordercodes as boc
import matloader.streams as streams
from matloader.mio5 import MatFile5Reader
import matloader.mio5_params as mio5p
import matloader.mio5_utils as m5u
from matloader.six import u


def _make_tag(base_dt, val, mdtype, sde=False):
    ''' Makes a simple matlab tag, full or sde '''
    base_dt = np.dtype(base_dt)
    bo = boc.to_numpy_code(base_dt.byteorder)
    byte_count = base_dt.itemsize
    if not sde:
        udt = bo + 'u4'
        padding = (-byte_count) % 8
        all_dt = [('mdtype', udt),
                  ('byte_count', udt),
                  ('val', base_dt)]
        if padding:
            all_dt.append(('padding', 'u1', padding))
    else:  # is sde
        udt = bo + 'u2'
        padding = 4 - byte_count
        if bo == '<':  # little endian
            all_dt = [('mdtype', udt),
                      ('byte_count', udt),
                      ('val', base_dt)]
        else:  # big endian
            all_dt = [('byte_count', udt),
                      ('mdtype', udt),
                      ('val', base_dt)]
        if padding:
            all_dt.append(('padding', 'u1', padding))
    tag = np.zeros((1,), dtype=all_dt)
    tag['mdtype'] = mdtype
    tag['byte_count'] = byte_count
    tag['val'] = val
    return tag


def _write_stream(stream, *strings):
    stream.truncate(0)
    stream.seek(0)
    for s in strings:
        stream.write(s)
    stream.seek(0)


def _make_readerlike(stream, byte_order=boc.native_code):
    class R(object):
        pass
    r = object.__new__(MatFile5Reader)
    r._stream = stream
    r._endian = byte_order
    r._struct_as_record = True
    r._chars_as_strings = False
    r._mat_dtype = False
    r._squeeze_me = False
    return r


def test_read_tag():
    # mainly to test errors
    # make reader-like thing
    str_io = BytesIO()
    r = _make_readerlike(str_io)
    with assert_raises(StopIteration):
        next(r._read_iter())
    # bad SDE
    tag = _make_tag('i4', 1, mio5p.miINT32, sde=True)
    tag['byte_count'] = 5
    _write_stream(str_io, tag.tostring())
    with assert_raises(ValueError):
        next(r._read_iter())


def test_read_stream():
    tag = _make_tag('i4', 1, mio5p.miINT32, sde=True)
    tag_str = tag.tostring()
    str_io = cStringIO(tag_str)
    st = streams.make_stream(str_io)
    s = streams._readinto(st, tag.itemsize)
    yield assert_equal, s, tag.tostring()


def test_read_numeric():
    # make reader-like thing
    str_io = cStringIO()
    r = _make_readerlike(str_io)
    # check simplest of tags
    for base_dt, val, mdtype in (('u2', 30, mio5p.miUINT16),
                                 ('i4', 1, mio5p.miINT32),
                                 ('i2', -1, mio5p.miINT16)):
        for byte_code in ('<', '>'):
            r._endian = byte_code
            for sde_f in (False, True):
                dt = np.dtype(base_dt).newbyteorder(byte_code)
                a = _make_tag(dt, val, mdtype, sde_f)
                a_str = a.tostring()
                _write_stream(str_io, a_str)
                el = next(r._read_iter())
                yield assert_equal, el, val
                # two sequential reads
                _write_stream(str_io, a_str, a_str)
                el = next(r._read_iter())
                yield assert_equal, el, val
                el = next(r._read_iter())
                yield assert_equal, el, val


def test_read_numeric_writeable():
    # make reader-like thing
    str_io = cStringIO()
    r = _make_readerlike(str_io, '<')
    dt = np.dtype('<u2')
    a = _make_tag(dt, 30, mio5p.miUINT16, sde=False)
    a_str = a.tostring()
    _write_stream(str_io, a_str)
    el = next(r._read_iter())
    yield assert_true, el.flags.writeable


# Removed test_byteswap since byteswap_u4 has been removed.
# Removed test_zero_byte_string since read_char has been removed.


if __name__ == "__main__":
    run_module_suite(argv=sys.argv)
