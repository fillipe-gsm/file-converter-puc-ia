==============
File Converter
==============

Converts files from CSV to JSON formats and vice-versa.

This is meant to be used as the final project for the Python course from the Artificial Intelligence program at PUC Minas.

It has nothing groundbreaking, so you can safely ignore it. In any case, if you managed to get here, feel free to check my other (hopefully) more useful projects:

- `Python TSP <https://github.com/fillipe-gsm/python-tsp>`_: a TSP solver;
- `Python Kanban <https://github.com/fillipe-gsm/python-kanban>`_: a Kanban board for the command line.

Installation
============

.. code:: bash

  pip install file-converter-fgsm

This assumes you are inside a virtual environment. If you wish to install it globally on the system (which I do not recommend for this class project), add ``sudo`` at the beginning.

Usage
=====

Once installed, a ``file_converter`` command becomes available. Type

.. code:: bash

  file_converter --help

to get further help.

Examples
========

Converting a single file
------------------------

Suppose you have a file ``sample_file.csv`` in the current directory with the contents

.. code:: csv

  header1,header2,header3
  1,"a",1.5
  2,"b",3.2

To convert it into a ``json`` format, run

.. code:: bash

  file_converter --conversion=csv2json --input_path=./sample_file.csv

and then you should have a ``sample_file.json`` in the same directory with the contents:

.. code:: json

  [
      {
          "header1": 1,
          "header2": "\"a\"",
          "header3": 1.5
      },
      {
          "header1": 2,
          "header2": "\"b\"",
          "header3": 3.2
      }
  ]


Notice how the quotes have been escaped.

The previous command is short for

.. code:: bash

  file_converter --conversion=csv2json --input_path=./sample_file.csv --output_path=. --separator=, --prefix=""

Experiment running again but with a different ``--output_path``.

The command supports the other way for the conversion as well. To test that, let us convert the recently converted ``json`` file but prefixing the file name with a ``new_``:

.. code:: bash

  file_converter --conversion=json2csv --input_path=./sample_file.json --prefix="new_"

Notice the ``csv2json`` became ``json2csv`` in the ``--command`` attribute. Also, we should have a ``new_sample_file.csv`` with the same contents at the beginning.

Converting all files in a folder
--------------------------------

If instead of a single file path you pass a folder in the ``--input_path`` parameter, the command will attempt to convert all files inside of it. Notice they all should have the same separator.

Experiment passing the current directory like


.. code:: bash

  file_converter --conversion=csv2json --input_path=. --prefix="from_folder_"

If you followed the previous example, you should have two new ``json`` files starting with ``from_folder_``.
