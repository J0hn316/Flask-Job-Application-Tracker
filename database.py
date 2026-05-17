import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "applications.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_job_applications_table() -> None:
    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS job_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                status TEXT NOT NULL,
                date_applied TEXT NOT NULL,
                job_url TEXT,
                location TEXT,
                notes TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """)
        connection.commit()
    finally:
        connection.close()


def add_job_application(
    company_name: str,
    job_title: str,
    status: str,
    date_applied: str,
    job_url: str,
    location: str,
    notes: str,
) -> None:
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO job_applications (
                company_name,
                job_title,
                status,
                date_applied,
                job_url,
                location,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                company_name,
                job_title,
                status,
                date_applied,
                job_url,
                location,
                notes,
            ),
        )
        connection.commit()
    finally:
        connection.close()


def get_all_job_applications() -> list[sqlite3.Row]:
    connection = get_connection()

    try:
        applications = connection.execute("""
            SELECT
                id,
                company_name,
                job_title,
                status,
                date_applied,
                job_url,
                location,
                notes,
                created_at
            FROM job_applications
            ORDER BY date_applied DESC, id DESC
            """).fetchall()

        return applications
    finally:
        connection.close()


def get_job_application_by_id(
    application_id: int,
) -> sqlite3.Row | None:
    connection = get_connection()

    try:
        application = connection.execute(
            """
            SELECT
                id,
                company_name,
                job_title,
                status,
                date_applied,
                job_url,
                location,
                notes,
                created_at
            FROM job_applications
            WHERE id = ?
            """,
            (application_id,),
        ).fetchone()

        return application
    finally:
        connection.close()


def update_job_application(
    application_id: int,
    company_name: str,
    job_title: str,
    status: str,
    date_applied: str,
    job_url: str,
    location: str,
    notes: str,
) -> None:
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE job_applications
            SET
                company_name = ?,
                job_title = ?,
                status = ?,
                date_applied = ?,
                job_url = ?,
                location = ?,
                notes = ?
            WHERE id = ?
            """,
            (
                company_name,
                job_title,
                status,
                date_applied,
                job_url,
                location,
                notes,
                application_id,
            ),
        )
        connection.commit()
    finally:
        connection.close()


def get_filtered_job_applications(
    search_query: str = "",
    status_filter: str = "",
) -> list[sqlite3.Row]:
    connection = get_connection()

    try:
        sql_query = """
            SELECT
                id,
                company_name,
                job_title,
                status,
                date_applied,
                job_url,
                location,
                notes,
                created_at
            FROM job_applications
            WHERE 1 = 1
        """
        parameters: list[str] = []

        if search_query:
            search_term = f"%{search_query}%"

            sql_query += """
                AND (
                    company_name LIKE ?
                    OR job_title LIKE ?
                )
            """
            parameters.extend([search_term, search_term])

        if status_filter:
            sql_query += """
                AND status = ?
            """
            parameters.append(status_filter)

        sql_query += """
            ORDER BY date_applied DESC, id DESC
        """

        applications = connection.execute(
            sql_query,
            parameters,
        ).fetchall()

        return applications
    finally:
        connection.close()


def delete_job_application(application_id: int) -> None:
    connection = get_connection()

    try:
        connection.execute(
            """
            DELETE FROM job_applications
            WHERE id = ?
            """,
            (application_id,),
        )
        connection.commit()
    finally:
        connection.close()
