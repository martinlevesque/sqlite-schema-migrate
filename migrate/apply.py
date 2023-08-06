from copy import deepcopy
from lib import log


# given the local schema, and remote schema, apply the diffs from the local schema to the remote schema

# Path: migrate/apply.py


def apply(local_parsed_schema=None, previous_parsed_schema=None, database=None):
    applied_schema = deepcopy(local_parsed_schema.all)

    for previous_item in previous_parsed_schema.all:
        if not any(other_item.id() == previous_item.id() for other_item in applied_schema):
            applied_schema.append(previous_item)

    for item in applied_schema:
        current = first_item([x for x in local_parsed_schema.all if x.id() == item.id()])
        previous = first_item([x for x in previous_parsed_schema.all if x.id() == item.id()])

        any_schema = current or previous

        any_schema.apply_changes(
            current_schema=current,
            previous_schema=previous,
            database=database
        )


def first_item(items):
    if len(items) > 0:
        return items[0]

    return None

    # items_to_apply = ["pragmas", "tables", "indexes", "drop_entities"]

    # for item_name in items_to_apply:
    #    apply_items(
    #        current_parsed_schema=applied_schema,
    #        previous_parsed_schema=previous_parsed_schema,
    #        attribute_name_items=item_name,
    #        database=database,
    #    )

    return applied_schema


def apply_items(
        current_parsed_schema=None,
        previous_parsed_schema=None,
        attribute_name_items=None,
        database=None,
):
    current_schema_items = getattr(current_parsed_schema, attribute_name_items)

    # the following item names are no more in the current schema
    missing_name_keys_in_current = [
        name
        for name in getattr(previous_parsed_schema, attribute_name_items).keys()
        if name not in current_schema_items.keys()
    ]

    for name in missing_name_keys_in_current:
        # it's getting initialized to null, so that we still process it
        current_schema_items[name] = None

    for name, item in current_schema_items.items():
        given_current_schema = getattr(current_parsed_schema, attribute_name_items).get(
            name, None
        )
        given_previous_schema = getattr(previous_parsed_schema, attribute_name_items).get(
            name, None
        )

        any_schema = given_current_schema or given_previous_schema
        any_schema.apply_changes(
            current_schema=given_current_schema,
            previous_schema=given_previous_schema,
            database=database,
        )
