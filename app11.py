from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Cấu hình secret key và thư mục upload
app.secret_key = 'your_secret_key'  # Thay bằng một secret key mạnh
UPLOAD_FOLDER = 'static/uploads'  # Thư mục lưu trữ ảnh
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Giả lập cơ sở dữ liệu người dùng và bài đăng
users = {}
posts = []

@app.route('/')
def index():
    username = session.get('username')  # Lấy tên người dùng từ session
    return render_template('index.html', username=username, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Kiểm tra thông tin đăng nhập
        if email in users and check_password_hash(users[email]['password'], password):
            session['username'] = users[email]['username']  # Lưu tên người dùng vào session
            session['email'] = email  # Lưu email vào session
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
        
        # Kiểm tra xem email đã tồn tại chưa
        if email in users:
            flash("Email đã được sử dụng. Vui lòng chọn email khác.", "danger")
            return redirect(url_for('register'))
        
        # Kiểm tra xem mật khẩu có khớp không
        if password != confirm_password:
            flash("Mật khẩu và xác nhận mật khẩu không khớp.", "danger")
            return redirect(url_for('register'))
        
        # Lưu thông tin người dùng
        users[email] = {
            'username': username,
            'password': generate_password_hash(password),  # Mã hóa mật khẩu
        }

        flash("Đăng ký thành công!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# @app.route('/blog', methods=['GET', 'POST'])
# def blog():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         email = session.get('email')

#         if email:
#             # Lưu bài viết
#             post = {
#                 'title': title,
#                 'content': content,
#                 'author': users[email]['username'],
#                 'date': "2 days ago"  # Bạn có thể thay thế bằng thời gian thực
#             }
#             posts.append(post)
#             flash("Bài viết đã được đăng thành công!", "success")
#             return redirect(url_for('blog'))
#         else:
#             flash("Bạn cần đăng nhập để đăng bài viết.", "warning")
#             return redirect(url_for('login'))

#     return render_template('blog.html', posts=posts)
@app.route('/blog', methods=['GET', 'POST'])
def blog():
    # Phân trang
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Số bài viết trên mỗi trang
    total_posts = len(posts)
    total_pages = (total_posts + per_page - 1) // per_page  # Tính tổng số trang

    # Lấy bài viết cho trang hiện tại
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

@app.route('/logout')  # Đường dẫn để đăng xuất
def logout():
    session.pop('username', None)  # Xóa tên người dùng khỏi session
    session.pop('email', None)  # Xóa email khỏi session
    flash("Bạn đã đăng xuất thành công!", "success")
    return redirect(url_for('index'))
@app.route('/profile')
def profile():
    if 'username' not in session:
        flash("Bạn cần đăng nhập để xem thông tin hồ sơ của mình.", "warning")
        return redirect(url_for('login'))

    email = session.get('email')
    user_info = users.get(email)

    return render_template('profile.html', user_info=user_info)
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    email = session.get('email')  # Lấy email người dùng từ session
    if not email or email not in users:
        flash("Bạn cần đăng nhập để chỉnh sửa thông tin.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        real_name = request.form['real_name']
        location = request.form['location']
        about_me = request.form['about_me']

        # Xử lý tải lên file avatar
        avatar = request.files['avatar']
        avatar_url = users[email].get('avatar_url', '')
        if avatar and avatar.filename:
            # Lưu file avatar vào thư mục uploads
            avatar_filename = secure_filename(avatar.filename)
            avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], avatar_filename))
            avatar_url = url_for('static', filename='uploads/' + avatar_filename)
        
        # Cập nhật thông tin người dùng
        users[email]['real_name'] = real_name
        users[email]['location'] = location
        users[email]['about_me'] = about_me
        users[email]['avatar_url'] = avatar_url  # Cập nhật URL avatar

        flash("Thông tin đã được cập nhật!", "success")
        return redirect(url_for('profile'))

    user_info = users[email]
    return render_template('edit_profile.html', user_info=user_info)
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    # Kiểm tra xem bài viết có tồn tại không
    if post_id < 0 or post_id >= len(posts):
        flash("Bài viết không tồn tại.", "danger")
        return redirect(url_for('blog'))

    post = posts[post_id]  # Lấy bài viết để chỉnh sửa

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # Cập nhật bài viết
        posts[post_id]['title'] = title
        posts[post_id]['content'] = content
        flash("Bài viết đã được chỉnh sửa thành công!", "success")
        return redirect(url_for('blog'))

    return render_template('edit_post.html', post=post, post_id=post_id)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)  # Tạo thư mục nếu chưa tồn tại
    app.run(debug=True)
