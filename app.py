from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/Home")
def home2():
    return render_template('home.html')

@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404

@app.route("/Login")
def Login():
    return render_template('Login.html')

@app.route("/Registration")
def Registration():
    return render_template('Registration.html')

if __name__ == '__main__':
  app.run(debug=True)

