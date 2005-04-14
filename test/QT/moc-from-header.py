#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

"""
Create a moc file from a header file.
"""

import TestSCons

test = TestSCons.TestSCons()

test.write('SConstruct', """
env = Environment()
""")

test.Qt_dummy_installation()

##############################################################################

aaa_exe = 'aaa' + TestSCons._exe
build_aaa_exe = test.workpath('build', aaa_exe)
moc = 'moc_aaa.cc'

test.Qt_create_SConstruct('SConstruct')

test.write('SConscript', """\
Import("env")
env.Program(target = 'aaa', source = 'aaa.cpp')
""")

test.write('aaa.cpp', r"""
#include "aaa.h"
int main() { aaa(); return 0; }
""")

test.write('aaa.h', r"""
#include "my_qobject.h"
void aaa(void) Q_OBJECT;
""")

test.run(arguments = aaa_exe)

test.up_to_date(options = '-n', arguments=aaa_exe)

test.up_to_date(options = '-n', arguments = aaa_exe)

test.write('aaa.h', r"""
/* a change */
#include "my_qobject.h"
void aaa(void) Q_OBJECT;
""")

test.not_up_to_date(options='-n', arguments = moc)

test.run(program = test.workpath(aaa_exe), stdout = 'aaa.h\n')

test.run(arguments = "build_dir=1 " + build_aaa_exe)

test.run(arguments = "build_dir=1 chdir=1 " + build_aaa_exe)

test.must_exist(test.workpath('build', moc))

test.run(arguments = "build_dir=1 chdir=1 dup=0 " +
                     test.workpath('build_dup0', aaa_exe) )

test.must_exist(['build_dup0', moc],
                ['build_dup0', aaa_exe])

test.pass_test()
