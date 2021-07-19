# oikoumene: use, create, and share gazetteers for humanities projects

> *οἰκουμένη (oikouméne),* noun: the inhabited world


## System Requirements

Tested on Python 3.9.6 under OSX Mojave. Your mileage may vary. Pull requests fixing problems you find on other platforms are always welcome.

## Installation

With pip from pypi:

```bash
pip install oikoumene
```

## Quick Start

*Oikoumene* knows about places and spaces (Places), toponyms (GeographicNames), and strings that refer to named places and spaces without being toponyms in their own right (e.g., "landing strip"; GeographicString). It also knows how to combine groups of these objects into a "Gazetteer," which you should think of as a big pile of name and/or place information with associated unique identifiers for each.

*Oikoumene* supports gazetteer building on the command line and in code.

## Build from a list of geographic strings

On the command line:

```bash
> more data/examples/ryland_names.txt 
Ryland
Ryland Pike
> python scripts/build_gazetteer.py --input_file=data/examples/ryland_names.txt --input_format=txt --output_format=txt
GeographicString: Ryland
GeographicString: Ryland Pike
```

You can omit the ```--output_format``` argument for the ```build_gazetteer.py``` in order to let it default to "json". This will give you a more complete view of the structure of the gazetteer and how the various content elements are elaborated:

```bash
python scripts/build_gazetteer.py --input_file=data/examples/ryland_names.txt --input_format=txt
{
    "contents": {
        "ryland": {
            "attested": "Ryland",
            "id": "ryland",
            "object_type": "GeographicString",
            "prior_ids": [
                "GeographicString.5d5170c2-4ba5-453f-ab65-4a59f697f2d1"
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
                "GeographicString.779b7f67-ecdb-4ad7-9f42-ae5c34f2c1ff"
            ],
            "romanized": [
                "Ryland Pike"
            ]
        }
    },
    "object_type": "Gazetteer"
}
```

The ```--output-file``` argument can be used to instruct the script to save results directly to file:

```bash
> python scripts/build_gazetteer.py --input_file=data/examples/ryland_names.txt --input_format=txt --output_format=txt --output_file=~/scratch/foo.txt
> more ~/scratch/foo.txt 
GeographicString: Ryland
GeographicString: Ryland Pike
```

Here's how to do the same things in the python interpreter:

```python
>>> from pathlib import Path
>>> inpath = Path('data/examples/ryland_names.txt')
>>> from oikoumene.parsing import StringParser
>>> parser = StringParser(delimiter='\n')
>>> data = parser.parse(inpath)
>>> type(data)
<class 'dict'>
>>> from pprint import pprint
>>> pprint(data, indent=4)
{   'ryland': <oikoumene.stringlike.GeographicString object at 0x109fba2b0>,
    'ryland-pike': <oikoumene.stringlike.GeographicString object at 0x109f9fee0>}
>>> from oikoumene.gazetteer import Gazetteer
>>> gaz = Gazetteer(data)
>>> pprint(gaz.contents, indent=4)
{   'ryland': <oikoumene.stringlike.GeographicString object at 0x109fba2b0>,
    'ryland-pike': <oikoumene.stringlike.GeographicString object at 0x109f9fee0>}
>>> print(gaz)
GeographicString: Ryland
GeographicString: Ryland Pike
>>> print(gaz.json())
{
    "contents": {
        "ryland": {
            "attested": "Ryland",
            "id": "ryland",
            "object_type": "GeographicString",
            "prior_ids": [
                "GeographicString.7ad52c7b-79d0-474f-a66a-bbb9aa776550"
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
                "GeographicString.25faa2af-9a8a-4599-b615-ac3e3461593d"
            ],
            "romanized": [
                "Ryland Pike"
            ]
        }
    },
    "object_type": "Gazetteer"
}
```
