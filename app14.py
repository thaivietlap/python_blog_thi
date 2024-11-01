from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Cấu hình secret key và thư mục upload
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Giả lập cơ sở dữ liệu người dùng
users = {
    'user1@example.com': {'username': 'user1', 'password': generate_password_hash('password1'), 'following': set(), 'avatar_url': '', 'real_name': '', 'location': '', 'about_me': ''},
    'user2@example.com': {'username': 'user2', 'password': generate_password_hash('password2'), 'following': set(), 'avatar_url': '', 'real_name': '', 'location': '', 'about_me': ''},
}

posts = []
comments = []  # Danh sách để lưu trữ bình luận

@app.route('/')
def index():
    username = session.get('username')
    email = session.get('email')
    return render_template('index.html', username=username, users=users, email=email, comments=comments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users and check_password_hash(users[email]['password'], password):
            session['username'] = users[email]['username']
            session['email'] = email
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('index'))
        else:
            flash("Thông tin đăng nhập không hợp lệ. Vui lòng thử lại.", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if email in users:
            flash("Email đã được sử dụng. Vui lòng chọn email khác.", "danger")
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash("Mật khẩu và xác nhận mật khẩu không khớp.", "danger")
            return redirect(url_for('register'))
        
        users[email] = {
            'username': username,
            'password': generate_password_hash(password),
            'following': set(),
            'avatar_url': '',
            'real_name': '',
            'location': '',
            'about_me': ''
        }

        flash("Đăng ký thành công!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    total_posts = len(posts)
    total_pages = (total_posts + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    posts_to_show = posts[start:end]

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        email = session.get('email')

        if email and email in users:
            post = {
                'title': title,
                'content': content,
                'author': users[email]['username'],
                'date': "2 days ago"
            }
            posts.append(post)
            flash("Bài viết đã được đăng thành công!", "success")
            return redirect(url_for('blog'))
        else:
            flash("Bạn cần đăng nhập để đăng bài viết.", "warning")
            return redirect(url_for('login'))

    return render_template('blog.html', posts=posts_to_show, total_pages=total_pages, current_page=page)

@app.route('/follow/<string:email_to_follow>')
def follow(email_to_follow):
    email = session.get('email')
    if email and email_to_follow in users:
        if email_to_follow not in users[email]['following']:
            users[email]['following'].add(email_to_follow)
            flash(f"Bạn đã theo dõi {users[email_to_follow]['username']}", "success")
        else:
            flash("Bạn đã theo dõi người này.", "info")
    else:
        flash("Đăng nhập để theo dõi người khác.", "warning")
    return redirect(url_for('index'))

@app.route('/unfollow/<string:email_to_unfollow>')
def unfollow(email_to_unfollow):
    email = session.get('email')
    if email and email_to_unfollow in users:
        if email_to_unfollow in users[email]['following']:
            users[email]['following'].remove(email_to_unfollow)
            flash(f"Bạn đã hủy theo dõi {users[email_to_unfollow]['username']}", "success")
        else:
            flash("Bạn chưa theo dõi người này.", "info")
    else:
        flash("Đăng nhập để hủy theo dõi người khác.", "warning")
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    flash("Bạn đã đăng xuất thành công!", "success")
    return redirect(url_for('index'))

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if post_id < 0 or post_id >= len(posts):
        flash("Bài viết không tồn tại.", "danger")
        return redirect(url_for('blog'))
    
    post = posts[post_id]

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        flash("Bài viết đã được cập nhật thành công!", "success")
        return redirect(url_for('blog'))

    return render_template('edit_post.html', post=post)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    email = session.get('email')
    if not email or email not in users:
        flash("Bạn cần đăng nhập để chỉnh sửa thông tin.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        real_name = request.form['real_name']
        location = request.form['location']
        about_me = request.form['about_me']
        
        avatar = request.files['avatar']
        avatar_url = users[email].get('avatar_url', '')
        if avatar and avatar.filename:
            avatar_filename = secure_filename(avatar.filename)
            avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))
            avatar_url = url_for('static', filename='uploads/' + avatar_filename)

        users[email]['real_name'] = real_name
        users[email]['location'] = location
        users[email]['about_me'] = about_me
        users[email]['avatar_url'] = avatar_url

        flash("Thông tin đã được cập nhật!", "success")
        return redirect(url_for('profile'))

    user_info = users[email]
    return render_template('edit_profile.html', user_info=user_info)

@app.route('/following')
def following():
    if 'email' not in session:
        flash("Bạn cần đăng nhập để xem danh sách đang theo dõi.", "warning")
        return redirect(url_for('login'))
    
    email = session['email']
    following_users = users[email]['following']
    return render_template('following.html', following_users=following_users, users=users)

@app.route('/user_profile/<string:email>', methods=['GET'])
def user_profile(email):
    if 'username' not in session:
        flash("Bạn cần đăng nhập để xem thông tin hồ sơ của mình.", "warning")
        return redirect(url_for('login'))

    user_info = users.get(email)
    if user_info is None:
        flash("Người dùng không tồn tại.", "danger")
        return redirect(url_for('index'))

    return render_template('profile.html', user_info=user_info)

@app.route('/profile')
def profile():
    if 'username' not in session:
        flash("Bạn cần đăng nhập để xem thông tin hồ sơ của mình.", "warning")
        return redirect(url_for('login'))

    email = session.get('email')
    user_info = users.get(email)
    return render_template('profile.html', user_info=user_info)

@app.route('/post_comment', methods=['POST'])
def post_comment():
    comment_content = request.form.get('comment')
    username = session.get('username', 'Anonymous')  # Sử dụng tên người dùng từ session

    if comment_content:
        comments.append({'username': username, 'content': comment_content})
        flash('Bình luận đã được đăng!', 'success')
    else:
        flash('Vui lòng nhập bình luận!', 'danger')

    return redirect('/')

@app.route('/comments')  # Đường dẫn URL cho trang bình luận
def show_comments():
    return render_template('comments.html', comments=comments)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
