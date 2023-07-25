from copy import deepcopy
from lib import log


# given the local schema, and remote schema, apply the diffs from the local schema to the remote schema

# Path: migrate/apply.py


def apply(local_parsed_schema=None, previous_parsed_schema=None, database=None):
    applied_schema = deepcopy(local_parsed_schema)

    # pragmas
    apply_items(
        current_parsed_schema=applied_schema,
        previous_parsed_schema=previous_parsed_schema,
        attribute_name_items="pragmas",
        database=database,
    )

    # todo refactor

    # tables
    for table_name, table_schema in local_parsed_schema.tables.items():
        table_schema = applied_schema.tables[table_name]

        previous_table_schema = previous_parsed_schema.tables.get(table_name, None)

        if previous_table_schema is None:
            database.execute(str(table_schema), log_function=log.info)
        else:
            log.debug(f"table {table_name} already exists...")

    # indexes
    apply_items(
        current_parsed_schema=applied_schema,
        previous_parsed_schema=previous_parsed_schema,
        attribute_name_items="indexes",
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
