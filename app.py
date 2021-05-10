from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["SECRET_KEY"] = "cle_de_votre_application"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'votre_adresse_email@gmail.com'
app.config["MAIL_PASSWORD"] = 'votre_mot_de_passe'
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
db = SQLAlchemy(app)
mail = Mail(app)
bootstrap = Bootstrap(app)

class ContactForm(FlaskForm):
    """
        Création du formulaire
    """
    name = StringField(label="votre nom".upper(), validators=[DataRequired()])
    email = StringField(label="votre mail".upper(), validators=[DataRequired(), Email()])
    content = TextAreaField(label="votre message".upper(), validators=[DataRequired()])
    submit = SubmitField(label="Envoyer")

class Contact(db.Model):
    """
        Création de la table contacts dans la base de donnée
    """
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow())

    def __str__(self):
        return self.name

@app.route("/", methods=("GET", "POST"))
def contact():
    form = ContactForm()
    if request.method == "POST" and form.validate_on_submit():
        name = request.form.get("name")
        email = request.form.get("email")
        content = request.form.get("content")

        # Sauvegarde dans la base de donnée
        new_contact = Contact(
            name=name,
            email=email,
            content=content
        )
        db.session.add(new_contact)
        db.session.commit()

        # Envoi email de confirmation
        msg = Message(
            "Confirmation réception de votre message",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )
        body = f"""
            Bonjour {name},
            Nous avons bien reçu votre message, et
            nous mettons tout en oeuvre pour vous répondre 
            dans les meilleurs dalais.
        """
        msg.body = body
        mail.send(msg)

        flash("Votre message a été envoyé avec succès", "success")
        return redirect(url_for("contact"))
    else:
        form = ContactForm()
    return render_template("contact.html", form=form)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)