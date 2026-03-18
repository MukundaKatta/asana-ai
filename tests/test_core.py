"""Tests for AsanaAi."""
from src.core import AsanaAi
def test_init(): assert AsanaAi().get_stats()["ops"] == 0
def test_op(): c = AsanaAi(); c.process(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = AsanaAi(); [c.process() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = AsanaAi(); c.process(); c.reset(); assert c.get_stats()["ops"] == 0
def test_service_name(): c = AsanaAi(); r = c.process(); assert r["service"] == "asana-ai"
