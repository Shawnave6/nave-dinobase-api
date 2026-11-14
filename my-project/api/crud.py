TABLE = "prehis_creat"

FIELDS = [
    "name", "scientific_name", "period", "diet", "family", "type", "defence",
    "location", "discovered", "life_span", "habitat", "weight", "height", "extinction",
]
COLUMNS = ["id"] + FIELDS
SELECT_COLUMNS = ", ".join(COLUMNS)
FILTERS = ["period", "diet", "habitat"]


def list_creatures(conn, filters=None):
    filters = filters or {}
    clauses, params = [], []
    for column in FILTERS:
        if filters.get(column):
            clauses.append(f"{column} = %s")
            params.append(filters[column])
    where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
    return conn.execute(
        f"SELECT {SELECT_COLUMNS} FROM {TABLE}{where} ORDER BY id", params
    ).fetchall()


def search_creatures(conn, text):
    escaped = text.lower().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return conn.execute(
        f"SELECT {SELECT_COLUMNS} FROM {TABLE} "
        "WHERE concat_ws(' ', name, scientific_name, period, diet, family, type, defence, location, habitat) "
        "ILIKE %s ORDER BY id",
        (f"%{escaped}%",),
    ).fetchall()


def get_creature(conn, creature_id):
    return conn.execute(
        f"SELECT {SELECT_COLUMNS} FROM {TABLE} WHERE id = %s", (creature_id,)
    ).fetchone()


def create_creature(conn, data):
    placeholders = ", ".join(["%s"] * len(FIELDS))
    values = [data[field] for field in FIELDS]
    return conn.execute(
        f"INSERT INTO {TABLE} ({', '.join(FIELDS)}) VALUES ({placeholders}) RETURNING {SELECT_COLUMNS}",
        values,
    ).fetchone()


def update_creature(conn, creature_id, changes):
    changes = {key: value for key, value in changes.items() if key in FIELDS}
    if not changes:
        return get_creature(conn, creature_id)
    assignments = ", ".join(f"{column} = %s" for column in changes)
    return conn.execute(
        f"UPDATE {TABLE} SET {assignments} WHERE id = %s RETURNING {SELECT_COLUMNS}",
        [*changes.values(), creature_id],
    ).fetchone()


def delete_creature(conn, creature_id):
    row = conn.execute(
        f"DELETE FROM {TABLE} WHERE id = %s RETURNING id", (creature_id,)
    ).fetchone()
    return row is not None
