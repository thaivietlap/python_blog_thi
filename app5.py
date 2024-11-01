# from flask import Flask, render_template, request, redirect, url_for, flash, session
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)

# # Cấu hình secret key
# app.secret_key = 'your_secret_key'  # Thay bằng một secret key mạnh

# # Giả lập cơ sở dữ liệu người dùng
# users = {}

# @app.route('/')
# def index():
#     username = session.get('username')  # Lấy tên người dùng từ session
#     return render_template('index.html', username=username)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
        
#         # Kiểm tra thông tin đăng nhập
#         if email in users and check_password_hash(users[email]['password'], password):
#             session['email'] = email  # Lưu email vào session
#             session['username'] = users[email]['username']  # Lưu tên người dùng vào session
#             flash("Đăng nhập thành công!", "success")
#             return redirect(url_for('profile'))  # Chuyển đến trang hồ sơ
#         else:
#             flash("Thông tin đăng nhập không hợp lệ. Vui lòng thử lại.", "danger")
#             return redirect(url_for('login'))

#     return render_template('login.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         email = request.form['email']
#         username = request.form['username']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']
#         real_name = request.form['real_name']  # Tên thật
#         location = request.form['location']  # Địa điểm
#         about_me = request.form['about_me']  # Giới thiệu bản thân
        
#         # Kiểm tra xem email đã tồn tại chưa
#         if email in users:
#             flash("Email đã được sử dụng. Vui lòng chọn email khác.", "danger")
#             return redirect(url_for('register'))
        
#         # Kiểm tra xem mật khẩu có khớp không
#         if password != confirm_password:
#             flash("Mật khẩu và xác nhận mật khẩu không khớp.", "danger")
#             return redirect(url_for('register'))
        
#         # Lưu thông tin người dùng
#         users[email] = {
#             'username': username,
#             'password': generate_password_hash(password),  # Mã hóa mật khẩu
#             'real_name': real_name,
#             'location': location,
#             'about_me': about_me
#         }

#         flash("Đăng ký thành công!", "success")
#         return redirect(url_for('login'))

#     return render_template('register.html')

# @app.route('/profile')  # Đường dẫn để hiển thị thông tin cá nhân
# def profile():
#     email = session.get('email')  # Lấy email người dùng từ session
#     if email and email in users:
#         user_info = users[email]
#         return render_template('profile.html', user_info=user_info)
#     flash("Bạn cần đăng nhập để xem trang này.", "warning")
#     return redirect(url_for('login'))

# @app.route('/logout')  # Đường dẫn để đăng xuất
# def logout():
#     session.pop('email', None)  # Xóa email khỏi session
#     session.pop('username', None)  # Xóa tên người dùng khỏi session
#     flash("Bạn đã đăng xuất thành công!", "success")
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)
import json
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Cấu hình secret key
app.secret_key = 'your_secret_key'  # Thay bằng một secret key mạnh

# Đường dẫn đến tệp JSON lưu trữ thông tin người dùng
users_file = 'users.json'

# Hàm để đọc dữ liệu người dùng từ tệp JSON
def load_users():
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return json.load(f)
    return {}

# Hàm để ghi dữ liệu người dùng vào tệp JSON
def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f)

# Đọc thông tin người dùng từ tệp
users = load_users()

@app.route('/')
def index():
    username = session.get('username')  # Lấy tên người dùng từ session
    return render_template('index.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Kiểm tra thông tin đăng nhập
        if email in users and check_password_hash(users[email]['password'], password):
            session['email'] = email  # Lưu email vào session
            session['username'] = users[email]['username']  # Lưu tên người dùng vào session
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('profile'))  # Chuyển đến trang hồ sơ
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
        real_name = request.form['real_name']  # Tên thật
        location = request.form['location']  # Địa điểm
        about_me = request.form['about_me']  # Giới thiệu bản thân
        
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
            'real_name': real_name,
            'location': location,
            'about_me': about_me
        }

        # Ghi thông tin người dùng vào tệp JSON
        save_users(users)

        flash("Đăng ký thành công!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# @app.route('/profile')  # Đường dẫn để hiển thị thông tin cá nhân
# def profile():
#     email = session.get('email')  # Lấy email người dùng từ session
#     if email and email in users:
#         user_info = users[email]
#         return render_template('profile.html', user_info=user_info)
#     flash("Bạn cần đăng nhập để xem trang này.", "warning")
#     return redirect(url_for('login'))
@app.route('/profile')  # Đường dẫn để hiển thị thông tin cá nhân
def profile():
    email = session.get('email')  # Lấy email người dùng từ session
    if email and email in users:
        user_info = users[email]
        return render_template('profile.html', user_info=user_info)
    flash("Bạn cần đăng nhập để xem trang này.", "warning")
    return redirect(url_for('login'))


@app.route('/logout')  # Đường dẫn để đăng xuất
def logout():
    session.pop('email', None)  # Xóa email khỏi session
    session.pop('username', None)  # Xóa tên người dùng khỏi session
    flash("Bạn đã đăng xuất thành công!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
