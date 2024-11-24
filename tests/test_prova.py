import pytest
import sys
sys.path.append('.')

from flask import session
#from app import app
import app as app

def test_add():
    result = app.add(a=1,b=4)
    assert result == 5