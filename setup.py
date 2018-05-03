###############################################################################
# Copyright (c) 2016, The Regents of the University of California All
# rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
# 
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
# 
#     * Neither the name of The Regents of the University of California
#       nor the names of its contributors may be used to endorse or
#       promote products derived from this software without specific
#       prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL REGENTS OF THE
# UNIVERSITY OF CALIFORNIA BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.
###############################################################################
from setuptools import setup

import os

jupyter_dest = '/home/xilinx/jupyter_notebooks'
tutorials = ["stream", "sharedmem", "io"]

# Find all of the tutorial notebooks in the tutorials_base path
tutorials_base = 'tutorial/notebooks/'
tutorials_dest_base = os.path.join(jupyter_dest, 'HLS-Tutorial')

data_files = []
for tut in tutorials:
    nbsource = os.path.join(tutorials_base, tut)
    notebooks = [os.path.join(nbsource, f) for f in os.listdir(nbsource)]
    nbdest = os.path.join(tutorials_dest_base, tut)
    picsource = os.path.join(nbsource, 'pictures')
    pictures = [os.path.join(picsource, f) for f in os.listdir(picsource)]
    picdest = os.path.join(nbdest, 'pictures')
    notebooks.remove(picsource)
    data_files.append((nbdest, notebooks))
    data_files.append((picdest, pictures))

demo_base = 'pynqhls/'
demo_dest_base = os.path.join(jupyter_dest, 'HLS-Demo')

for tut in tutorials:
    nbsource = os.path.join(demo_base, tut, 'notebooks')
    notebooks = [os.path.join(nbsource, f) for f in os.listdir(nbsource)]
    nbdest = os.path.join(demo_dest_base, tut)
    picsource = os.path.join(nbsource, 'pictures')
    pictures = [os.path.join(picsource, f) for f in os.listdir(picsource)]
    picdest = os.path.join(nbdest, 'pictures')
    notebooks.remove(picsource)
    data_files.append((nbdest, notebooks))
    data_files.append((picdest, pictures))

setup(name='pynq-hls',
      version='0.1',
      description="A simple package describing how to create a PYNQ\
            bitstream with HLS cores",
      author='Dustin Richmond',
      author_email='drichmond@eng.ucsd.edu',
      url='https://github.com/drichmond/PYNQ-HLS/',
      license='BSD-3',
      data_files = data_files,
      packages=['pynqhls', 'pynqhls.stream', 'pynqhls.io', 'pynqhls.sharedmem'],
      package_data={'':['*.bit', '*.tcl']},
      install_requires=['pynq'],
      dependency_links=['http://github.com/xilinx/PYNQ.git@v2.0#egg=pynq'],
)
