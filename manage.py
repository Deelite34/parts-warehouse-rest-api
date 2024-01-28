import click

from flask.cli import with_appcontext
import pytest
from utils import generate_sample_data


@click.command("generate_data")
@with_appcontext
def create_data():
    """Generate set of data consisting of 1 base category, 3 subcategories and 6 parts using them"""
    generate_sample_data(num_of_categories=3, num_of_parts=6)


@click.command("test")
@with_appcontext
def run_pytest():
    pytest.main(["-s", "tests"])
