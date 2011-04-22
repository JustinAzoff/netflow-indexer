Installation
============

Install prerequisites
---------------------

netflow indexer uses the python xapian bindings.  The IPy module is used for
some subnet calculations to support CIDR searching.  On debian you can install
all the dependencies using::

    # apt-get install python-pip python-xapian xapian-tools  python-ipy

Install netflow-indexer
-----------------------

I recommend installing netflow-indexer into a virtual environment::

    # pip install -s -E /usr/local/python_env/ netflowindexer-0.1.9.tar.gz

Then modify your path or source the activation script::

    # PATH=/usr/local/python_env/bin/:$PATH
