*******
Scripts
*******

.. _script_build_gazetteer:

build_gazetteer.py
------------------

.. code-block:: bash

    $ python scripts/build_gazetteer.py -h
    usage: build_gazetteer.py [-h] [-l LOGLEVEL] [-v] [-w] [-i INPUT_FILE] [-if INPUT_FORMAT] [-o OUTPUT_FILE] [-of OUTPUT_FORMAT]

    Build a gazetteer from basic data.

    optional arguments:
    -h, --help            show this help message and exit
    -l LOGLEVEL, --loglevel LOGLEVEL
                            desired logging level (case-insensitive string: DEBUG, INFO, WARNING, or ERROR (default: NOTSET)
    -v, --verbose         verbose output (logging level == INFO) (default: False)
    -w, --veryverbose     very verbose output (logging level == DEBUG) (default: False)
    -i INPUT_FILE, --input_file INPUT_FILE
                            path to input file (default: )
    -if INPUT_FORMAT, --input_format INPUT_FORMAT
                            input file format (default: json)
    -o OUTPUT_FILE, --output_file OUTPUT_FILE
                            path to output file (default: )
    -of OUTPUT_FORMAT, --output_format OUTPUT_FORMAT
                            output file format (default: json)

For usage examples, see :ref:`create_from_list`.
