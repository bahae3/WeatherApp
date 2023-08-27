import requests
from flask import Flask, render_template, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bahae03'


class CityName(FlaskForm):
    city = StringField("The city name: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LatAndLong(FlaskForm):
    latitude = StringField("Latitude: ", validators=[DataRequired()])
    longitude = StringField("Longitude: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ContactUs(FlaskForm):
    send_us_msg = TextAreaField("Type in your message:", validators=[DataRequired()])
    send = SubmitField("Send 📩")


API_URL = 'https://api.weatherapi.com/v1/current.json'
API_KEY = '8caf0227291b44ef9b4121126232608'


@app.route("/", methods=['POST', 'GET'])
def home():
    city_form = CityName()
    lat_and_long_form = LatAndLong()
    if city_form.validate_on_submit():
        city = city_form.data.get('city')
        response = requests.get(f"{API_URL}?key={API_KEY}&q={city.capitalize()}").json()
        session['city_data'] = response
        return redirect(url_for('success'))
    elif lat_and_long_form.validate_on_submit():
        latitude = round(float(lat_and_long_form.data.get('latitude')), 4)
        longitude = round(float(lat_and_long_form.data.get('longitude')), 4)
        response = requests.get(f"{API_URL}?key={API_KEY}&q={latitude},{longitude}").json()
        session['lat_and_long'] = response
        return redirect(url_for('success'))
    return render_template('home.html', form1=city_form, form2=lat_and_long_form)


@app.route("/success")
def success():
    city_data = session.get('city_data')
    l_data = session.get('lat_and_long')
    if city_data:
        city_name = city_data['location']['name']
        country = city_data['location']['country']
        temp = city_data['current']['temp_c']
        condition = city_data['current']['condition']['text']
        condition_photo = city_data['current']['condition']['icon']
        session['city_data'] = None
        return render_template('success.html', city=city_name, country=country, temperature=temp,
                               weather_condition=condition, weather_icon=condition_photo)
    elif l_data:
        city_name = l_data['location']['name']
        country = l_data['location']['country']
        temp = l_data['current']['temp_c']
        condition = l_data['current']['condition']['text']
        condition_photo = l_data['current']['condition']['icon']
        session['lat_and_long'] = None
        return render_template('success.html', city=city_name, country=country, temperature=temp,
                               weather_condition=condition, weather_icon=condition_photo)
    else:
        return render_template('failed.html')


@app.route("/failed")
def failed():
    return render_template('failed.html')


@app.route("/ourteam")
def ourteam():
    return render_template("ourteam.html")


@app.route("/contactus", methods=['POST', 'GET'])
def contactus():
    form = ContactUs()
    return render_template("contactus.html", form=form)


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


if __name__ == '__main__':
    app.run(debug=True)
