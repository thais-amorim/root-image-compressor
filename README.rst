Root Image Compressor
========

|MIT license|

.. |MIT license| image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://lbesson.mit-license.org/

Install dependencies
--------------------

$ pip3 install -r requirements.txt

Running
-------
To apply Huffman:

$ python main.py -cm huffman images\benchmark.bmp

$ python main.py -dm huffman images\benchmark.bmp.pdi


To apply Huffman + scale:

$ python main.py -cm huffman_with_scale images\benchmark.bmp

$ python main.py -dm huffman_with_scale images\benchmark_small.bmp.pdi


Features
--------

Implemented compression methods:

- Huffman
- Run-length
- Scale + Huffman

Contribute
----------

- Issue Tracker: https://github.com/thasmarinho/root-image-compressor/issues
- Source Code: https://github.com/thasmarinho/root-image-compressor

License
-------

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
