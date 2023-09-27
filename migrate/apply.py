from copy import deepcopy

from schema.parsed_schema import ParsedSchema
from sqlite_db import Database
from lib import log


# given the local schema, and remote schema, apply the diffs from the local schema to the remote schema

# Path: migrate/apply.py


def apply(
    local_parsed_schema: ParsedSchema,
    previous_parsed_schema: ParsedSchema,
    database: Database,
    force: bool,
):
    applied_schema = deepcopy(local_parsed_schema.all)
    initiated_transaction = False

    for previous_item in previous_parsed_schema.all:
        if not any(
            other_item.id() == previous_item.id() for other_item in applied_schema
        ):
            applied_schema.append(previous_item)

    deleted_ids = []

    for item in applied_schema:
        print(f"for item = {item}")
        current = first_item(
            [x for x in local_parsed_schema.all if x.id() == item.id()]
        )
        previous = first_item(
            [x for x in previous_parsed_schema.all if x.id() == item.id()]
        )

        if item.TYPE != "pragma" and not initiated_transaction:
            database.execute("BEGIN TRANSACTION;", log_function=log.info)
            initiated_transaction = True

        any_schema = current or previous

        if any_schema is None:
            continue

        print(f"applying change {any_schema.id()}")
        state_result = any_schema.apply_changes(
            current,
            previous,
            database,
            force,
        )
        print(f"done applying change {any_schema.id()}")

        if state_result == "remove":
            deleted_ids.append(any_schema.id())

    database.execute("COMMIT;", log_function=log.info)

    return [schema for schema in applied_schema if schema.id() not in deleted_ids]


def first_item(items: list):
    if len(items) > 0:
        return items[0]

    return None
