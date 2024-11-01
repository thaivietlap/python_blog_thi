from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Thay bằng một secret key mạnh

# Giả lập cơ sở dữ liệu người dùng
users = {}

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
        if email in users and users[email]['password'] == password:
            session['username'] = users[email]['username']  # Lưu tên người dùng vào session
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
        users[email] = {'username': username, 'password': password}
        flash("Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')  # Đường dẫn để đăng xuất
def logout():
    session.pop('username', None)  # Xóa tên người dùng khỏi session
    flash("Bạn đã đăng xuất thành công!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
