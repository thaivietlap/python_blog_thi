from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Thay bằng một secret key mạnh

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = 'remember' in request.form

        # Giả lập kiểm tra thông tin đăng nhập
        if email == "test@example.com" and password == "password":
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('index'))
        else:
            flash("Thông tin đăng nhập không hợp lệ. Vui lòng thử lại.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

