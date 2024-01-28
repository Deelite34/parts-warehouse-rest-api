import random
from api.models import Category, Part
from tests.conftest import BASE_CATEGORY_NAME, SUBCATEGORY_NAME
from utils import fake


def make_category(count=1):
    """Creates subcategories of base category."""

    categories_to_be_created = []

    base_exists = Category.objects.get_or_none(name=BASE_CATEGORY_NAME)
    if not base_exists:
        categories_to_be_created.append(
            Category(name=BASE_CATEGORY_NAME, parent_name="")
        )

    for _ in range(count):
        category = Category(
            name=fake.word() + str(random.uniform(1, 10000000)),
            parent_name=BASE_CATEGORY_NAME,
        )
        categories_to_be_created.append(category)

    return Category.objects.insert(categories_to_be_created)


def make_part(category_name=SUBCATEGORY_NAME, count=1):
    base_category = Category.objects.get_or_none(name=BASE_CATEGORY_NAME)
    if not base_category:
        base_category = Category(name=BASE_CATEGORY_NAME, parent_name="")
        base_category.save()

    category = Category.objects.get(name=category_name)
    if not category:
        category = Category(
            name=category_name + str(random.uniform(1, 10000000)),
            parent_name=BASE_CATEGORY_NAME,
        )

    parts_to_be_created = []

    for _ in range(count):
        part = Part(
            serial_number=fake.bothify(text="?????-######"),
            name=fake.ecommerce_name(),
            description=fake.paragraph(nb_sentences=2),
            category=category.name,
            quantity=random.randrange(300),
            price=round(random.uniform(1, 10000), 2),
            location={
                "room": random.randrange(1, 30),
                "bookcase": random.randrange(1, 100),
                "shelf": fake.bothify(text="??-##"),
                "cuvette": random.randrange(1, 30),
                "column": random.randrange(1, 50),
                "row": random.randrange(1, 20),
            },
        )
        parts_to_be_created.append(part)

    return Part.objects.insert(parts_to_be_created)
