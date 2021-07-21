.. _create_from_list:

Create a gazetteer from a list 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At the command line, use the :ref:`script_build_gazetteer` script to convert a series of character strings into a structured gazetteer. By default, the script expects a file containing a plain-text, UTF-8 encoded list of :term:`geographic strings <geographic string>`, one per line. The path to this file must be supplied using the ``--input_file`` keyword argument. The default output is a :term:`JSON` representation of the resulting gazetteer, and it is written to :py:obj:`stdout`.

.. code-block:: console

    $ cat data/examples/ryland_names.txt 
    Ryland
    Ryland Pike
    $ python scripts/build_gazetteer.py --input_file=data/examples/ryland_names.txt 
    {
        "contents": {
            "ryland": {
                "attested": "Ryland",
                "id": "ryland",
                "object_type": "GeographicString",
                "prior_ids": [
                    "GeographicString.c1b94486-2c4f-4264-9347-3d1e15aca11c"
                ],
                "romanized": [
                    "Ryland"
                ]
            },
            "ryland-pike": {
                "attested": "Ryland Pike",
                "id": "ryland-pike",
                "object_type": "GeographicString",
                "prior_ids": [
                    "GeographicString.bcac8611-9196-404c-be84-74f0061f3cf8"
                ],
                "romanized": [
                    "Ryland Pike"
                ]
            }
        },
        "object_type": "Gazetteer"
    }

The ``--output_format`` keyword argument can be set to "txt" to view a simple summary of the strings in the resulting gazetteer, instead of the JSON format:

.. code-block:: console

    $ python scripts/build_gazetteer.py --output_format=txt --input_file=data/examples/ryland_names.txt
    GeographicString: Ryland
    GeographicString: Ryland Pike

By changing the values of some of the keyword arguments, you can :ref:`create_from_json` and :ref:`save_to_file`.
