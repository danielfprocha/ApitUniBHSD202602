from app.core.database import get_db_connection
from app.schemas.registro import RegistroBase


def listar() -> list[dict]:
    conn = get_db_connection()
    try:
        rows = conn.execute("SELECT * FROM registros").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def buscar_por_id(registro_id: int) -> dict | None:
    conn = get_db_connection()
    try:
        row = conn.execute("SELECT * FROM registros WHERE id = ?", (registro_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def criar(registro: RegistroBase) -> dict:
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO registros (titulo, descricao, ativo) VALUES (?, ?, ?)",
            (registro.titulo, registro.descricao, registro.ativo),
        )
        conn.commit()
        return {**registro.model_dump(), "id": cursor.lastrowid}
    finally:
        conn.close()


def atualizar(registro_id: int, registro: RegistroBase) -> dict | None:
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "UPDATE registros SET titulo = ?, descricao = ?, ativo = ? WHERE id = ?",
            (registro.titulo, registro.descricao, registro.ativo, registro_id),
        )
        conn.commit()
        if cursor.rowcount == 0:
            return None
        return {**registro.model_dump(), "id": registro_id}
    finally:
        conn.close()


def deletar(registro_id: int) -> bool:
    conn = get_db_connection()
    try:
        cursor = conn.execute("DELETE FROM registros WHERE id = ?", (registro_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()