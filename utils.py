import random
from flask import abort, current_app, make_response
from faker import Faker
import faker_commerce


fake = Faker()
fake.add_provider(faker_commerce.Provider)


def detailed_abort(code, details: str | Exception) -> None:
    """Abort response with additional 'details' key and value"""
    abort(
        make_response(
            {"code": code, "status": "Bad Request", "details": str(details)}, code
        )
    )


def generate_sample_data(
    num_of_categories=3, num_of_parts=6, base_category_name="base"
) -> None:
    """Creates parts and categories in current database"""
    from api.models import Category, Part

    categories_to_be_created = []

    base_exists = Category.objects.get_or_none(name=base_category_name)
    if not base_exists:
        categories_to_be_created.append(
            Category(name=base_category_name, parent_name="")
        )

    parts_to_be_created = []

    for _ in range(num_of_categories):
        category = Category(
            name=f"{fake.word()}-{str(random.randrange(1, 1000))}",
            parent_name=base_category_name,
        )
        categories_to_be_created.append(category)

    for _ in range(num_of_parts):
        part = Part(
            serial_number=fake.bothify(text="?????-######"),
            name=fake.ecommerce_name(),
            description=fake.paragraph(nb_sentences=2),
            category=categories_to_be_created[
                random.randrange(1, len(categories_to_be_created))
            ].name,  # Assign to random but not base category
            quantity=random.randrange(1, 300),
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

    Category.objects.insert(categories_to_be_created)
    Part.objects.insert(parts_to_be_created)
    current_app.logger.debug(
        f"Created base category, {str(num_of_categories)} subcategories of base, {str(num_of_parts)} parts assigned to random categories"
    )
