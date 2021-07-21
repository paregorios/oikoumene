Create gazetteers
^^^^^^^^^^^^^^^^^

Programmers can create a gazetteer from a delimited list of strings using a two-step process:

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

    