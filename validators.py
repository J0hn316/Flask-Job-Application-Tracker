from datetime import date
from urllib.parse import urlparse

ALLOWED_STATUSES = {
    "Applied",
    "Interviewing",
    "Rejected",
    "Offer",
}


def is_valid_url(url: str) -> bool:
    parsed_url = urlparse(url)

    return parsed_url.scheme in {"http", "https"} and bool(parsed_url.netloc)


def is_valid_iso_date(date_value: str) -> bool:
    try:
        date.fromisoformat(date_value)
    except ValueError:
        return False

    return True


def validate_job_application_input(
    company_name: str,
    job_title: str,
    status: str,
    date_applied: str,
    job_url: str,
) -> list[str]:
    errors: list[str] = []

    if not company_name:
        errors.append("Company name is required.")

    if not job_title:
        errors.append("Job title is required.")

    if not status:
        errors.append("Application status is required.")
    elif status not in ALLOWED_STATUSES:
        errors.append("Application status is invalid.")

    if not date_applied:
        errors.append("Date applied is required.")
    elif not is_valid_iso_date(date_applied):
        errors.append("Date applied must be a valid date.")

    if job_url and not is_valid_url(job_url):
        errors.append(
            "Job posting URL must start with http:// or https:// and include a valid domain."
        )

    return errors
