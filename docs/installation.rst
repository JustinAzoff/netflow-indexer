Installation
============

Install prerequisites
---------------------

netflow indexer uses the python xapian bindings.  On debian you can install this using::

    # apt-get install python-pip python-xapian xapian-tools 

Install netflow-indexer
-----------------------

I recommend installing netflow-indexer into a virtual environment::

    # pip install -s -E /usr/local/python_env/ netflowindexer-0.1.9.tar.gz

Then modify your path or source the activation script::

    # PATH=/usr/local/python_env/bin/:$PATH
