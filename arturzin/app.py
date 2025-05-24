from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import shutil

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "uma-chave-qualquer")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///dev.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
UPLOAD_FOLDER = "atestados"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)


class CallRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crm = db.Column(db.Integer, nullable=False)
    entry_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    exit_time = db.Column(db.DateTime, nullable=True)
    lessons_present = db.Column(db.Integer, nullable=True)
    absences = db.Column(db.Integer, nullable=True)
    justified = db.Column(db.Boolean, default=False)
    certificate_path = db.Column(db.String(200), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Registrar entrada
        try:
            crm = int(request.form["crm"])
        except (ValueError, KeyError):
            flash("CRM inválido.", "error")
            return redirect(url_for("index"))

        record = CallRecord(crm=crm)
        db.session.add(record)
        db.session.commit()
        flash(
            f"✅ Entrada registrada para CRM {crm} às {record.entry_time.strftime('%H:%M:%S')}",
            "success",
        )
        return redirect(url_for("index"))

    # GET: listar registros abertos (sem saída) e fechados (com saída)
    open_calls = CallRecord.query.filter_by(exit_time=None).all()
    closed_calls = (
        CallRecord.query.filter(CallRecord.exit_time.isnot(None))
        .order_by(CallRecord.entry_time.desc())
        .limit(10)
        .all()
    )
    return render_template(
        "index.html", open_calls=open_calls, closed_calls=closed_calls
    )


@app.route("/exit/<int:call_id>", methods=["POST"])
def register_exit(call_id):
    record = CallRecord.query.get_or_404(call_id)
    # confirmação de CRM
    try:
        crm_conf = int(request.form["crm_conf"])
    except (ValueError, KeyError):
        flash("CRM de confirmação inválido.", "error")
        return redirect(url_for("index"))

    if crm_conf != record.crm:
        flash("❌ CRM não corresponde ao de entrada.", "error")
        return redirect(url_for("index"))

    # marca saída
    record.exit_time = datetime.utcnow()
    # calcula aulas e faltas (exemplo fixo; aqui deveria vir sua lógica de horários)
    total_periods = 3
    # supondo presença total se entrou antes de primeiro horário
    record.lessons_present = 1
    record.absences = total_periods - record.lessons_present

    # trata upload de atestado
    file = request.files.get("certificate")
    if file and file.filename:
        filename = (
            f"{record.crm}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        )
        dest = os.path.join(UPLOAD_FOLDER, filename)
        file.save(dest)
        record.certificate_path = dest
        record.justified = True

    db.session.commit()
    flash(
        f"✅ Saída registrada para CRM {record.crm} às {record.exit_time.strftime('%H:%M:%S')}",
        "success",
    )
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
