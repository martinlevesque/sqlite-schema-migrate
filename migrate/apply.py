
# given the local schema, and remote schema, apply the diffs from the local schema to the remote schema

# Path: migrate/apply.py


def apply(local_schema=None, remote_schema=None, database=None):

    # pragmas
    for pragma_name, pragma in local_schema['pragmas'].items():
        print(f"will apply {pragma_name}!")

        desired_value = pragma.value()

        # get remote db value:
        current_value = database.first_column(f"PRAGMA {pragma_name};")
        print(f"remote value = {current_value}")

    print(f"will apply!")

    return {}
