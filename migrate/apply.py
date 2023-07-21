from copy import deepcopy
from lib import log

# given the local schema, and remote schema, apply the diffs from the local schema to the remote schema

# Path: migrate/apply.py


def apply(local_schema=None, previous_schema=None, database=None):
    applied_schema = deepcopy(local_schema)

    # todo refactor

    # pragmas
    for pragma_name, pragma in local_schema.pragmas.items():
        pragma_schema = applied_schema.pragmas[pragma_name]

        desired_value = pragma_schema.value()

        # get remote db value:
        previous_pragma_schema = previous_schema.pragmas.get(pragma_name, None)

        if (
            previous_pragma_schema is None
            or previous_pragma_schema.value() != desired_value
        ):
            pragma_schema.override_value = desired_value
            database.execute(str(pragma_schema), log_function=log.info)

            mutated_value = database.first_column(f"PRAGMA {pragma_name};")
            pragma_schema.override_value = mutated_value

    # indexes
    for index_name, index_schema in local_schema.indexes.items():
        index_schema = applied_schema.indexes[index_name]

        previous_index_schema = previous_schema.indexes.get(index_name, None)

        if previous_index_schema is None:
            database.execute(str(index_schema), log_function=log.info)
        else:
            log.debug(f"index {index_name} already exists...")

    return applied_schema
