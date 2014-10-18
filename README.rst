Django Trello Freckle Sprints
=============================

A reusable Django app that creates burndown charts based on Trello boards and
Freckle entries.

The idea is that you have a Trello board which has three lists:

* Whishlist: Contains stuff that the customer adds whenever it comes to their
  mind. Someone needs to add estimations to these cards and move them into the
  Backlog.
* Backlog: Contains cards that have been estimated. The total estimated time
  is the time left to get everything done to finish the project. Cards from
  this list will moved into the Sprint list. 
* Sprint: Contains cards that are currently prioritized for a sprint.

On Trello, add ``(XXX)`` at the end of each card title, where ``XXX`` resembles
the number of minutes estimated for the card.

On Freckle, when you track time that has been spent on a certain card, just add
``cXXX`` to the entry description, where ``XXX`` is the card-ID from Trello
(you can see that in the URL when you open a card).

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
