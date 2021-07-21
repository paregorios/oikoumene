.. _create_from_list:

Create a gazetteer from a list 
------------------------------

**At the command line,** use the :ref:`script_build_gazetteer` script to convert a series of character strings into a structured gazetteer. By default, the script expects a file containing a plain-text, UTF-8 encoded list of :term:`geographic strings <geographic string>`, one per line. The path to this file must be supplied using the ``--input_file`` keyword argument. The default output is a :term:`JSON` representation of the resulting gazetteer, and it is written to :py:obj:`stdout`.

.. code-block:: bash

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

.. code-block:: bash

    $ python scripts/build_gazetteer.py --output_format=txt --input_file=data/examples/ryland_names.txt
    GeographicString: Ryland
    GeographicString: Ryland Pike

By changing the values of some of the keyword arguments, you can :ref:`create_from_json` and :ref:`save_to_file`.

**Programmers** can create a gazetteer from a delimited list of strings using a two-step process:

.. py:currentmodule:: oikoumene.stringlike

- Use the :py:class:`StringParser <oikoumene.parsing.StringParser>` class to produce a :py:class:`dict` of :py:class:`GeographicName` and/or :py:class:`GeographicString` objects.
- Pass the :py:class:`dict` of objects to a :py:class:`Gazetteer <oikoumene.gazetteer.Gazetteer>` object at initialization.

.. code-block:: python

    >>> from oikoumene.parsing import StringParser
    >>> parser = StringParser()
    >>> s = "Ryland,Ryland Pike,DJ's Pizza"
    >>> objs = parser.parse(s)
    >>> isinstance(objs, dict)
    True
    >>> len(objs)
    3
    >>> objs.keys()
    dict_keys(['ryland', 'ryland-pike', 'dj-s-pizza'])
    >>> o = objs['ryland']
    >>> from oikoumene.stringlike import GeographicString
    >>> isinstance(o, GeographicString)
    True
    >>> from pprint import pprint
    >>> pprint(o._ddict(), indent=4)
    {   'attested': 'Ryland',
        'id': 'ryland',
        'object_type': 'GeographicString',
        'prior_ids': ['GeographicString.00e5f2a7-3958-44fb-8ccb-abc582936668'],
        'romanized': ['Ryland']}
    >>> from oikoumene.gazetteer import Gazetteer
    >>> g = Gazetteer(objs)
    >>> len(g.contents)
    3
    >>> g.contents.keys()
    dict_keys(['ryland', 'ryland-pike', 'dj-s-pizza'])

.. py:currentmodule:: oikoumene.parsing

Code in :file:`tests/test_parsing.py` demonstrates the flexibility of :py:class:`StringParser`. Some highlights follow here.

A :py:class:`StringParser` object can be initialized to produce :py:class:`GeographicName <oikoumene.stringlike.GeographicName>` objects instead of the default :py:class:`GeographicString <oikoumene.stringlike.GeographicString>`.

.. code-block:: python

    from oikoumene.parsing import StringParser
    from oikoumene.stringlike import GeographicName
    parser = StringParser(output_format=GeographicName)

A different delimiter character can also be designated at initialization:

.. code-block:: python

    from oikoumene.parsing import StringParser
    parser = StringParser(delimiter='\n')

By default, a :py:class:`StringParser` object assigns the parsed character string to the :py:property:`attested` property of the object it creates. Note that, since both :py:class:`GeographicName <oikoumene.stringlike.GeographicName>` and :py:class:`GeographicString <oikoumene.stringlike.GeographicString>` objects require at least one value in the :py:property:`romanized` :type:`list` and use the :ref:`python-slugify package<https://github.com/un33k/python-slugify>` to create one if only :py:property:`attested` is provided at initialization, the objects created by :py:class:`StringParser` will have both properties assigned.

.. code-block:: python

>>> from oikoumene.parsing import StringParser
>>> from pprint import pformat
>>> parser = StringParser()
>>> objs = parser.parse('穆恩敦','阿拉巴馬州')
>>> for oid, obj in objs.items():
...     print(f'{oid}: {pformat(obj._ddict(), indent=4)}')
... 
mu-en-dun: {   'attested': '穆恩敦',
    'id': 'mu-en-dun',
    'object_type': 'GeographicString',
    'prior_ids': ['GeographicString.983887a2-a8ed-4346-bcfe-ed14502980f9'],
    'romanized': ['Mu En Dun']}

.. todo::

    Demonstrate how to assign the parsed strings just to the "romanized" field.

.. todo::

    Demonstrate the creation of ad hoc attributes.

    

