
from copy import deepcopy
from lib import log

# given the local schema, and remote schema, apply the diffs from the local schema to the remote schema

# Path: migrate/apply.py


def apply(local_schema=None, previous_schema=None, database=None):
    applied_schema = deepcopy(local_schema)

    # pragmas
    for pragma_name, pragma in local_schema.pragmas.items():

        desired_value = pragma.value()

        # get remote db value:
        current_value = previous_schema.pragmas.get(pragma_name, None)

        if current_value != desired_value:
            database.execute(f"PRAGMA {pragma_name} = {desired_value};", log_function=log.info)

            mutated_value = database.first_column(f"PRAGMA {pragma_name};")
            applied_schema.pragmas[pragma_name].override_value = mutated_value

            # indexes:
            # todo: if index no more there, drop it

    return applied_schema
