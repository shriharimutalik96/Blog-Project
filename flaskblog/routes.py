import secrets
import os
from PIL import Image
from flask import render_template,url_for,flash,redirect,request,abort
from flaskblog.forms import RegistrationForm,LoginForm,UpdateAccountForm,PostForm
from flaskblog import app
from flaskblog.models import User,Post
from flaskblog import db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required


@app.route('/')
@app.route('/home')
def home():
    auth_user = current_user.is_authenticated
    posts = Post.query.all()

    return render_template('home.html',posts=posts,title='Home',auth_user=auth_user)



@app.route('/about')
def about():
    return render_template('about.html',title='About')





@app.route('/register',methods=['GET','POST'])
def register():
  if current_user.is_authenticated :
    return redirect(url_for('home'))
  form = RegistrationForm()                                                                       # an instance/object of RegistrationForm class  : Display the form
  if form.validate_on_submit():                                                                   #validate on clicking the submit button
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')           # generating a hashed password once the form has been submitted ,it.e the data sent to the route is 'POST' data
    user = User(username=form.username.data,email=form.email.data,password=hashed_password)       #creating an instance of user
    db.session.add(user)          # adding the  user to the database
    db.session.commit()                                                                          # adding user to the database
    flash(f'Account created for {form.username.data}!,You are able to login',category="success")  # success here is a bootstrap class
    return redirect(url_for('login'))                                                             # here home is the function not the title , so this link will be redirected to
                                                                                                  # to the home route(function)

  return render_template('register.html',title='Register',form=form)









@app.route('/login',methods=['GET','POST'])
def login():
  if current_user.is_authenticated :
    return redirect(url_for('home'))
  form = LoginForm()            # an instance/objecct of LoginForm class

  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()

    if user and bcrypt.check_password_hash(user.password,form.password.data):
      login_user(user,remember=form.remember.data)          #calling the login_user method from models.py
      flash('You have been successfully logged in',category='success')
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('home'))  #ternary conditional

    elif user==None:
      flash('Please register before logging in',category='primary')
      return redirect(url_for('register'))

    else:
      flash('Login unsuccessful.Please check email and password',category='danger')

  return render_template('login.html',title='Login',form=form)





@app.route('/logout')
def logout():
  logout_user()

  return redirect(url_for('home'))





def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  f_name,f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path , 'static/profile_pics', picture_fn)

  output_size = (125,125)
  image_pillow = Image.open(form_picture)
  image_pillow.thumbnail(output_size)

  image_pillow.save(picture_path)

  return picture_fn






@app.route('/account',methods=['GET','POST'])
@login_required
def account():
  image_file = url_for('static' ,filename='profile_pics/' + current_user.image_file)
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:     # if it is not None
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data

    db.session.commit()   # moving the changes to the database
    flash('Account has been updated',category="success")
    return redirect(url_for('account'))

  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email



  return render_template('account.html',title='Profile',
          image_file=image_file,form=form)






@app.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(title=form.title.data,content=form.content.data,author=current_user)
    db.session.add(post)
    db.session.commit()
    flash('Your post has been created!',category='success')
    return redirect(url_for('home'))


  return render_template('create_post.html',title='New Post',form=form)



@app.route('/post/<int:post_id>')
def post_detail(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('post.html',title=post.title,post=post)




@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
def post_update(post_id):
  post = Post.query.get_or_404(post_id)

  if post.author != current_user:
    abort(403)

  form = PostForm()

  if form.validate_on_submit():
    post.title = form.title.data
    post.content = form.content.data
    db.session.commit()
    flash('Post has been updated',category="success")
    return redirect(url_for('post_detail',post_id=post.id))

  elif request.method == 'GET':
    form.title.data = post.title
    form.content.data = post.content

  return render_template('update_post.html',title='Update Post',form=form)


@app.route('/post/<int:post_id>/delete',methods=['POST'])
def delete_post(post_id):


  post = Post.query.get_or_404(post_id)

  if post.author != current_user:
    abort(403)

  db.session.delete(post)
  db.session.commit()
  flash('Post has been deleted',category="success")
  return redirect(url_for('home'))
