from flask import Blueprint, send_file, jsonify
import io
import requests
from services.student_client import fetch_student
from services.pdf_generator import generate_pdf

report_bp = Blueprint("report", __name__)


@report_bp.get("/students/<student_id>/report")
def get_student_report(student_id: str):
    try:
        student = fetch_student(student_id)
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot connect to the Node.js backend. Make sure it is running on port 5007."}), 503
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"Backend returned an error: {e.response.status_code}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if student is None:
        return jsonify({"error": f"Student with id '{student_id}' not found"}), 404

    pdf_bytes = generate_pdf(student)
    filename = f"student_{student_id}_report.pdf"

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )
