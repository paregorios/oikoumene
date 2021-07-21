********
Glossary
********


.. glossary::

    ad hoc attributes
        Data attributes (key:value pairs) that you add to an event, geographic name, geographic string, or place when it is created. *Oikoumene* does not provide any special functions or indexing for ad hoc attributes, but they are automatically read from, and written to, the default JSON serialization used by the package.
        
    event
        A change or experience that occurs at discrete moments or durations in time and space. 

        *Oikoumene* models events using the :py:class:`Event <oikoumene.event.Event>` class.

    gazetteer
        A gazetteer is a geographical dictionary or directory, indexing places, toponyms, locations, and associated information. Gazetteers often serve as the focus, or as a critical component, of digital humanities publications and projects.

        See also: :ref:`conceptual_discussion`.
        
        See further: Berman, Merrick Lex, et al., editors, *Placing Names: Enriching and Integrating Gazetteers.* Indiana University Press, 2016, http://www.worldcat.org/oclc/994713636, especially the "Introduction" and "Section I: What is a Gazetteer?", pp. 1-66.

        *Oikoumene* models gazetteers using the :py:class:`Gazetteer <oikoumene.gazetteer.Gazetteer>` class.

    geographic name
        By "geographic name", we mean a :term:`string` that constitutes a toponym, placename, region/area name, and the like. If a modern, English-speaking cartographer would title-capitalize the name on a map or in a gazetteer, then it is probably a "geographic name". 
        
        See also: :term:`geographic string`.

        *Oikoumene* models geographic names using the :py:class:`GeographicName <oikoumene.stringlike.GeographicName>` class.
        
    geographic string
        By "geographic string", we mean any word, phrase, or other sequence of words that corresponds to, mentions, evokes, or describes a place, region, area, or other geographic or spatial feature, but that does not constitute a :term:`geographic name` in the cultural, scholarly, or analytic context.

        *Oikoumene* models geographic strings using the :py:class:`GeographicString <oikoumene.stringlike.GeographicString>` class.

    JavaScript Object Notation (JSON)
        A lightweight data-interchange format. 
        
        See further: https://www.json.org/json-en.html.

    JSON
        See :term:`JavaScript Object Notation (JSON)`.

    name
        See :term:`geographic name`.

    place
        *Oikoumene* defines places in the same way that `the Pleiades gazetteer of ancient places <https://pleiades.stoa.org>`_ does:
        
            [Places] are conceptual entities: the term "place" applies to any locus of human attention, material or intellectual, in a real-world geographic context. A settlement mentioned in [a] ... text is a place, whether or not it can now be located; an archaeological site is a place; a modern city ... is a place. Basically, any spatial feature ... that a human being has noticed and discussed as such between the past and the present is a place.

            -- Gillies, Sean et al., "Conceptual Overview" in *Pleiades*, https://pleiades.stoa.org/help/conceptual-overview.

        *Oikoumene* models places using the :py:class:`Place <oikoumene.place.Place>` class.

    placename
        See :term:`geographic name`.

    string
        In computing, a "string" is a sequence of characters from a writing system.
        
        See further: https://en.wikipedia.org/wiki/String_(computer_science).

    toponym
        See :term:`geographic name`.
