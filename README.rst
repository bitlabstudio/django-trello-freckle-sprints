Django Trello Freckle Sprints
============

A reusable Django app that creates burndown charts based on Trello boards and Freckle entries.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-trello-freckle-sprints

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/django-trello-freckle-sprints.git#egg=sprints

TODO: Describe further installation steps (edit / remove the examples below):

Add ``sprints`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'sprints',
    )

Add the ``sprints`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^sprints/', include('sprints.urls')),
    )

Before your tags/filters are available in your templates, load them by using

.. code-block:: html

	{% load sprints_tags %}


Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate sprints


Usage
-----

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-trello-freckle-sprints
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch
