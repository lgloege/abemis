.. abemis documentation master file, created by
   sphinx-quickstart on Thu Jul 25 14:24:07 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ABEMIS Documentation
====================

``abemis`` is Python package to calculate activity-based emissions.
Activity-based emissions (:math:`E`) are typically caculated as the product of
of an *activity* (:math:`A`) by an *emission factor* (:math:`EF`)

.. math::

   E = A \cdot EF

However, sometimes the equation is more complex,
wich activities and emission factors requring additional information.
This is where ``abemis`` shines.

Abemis is based on the `GHG protocol for cities <https://ghgprotocol.org/ghg-protocol-cities>`_
and `2006 IPCC Guidelines for National Greenhouse Gas Inventories <https://www.ipcc-nggip.iges.or.jp/public/2006gl/>`_.

.. note::

   Contributions are encouraged as this project is a work in progress.


Installation
------------

.. code-block:: Python

   # bleeding edge installation
   pip install git+https://github.com/lgloege/abemis.git

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   api

.. toctree::
   :maxdepth: 2
   :caption: Help and Reference

   contributing
   authors
   GitHub Repo <https://github.com/lgloege/abemis>


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`