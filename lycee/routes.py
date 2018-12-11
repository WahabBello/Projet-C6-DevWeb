from flask import render_template, url_for, flash, redirect, request, abort
from lycee import app, db
from lycee.forms import RegistrationForm, LoginForm, ClasseForm, UpdateForm
from lycee.models import User, Classe, Admin
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required

@app.context_processor
def injet_now():
    return dict(now=datetime.now())


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html',)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/Formation")
def formation():
    return render_template('formation.html', title='Formations')

@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')

@app.route("/gestion")
@login_required
def gestion():
    classes= Classe.query.all()
    return render_template('gestion.html', title='Gestion des classes', classes=classes)



@app.route("/classe/new", methods=['GET', 'POST'])
@login_required
def new_classe():
    form = ClasseForm()
    if form.validate_on_submit():
        classe = Classe(title=form.title.data)
        db.session.add(classe)
        db.session.commit()
        flash('Your classrom has been created!', 'success')
        return redirect(url_for('gestion'))
    return render_template('create_classe.html', title='New Classe',
                           form=form, legend='New Classe')

@app.route("/Classe/<int:classe_id>")
def classe(classe_id):
    classe = Classe.query.get_or_404(classe_id)
    users = User.query.filter_by(classe=classe.title).all()   
    return render_template('classe.html', users=users, title=classe.title, classe=classe)

@app.route("/Liste_Total")
@login_required
def liste_total():
    users = User.query.all()
    return render_template('liste_total.html', users=users, title='Liste Total')


@app.route("/user/new", methods=['GET', 'POST'])
@login_required
def new_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(prenom=form.prenom.data, nom=form.nom.data, email=form.email.data, number=form.number.data,
                    niveau=form.niveau.data, classe=form.classe.data)
        db.session.add(user)
        db.session.commit()
        flash('Your user has been created!', 'success')
        return redirect(url_for('liste_total'))
    return render_template('create_user.html', title='New User',
                           form=form, legend='New User')


@app.route("/User/<int:user_id>")
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', title=user.nom, user=user)


@app.route("/<int:user_id>/update", methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UpdateForm()
    if form.validate_on_submit():
        user.prenom = form.prenom.data
        user.nom = form.nom.data
        user.email = form.email.data
        user.number = form.number.data
        user.niveau = form.niveau.data
        user.classe = form.classe.data
        db.session.commit()
        flash('Your user has been updated!', 'success')
        return redirect(url_for('liste_total'))
    elif request.method == 'GET':
        form.prenom.data = user.prenom
        form.nom.data = user.nom 
        form.email.data = user.email
        form.number.data = user.number
        form.niveau.data = user.niveau
        form.classe.data = user.classe
    return render_template('update_user.html', title='Update User',
                           form=form, legend='Update User')


@app.route("/register", methods=['GET', 'POST'])
def register():    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(prenom = form.prenom.data, nom = form.nom.data, email = form.email.data, number = form.number.data,
                    niveau = form.niveau.data, classe = form.classe.data, classe_id=form.classe.data)
        db.session.add(user)
        db.session.commit()
        flash('Your registration has been received! We will contact you sonn !!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html', title='Inscription', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('gestion')) 
    form = LoginForm()
    if form.validate_on_submit():
        user=Admin.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user:
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('login'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Connection', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))




@app.route("/classe/<int:classe_id>/delete", methods=['POST'])
@login_required
def delete_classe(classe_id):
    classe = Classe.query.get_or_404(classe_id)
    db.session.delete(classe)
    db.session.commit()
    flash('The classrom has been deleted!', 'success')
    return redirect(url_for('gestion'))


@app.route("/User/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('The user has been deleted!', 'success')
    return redirect(url_for('liste_total'))