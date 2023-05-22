from django.test import TestCase

# Create your tests here.

# We have to install gevent using pip :-
#
# pip install gevent
#
# Then to run celery,
#
# celery -A <proj_name> worker -l info -P gevent