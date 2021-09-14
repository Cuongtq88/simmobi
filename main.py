from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Optional
import smtplib
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)
MK = os.environ.get("NEW_MK")
##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("postgresql://DATABASE_URL", "sqlite:///sim.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class SimSo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sothuebao = db.Column(db.String(250), nullable=False)
    sodinhdang = db.Column(db.String(250), nullable=False)
    gia = db.Column(db.Integer, nullable=False)
    khuyenmai = db.Column(db.String(250), nullable=True)
    dangso = db.Column(db.String(250), nullable=True)
    sohuu = db.Column(db.String(250), nullable=False)
class SimSoTraSau(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sothuebao = db.Column(db.String(250), nullable=False)
    sodinhdang = db.Column(db.String(250), nullable=False)
    goicuoc = db.Column(db.String(250), nullable=False)
    dangso = db.Column(db.String(250), nullable=False)

class GoiCuoc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tengoi = db.Column(db.String(250), nullable=False)
    gia = db.Column(db.Integer, nullable=False)
    ngaysudung = db.Column(db.Integer, nullable=False)
    giamgia = db.Column(db.Float, nullable=True)
    uudaichinh = db.Column(db.String(1000), nullable=False)
    uudaidata = db.Column(db.String(500), nullable=True)
    uudaithoai = db.Column(db.String(1000), nullable=True)
    nhom = db.Column(db.String(250), nullable=True)
    loai = db.Column(db.String(250), nullable=False)
    khuyenmai = db.Column(db.String(250), nullable=True)
    quatang = db.Column(db.String(250), nullable=True)
# db.create_all()

class ShowSimTT(FlaskForm):
    hoten = StringField('Họ tên:', validators=[DataRequired()])
    diachi = StringField('Địa chỉ:', validators=[DataRequired()])
    solienhe = StringField('Số điện thoại:', validators=[DataRequired()])

class ShowSimTS(FlaskForm):
    hoten = StringField('Họ tên:', validators=[DataRequired()])
    diachi = StringField('Địa chỉ:', validators=[DataRequired()])
    solienhe = StringField('Số điện thoại:', validators=[DataRequired()])
    goicuoc = StringField('Quý khách Chọn Gói Cước Nào', validators=[Optional()])
@app.route('/tratruoc/dathang',methods=["GET","POST"])
def show_tt():
    form = ShowSimTT()
    stb = request.args.get('stb')
    gia = int(request.args.get('gia'))
    if form.validate_on_submit():
        stb = request.args.get('stb')
        gia = request.args.get('gia')
        my_email = "donhangsimso@gmail.com"
        password = MK
        your_email = "cuongtq88@gmail.com"
        with smtplib.SMTP("smtp.gmail.com",587) as conection:
            msg = f"Khách hàng {form.hoten.data} \nĐịa chỉ {form.diachi.data} \nSố liên hệ {form.solienhe.data} \nSố mua {stb} \nGiá {gia}"
            subject = "Đơn hàng"
            conection.starttls()
            conection.login(my_email, password)
            fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'
            conection.sendmail(my_email, your_email,fmt.format(my_email,your_email,subject,msg).encode('utf-8'))
        return redirect(url_for('chotdontt'))
    return render_template('dathangtt.html', form =form, stb=stb, gia=gia)

@app.route('/goicuoc/dathang',methods=["GET","POST"])
def show_goicuoc():
    form = ShowSimTT()
    tengoi = request.args.get('tengoi')
    giagoi = request.args.get('giagoi')
    giagiam = request.args.get('giamgia')
    quatang = request.args.get('quatang')

    if form.validate_on_submit():
        tengoi = request.args.get('tengoi')
        giagoi = int(request.args.get('giagoi'))
        giagiam = request.args.get('giagiam')
        quatang = request.args.get('quatang')
        if giagiam != None:
            thanhtien = (giagoi - (giagoi * float(giagiam))) + 50000
        else:
            thanhtien = giagoi + 60000
        my_email = "donhangsimso.com"
        password = MK
        your_email = "cuongtq88@gmail.com"

        with smtplib.SMTP("smtp.gmail.com",587) as conection:
            msg = f"Khách hàng {form.hoten.data} \nĐịa chỉ {form.diachi.data} \nSố liên hệ {form.solienhe.data} \nGói Mua {tengoi} \nThành Tiền {thanhtien} "
            subject = "Đơn hàng"
            conection.starttls()
            conection.login(my_email, password)
            fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'
            conection.sendmail(my_email, your_email,fmt.format(my_email,your_email,subject,msg).encode('utf-8'))
        return redirect(url_for('chotdontt'))
    if giagiam == None:
        return render_template('datgoicuoc.html', form=form, tengoi=tengoi, giagoi=int(giagoi), quatang=quatang)
    return render_template('datgoicuoc.html', form=form, tengoi=tengoi, giagoi=int(giagoi), giagiam=float(giagiam), quatang=quatang)
@app.route('/')
def home():
    print("xxx")
    print(MK)
    return render_template('index.html')
@app.route('/zalo')
def contact():
    return render_template('zalo.html')

@app.route('/chotdontt')
def chotdontt():
    return render_template('chotdontt.html')

@app.route('/tracuuso')
def tracuu():
    return redirect(url_for('tratruoc'))

@app.route("/tratruoc", methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/tratruoc/<int:page>',methods=["GET","POST"])
def tratruoc(page):
    page = page
    pages = 10
    all_sim = SimSo.query.order_by(SimSo.gia.desc()).paginate(page,pages,error_out=False)
    if request.method == 'POST' and 'cars' in request.form and 'socantim' in request.form:
        socantim = request.form["socantim"]
        dangso = request.form["cars"]
        if dangso != "All" and socantim !="":
            search = "%{}%".format(socantim)
            all_sim = SimSo.query.filter(SimSo.sothuebao.like(search)).paginate(page, pages, error_out=False)
            print("aaa")
            return render_template('tratruoc.html', all_sim=all_sim, dangso="All", socantim="")
    if request.method == 'POST' and 'cars' in request.form:
        page = 1
        dangso = request.form["cars"]
        socantim = request.form["socantim"]
        dangso_ts = SimSo.query.filter_by(dangso=dangso).all()
        print(dangso_ts)
        if dangso != "All" and socantim == "":
            all_sim = SimSo.query.filter_by(dangso=dangso).paginate(page,pages,error_out=False)
        elif dangso == "All" and socantim == "":
            all_sim = SimSo.query.paginate(page,pages,error_out=False)
        elif socantim != "":
            socantim = request.form["socantim"]
            search = "%{}%".format(socantim)
            all_sim = SimSo.query.filter(SimSo.sothuebao.like(search)).paginate(page,pages,error_out=False)
        return render_template('tratruoc.html', all_sim=all_sim, dangso=dangso, socantim = socantim)
    dangso = request.args.get('dangso')
    socantim = request.args.get('socantim')
    if dangso != "" and dangso !=None and dangso != "All":
        all_sim = SimSo.query.filter_by(dangso=dangso).paginate(page, pages, error_out=False)
        return render_template('tratruoc.html', all_sim=all_sim, dangso=dangso)
    elif socantim != "" and socantim != None:
        search = "%{}%".format(socantim)
        all_sim = SimSo.query.filter(SimSo.sothuebao.like(search)).paginate(page, pages, error_out=False)
        return render_template('tratruoc.html', all_sim=all_sim, socantim=socantim)
    return render_template('tratruoc.html', all_sim = all_sim, dangso="All")


@app.route("/trasau", methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/tracuusotrasau/<int:page>',methods=["GET","POST"])
def trasau(page):
    page = page
    pages = 10
    all_sim = SimSoTraSau.query.filter_by(dangso="09").paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'cars' in request.form and 'socantim' in request.form:
        socantim = request.form["socantim"]
        dangso = request.form["cars"]
        if dangso == "All" and socantim !="":
            search = "%{}%".format(socantim)
            all_sim = SimSoTraSau.query.filter(SimSoTraSau.sothuebao.like(search)).paginate(page, pages, error_out=False)
            return render_template('trasau.html', all_sim_ts=all_sim, dangso="All", socantim=socantim)
        elif dangso != "All" and socantim != "":
            all_sim = SimSoTraSau.query.filter_by(dangso=dangso).paginate(page, pages, error_out=False)
            return render_template('trasau.html', all_sim_ts=all_sim, dangso=dangso, socantim="")
    if request.method == 'POST' and 'cars' in request.form:
        page = 1
        dangso = request.form["cars"]
        socantim = request.form["socantim"]
        if dangso != "All" and socantim == "":
            all_sim = SimSoTraSau.query.filter_by(dangso=dangso).paginate(page,pages,error_out=False)
        elif dangso == "All" and socantim == "":
            all_sim = SimSoTraSau.query.paginate(page,pages,error_out=False)
        elif socantim != "":
            socantim = request.form["socantim"]
            search = "%{}%".format(socantim)
            all_sim = SimSoTraSau.query.filter(SimSoTraSau.sothuebao.like(search)).paginate(page,pages,error_out=False)
        return render_template('trasau.html', all_sim_ts=all_sim, dangso=dangso, socantim = socantim)
    dangso = request.args.get('dangso')
    socantim = request.args.get('socantim')
    if dangso != "" and dangso !=None and dangso != "All":
        all_sim = SimSoTraSau.query.filter_by(dangso=dangso).paginate(page, pages, error_out=False)
        return render_template('trasau.html', all_sim_ts=all_sim, dangso=dangso)
    elif socantim != "" and socantim != None:
        search = "%{}%".format(socantim)
        all_sim = SimSoTraSau.query.filter(SimSoTraSau.sothuebao.like(search)).paginate(page, pages, error_out=False)
        return render_template('trasau.html', all_sim_ts=all_sim, socantim=socantim)
    return render_template('trasau.html', all_sim_ts = all_sim, dangso="All")

@app.route("/goicuoc", methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/tracuugoi/<int:page>',methods=["GET","POST"])
def goicuoc(page):
    page = page
    pages = 6
    all_goi = GoiCuoc.query.filter_by(khuyenmai="sales").paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'loaigoi' in request.form:
        loaigoi = request.form["loaigoi"]
        if loaigoi != "Phổ Biến":
            all_goi = GoiCuoc.query.filter_by(loai=loaigoi).paginate(page, pages, error_out=False)
        else:
            all_goi = GoiCuoc.query.filter_by(nhom="Phổ Biến").paginate(page, pages, error_out=False)
        return render_template('goicuoc.html', all_goi=all_goi, loaigoi=loaigoi)
    loaigoi = request.args.get('loaigoi')

    if loaigoi != "" and loaigoi !=None:
        print("aaa")
        all_goi = GoiCuoc.query.filter_by(loai=loaigoi).paginate(page, pages, error_out=False)
        return render_template('goicuoc.html', all_goi=all_goi, loaigoi=loaigoi)
    return render_template('goicuoc.html', all_goi=all_goi)

@app.route('/trasau/dathangts',methods=["GET","POST"])
def show_ts():
    form = ShowSimTS()
    stb = request.args.get('stb')
    goicuoc = request.args.get('goicuoc')
    if form.validate_on_submit():
        stb = request.args.get('stb')
        goicuoc = request.args.get('goicuoc')
        my_email = "donhangsimso@gmail.com"
        password = MK
        your_email = "cuongtq88@gmail.com"

        with smtplib.SMTP("smtp.gmail.com",587) as conection:
            msg = f"Khách hàng {form.hoten.data} \nĐịa chỉ {form.diachi.data} \nSố liên hệ {form.solienhe.data} \nSố mua {stb} \nGói Cước {goicuoc}"
            subject = "Đơn hàng Trả Sau"
            conection.starttls()
            conection.login(my_email, password)
            fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'
            conection.sendmail(my_email, your_email,fmt.format(my_email,your_email,subject,msg).encode('utf-8'))
        return redirect(url_for('chotdontt'))
    return render_template('dathangts.html', stb= stb, goicuoc=goicuoc, form=form)
if __name__ == "__main__":
    app.run(debug=True)