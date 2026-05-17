import os
from flask import Flask, flash, redirect, render_template, request, url_for

from validators import ALLOWED_STATUSES, validate_job_application_input
from database import (
    add_job_application,
    create_job_applications_table,
    delete_job_application,
    get_job_application_by_id,
    update_job_application,
    get_filtered_job_applications,
    get_dashboard_stats,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "dev-secret-key-change-me",
)

create_job_applications_table()


@app.route("/", methods=["GET", "POST"])
def home() -> str:
    form_data = {
        "company_name": "",
        "job_title": "",
        "status": "Applied",
        "date_applied": "",
        "job_url": "",
        "location": "",
        "notes": "",
    }
    validation_errors: list[str] = []

    if request.method == "POST":
        form_data = {
            "company_name": request.form.get("company_name", "").strip(),
            "job_title": request.form.get("job_title", "").strip(),
            "status": request.form.get("status", "").strip(),
            "date_applied": request.form.get("date_applied", "").strip(),
            "job_url": request.form.get("job_url", "").strip(),
            "location": request.form.get("location", "").strip(),
            "notes": request.form.get("notes", "").strip(),
        }

        validation_errors = validate_job_application_input(
            form_data["company_name"],
            form_data["job_title"],
            form_data["status"],
            form_data["date_applied"],
            form_data["job_url"],
        )

        if not validation_errors:
            add_job_application(
                form_data["company_name"],
                form_data["job_title"],
                form_data["status"],
                form_data["date_applied"],
                form_data["job_url"],
                form_data["location"],
                form_data["notes"],
            )

            flash("Application added successfully.", "success")
            return redirect(url_for("home"))

    search_query = request.args.get("search", "").strip()
    status_filter = request.args.get("search", "").strip()

    if status_filter not in ALLOWED_STATUSES:
        status_filter = ""

    applications = get_filtered_job_applications(
        search_query=search_query,
        status_filter=status_filter,
    )

    dashboard_stats = get_dashboard_stats()

    return render_template(
        "index.html",
        applications=applications,
        dashboard_stats=dashboard_stats,
        form_data=form_data,
        validation_errors=validation_errors,
        search_query=search_query,
        status_filter=status_filter,
    )


@app.route(
    "/applications/<int:application_id>/edit",
    methods=["GET", "POST"],
)
def edit_job_application(application_id: int) -> str:
    application = get_job_application_by_id(application_id)

    if application is None:
        flash("Application not found.", "error")
        return redirect(url_for("home"))

    form_data = {
        "company_name": application["company_name"],
        "job_title": application["job_title"],
        "status": application["status"],
        "date_applied": application["date_applied"],
        "job_url": application["job_url"] or "",
        "location": application["location"] or "",
        "notes": application["notes"] or "",
    }

    validation_errors: list[str] = []

    if request.method == "POST":
        form_data = {
            "company_name": request.form.get("company_name", "").strip(),
            "job_title": request.form.get("job_title", "").strip(),
            "status": request.form.get("status", "").strip(),
            "date_applied": request.form.get("date_applied", "").strip(),
            "job_url": request.form.get("job_url", "").strip(),
            "location": request.form.get("location", "").strip(),
            "notes": request.form.get("notes", "").strip(),
        }

        validation_errors = validate_job_application_input(
            form_data["company_name"],
            form_data["job_title"],
            form_data["status"],
            form_data["date_applied"],
            form_data["job_url"],
        )

        if not validation_errors:
            update_job_application(
                application_id,
                form_data["company_name"],
                form_data["job_title"],
                form_data["status"],
                form_data["date_applied"],
                form_data["job_url"],
                form_data["location"],
                form_data["notes"],
            )
            flash("Application updated successfully.", "success")
            return redirect(url_for("home"))

    return render_template(
        "edit_application.html",
        application=application,
        form_data=form_data,
        validation_errors=validation_errors,
    )


@app.route("/applications/<int:application_id>/delete", methods=["POST"])
def remove_job_application(application_id: int) -> str:
    delete_job_application(application_id)
    flash("Application deleted successfully.", "success")
    return redirect(url_for("home"))
