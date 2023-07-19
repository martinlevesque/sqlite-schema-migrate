from copy import deepcopy
from lib import log

# given the local schema, and remote schema, apply the diffs from the local schema to the remote schema

# Path: migrate/apply.py


def apply(local_schema=None, previous_schema=None, database=None):
    applied_schema = deepcopy(local_schema)

    # pragmas
    for pragma_name, pragma in local_schema.pragmas.items():
        pragma_schema = applied_schema.pragmas[pragma_name]

        desired_value = pragma.value()

        # get remote db value:
        current_value = previous_schema.pragmas.get(pragma_name, None)

        if current_value != desired_value:

            pragma_schema.override_value = desired_value
            database.execute(str(pragma_schema), log_function=log.info)

            mutated_value = database.first_column(f"PRAGMA {pragma_name};")
            pragma_schema.override_value = mutated_value

    # indexes
    for index_name, index in local_schema.indexes.items():
        print(f"index_name: {index_name}")
        print(f"index: {index}")


    return applied_schema
