CENotes lib package
===================

.. image:: https://travis-ci.org/cenotes/cenotes-lib.svg?branch=master
    :target: https://travis-ci.org/cenotes/cenotes-lib

**C(ryptographical) E(xpendable) Notes library**

-  Free software: GNU General Public License v3

-  `Backend & Frontend Demo`_

-  Source code:

   -  `Backend`_
   -  `Frontend`_
   -  `CLI`_

-  `Documentation`_

-  `Backend Design`_

What is this?
-------------

This is a **library** project to support encryption/decryption
of expendable notes

An example of a backend that uses the libraries provided here can be
found at https://cenot.es

What this isn’t
---------------

UI/Frontend/Backend/CLI. This is a **library** project. Frontend and
backend solutions are different projects. The reason for this is to
allow flexibility in frontend / backend choice and to avoid huge bundle
projects.

-  A **backend** project that uses these libraries can be found `here`_

-  A **frontend** project that communicates with the **backend** can be
   found `here <https://github.com/cenotes/cenotes-reaction>`__

-  A **cli** project that uses these libraries can be found
   `here <https://github.com/cenotes/cenotes-cli>`__

Features
--------

-  Symmetric encryption of notes using the `pynacl`_ project

How does cenotes work?
----------------------

See `design`_

How to use
----------

**You will need python >= 3.4**


Installing the python package

-  Ideally inside a virtualenv: ``pip install cenotes-lib``

- Then in your project: ``import cenotes_lib``


.. _Backend & Frontend Demo: https://cenot.es
.. _Backend: https://github.com/cenotes/cenotes
.. _Frontend: https://github.com/cenotes/cenotes-reaction
.. _CLI: https://github.com/cenotes/cenotes-cli
.. _Documentation: https://cenotes.readthedocs.io
.. _Backend Design: https://cenotes.readthedocs.io/en/latest/design.html
.. _here: https://github.com/cenotes/cenotes
.. _pynacl: https://pynacl.readthedocs.io/en/latest/
.. _design: https://cenotes.readthedocs.io/en/latest/design.html

