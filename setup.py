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

# Find all of the tutorial notebooks in the tutorials_src path
tutorials_src = 'tutorial/notebooks/'
tutorials_dest = os.path.join(jupyter_dest, 'HLS-Tutorial')
tutorials = [os.path.join(tutorials_src, f)
             for f in os.listdir(tutorials_src)]

# Find all of the tutorial notebook pictures in the pictures_src path
pictures_src = os.path.join(tutorials_src, 'pictures')
pictures_dest = os.path.join(tutorials_dest, 'pictures')
pictures = [os.path.join(pictures_src, f) for f in os.listdir(pictures_src)]

# Find all of the stream notebooks in the stream_src path
stream_src = 'pynqhls/stream/notebooks/'
stream_dest = os.path.join(jupyter_dest, 'HLS-Stream')
stream = [os.path.join(stream_src, f)
             for f in os.listdir(stream_src)]

# Find all of the tutorial notebook pictures in the pictures_src path
stream_pictures_src = os.path.join(stream_src, 'pictures')
stream_pictures_dest = os.path.join(stream_dest, 'pictures')
stream_pictures = [os.path.join(stream_pictures_src, f) for f in os.listdir(stream_pictures_src)]

# Find all of the io notebooks in the io_src path
io_src = 'pynqhls/io/notebooks/'
io_dest = os.path.join(jupyter_dest, 'HLS-IO')
io = [os.path.join(io_src, f)
             for f in os.listdir(io_src)]

tutorials.remove(pictures_src)
stream.remove(stream_pictures_src)

setup(name='pynq-hls',
      version='0.1',
      description="A simple package describing how to create a PYNQ\
            bitstream with HLS cores",
      author='Dustin Richmond',
      author_email='drichmond@eng.ucsd.edu',
      url='https://github.com/drichmond/PYNQ-HLS/',
      license='BSD-3',
      data_files = [(tutorials_dest, tutorials),
                    (pictures_dest, pictures),
                    (stream_dest, stream),
                    (io_dest, io),
                    (stream_pictures_dest, stream_pictures)],
      packages=['pynqhls', 'pynqhls.stream', 'pynqhls.io'],
      package_data={'':['*.bit', '*.tcl']},
      install_requires=['pynq'],
      dependency_links=['http://github.com/xilinx/PYNQ.git@v2.0#egg=pynq'],
)
