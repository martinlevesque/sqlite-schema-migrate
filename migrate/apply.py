from copy import deepcopy
from lib import log


# given the local schema, and remote schema, apply the diffs from the local schema to the remote schema

# Path: migrate/apply.py


def apply(local_parsed_schema=None, previous_parsed_schema=None, database=None):
    applied_schema = deepcopy(local_parsed_schema)

    items_to_apply = ["pragmas", "tables", "indexes"]

    for item_name in items_to_apply:
        apply_items(
            current_parsed_schema=applied_schema,
            previous_parsed_schema=previous_parsed_schema,
            attribute_name_items=item_name,
            database=database,
        )


def apply_items(
    current_parsed_schema=None,
    previous_parsed_schema=None,
    attribute_name_items=None,
    database=None,
):
    current_schema_items = getattr(current_parsed_schema, attribute_name_items)

    for name, item in current_schema_items.items():
        given_current_schema = getattr(current_parsed_schema, attribute_name_items).get(
            name, None
        )
        given_previous_schema = getattr(previous_parsed_schema, attribute_name_items).get(
            name, None
        )

        given_current_schema.apply_changes(
            previous_schema=given_previous_schema, database=database
        )
