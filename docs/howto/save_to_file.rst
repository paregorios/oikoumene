.. _save_to_file:

Save a gazetteer to a file 
--------------------------

When using the :ref:`script_build_gazetteer` script at the command line to create a gazetteer, the results can be saved to a file either by using your shell's IO redirection capabilities, e.g., 

.. code-block:: bash

    $ python scripts/build_gazetteer.py --output_format=txt --input_file=data/examples/ryland_names.txt > ~/scratch/foo.txt
    $ cat ~/scratch/foo.txt
    GeographicString: Ryland
    GeographicString: Ryland Pike

You can also make use of the script's ``--output_file`` keyword argument:

.. code-block:: bash

    $ python scripts/build_gazetteer.py --output_format=txt --input_file=data/examples/ryland_names.txt --output_file=~/scratch/bar.txt
    $ cat ~/scratch/bar.txt 
    GeographicString: Ryland
    GeographicString: Ryland Pike
