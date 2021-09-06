from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

@app.route('/')
def home():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)