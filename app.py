from flask import Flask, redirect, render_template, request, url_for

from database import (
    add_job_application,
    create_job_applications_table,
    delete_job_application,
    get_all_job_applications,
    get_job_application_by_id,
    update_job_application,
)

app = Flask(__name__)

create_job_applications_table()


@app.route("/", methods=["GET", "POST"])
def home() -> str:
    if request.method == "POST":
        company_name = request.form.get("company_name", "").strip()
        job_title = request.form.get("job_title", "").strip()
        status = request.form.get("status", "").strip()
        date_applied = request.form.get("date_applied", "").strip()
        job_url = request.form.get("job_url", "").strip()
        location = request.form.get("location", "").strip()
        notes = request.form.get("notes", "").strip()

        add_job_application(
            company_name,
            job_title,
            status,
            date_applied,
            job_url,
            location,
            notes,
        )

        return redirect(url_for("home"))

    applications = get_all_job_applications()

    return render_template("index.html", applications=applications)


@app.route(
    "/applications/<int:application_id>/edit",
    methods=["GET", "POST"],
)
def edit_job_application(application_id: int) -> str:
    application = get_job_application_by_id(application_id)

    if application is None:
        return redirect(url_for("home"))

    if request.method == "POST":
        company_name = request.form.get("company_name", "").strip()
        job_title = request.form.get("job_title", "").strip()
        status = request.form.get("status", "").strip()
        date_applied = request.form.get("date_applied", "").strip()
        job_url = request.form.get("job_url", "").strip()
        location = request.form.get("location", "").strip()
        notes = request.form.get("notes", "").strip()

        update_job_application(
            application_id,
            company_name,
            job_title,
            status,
            date_applied,
            job_url,
            location,
            notes,
        )

        return redirect(url_for("home"))

    return render_template(
        "edit_application.html",
        application=application,
    )


@app.route("/applications/<int:application_id>/delete", methods=["POST"])
def remove_job_application(application_id: int) -> str:
    delete_job_application(application_id)
    return redirect(url_for("home"))
