===================
Changing formatting
===================

Changing displayed columns
--------------------------

If you want displayed columns in a list operation, ``-c`` option can be used.
``-c`` can be specified multiple times and the column order will be same as
the order of ``-c`` options.

Changing format
---------------

If you want to change the format data is displayed in, you can use ``-f``
option for that. Format can be specified just once and it affects they way
the data is printed to the ``STDOUT``. The available formats, data can be
presented in, can be checked with:

.. code-block:: text

    monasca <command> --help

Look for section **output formatters** and the flag ``--format`` or ``-f``.
In most of the cases you will be able to pick one out of
``csv``, ``json``, ``table``, ``value``, ``yaml``.

Affecting the width
-------------------

If, for some reason, you are not happy with the width the output has taken, you
can use ```--max-width {number}``` flag and set the value to
match your preference. Without that output will not be constrained
by the terminal width. Alternatively you may want to pass ``--fit-width``
to fit the output to display width. Remember that these flags
affect the output only if ``table`` formatter is used.
