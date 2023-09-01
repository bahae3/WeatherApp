from pprint import pprint
import requests
import smtplib
from flask import Flask, render_template, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bahae03'


def custom_date_format(value, input_format, output_format):
    parsed_date = datetime.strptime(value, input_format)
    formatted_date = parsed_date.strftime(output_format)
    return formatted_date


app.jinja_env.filters['custom_date_format'] = custom_date_format


class CityName(FlaskForm):
    city = StringField("The city name: ", validators=[DataRequired()])
    days = StringField("N° of days (1-10): ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LatAndLong(FlaskForm):
    latitude = StringField("Latitude: ", validators=[DataRequired()])
    longitude = StringField("Longitude: ", validators=[DataRequired()])
    days = StringField("N° of days (1-10): ", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ContactUs(FlaskForm):
    send_us_msg = TextAreaField("Type in your message:", validators=[DataRequired()])
    send = SubmitField("Send 📩")


API_URL_CURRENT = 'https://api.weatherapi.com/v1/current.json'
API_URL_DAYS = 'https://api.weatherapi.com/v1/forecast.json'
API_KEY = '8caf0227291b44ef9b4121126232608'
EMAIL = "bahaeassaoui23@gmail.com"
PASSWORD = "snpqzggucxxypshf"


@app.route("/", methods=['POST', 'GET'])
def home():
    city_form = CityName()
    lat_and_long_form = LatAndLong()
    if city_form.validate_on_submit():
        city = city_form.data.get('city')
        days = int(city_form.data.get('days'))
        session['user_days_input'] = days
        if days == 1:
            response = requests.get(f"{API_URL_CURRENT}?key={API_KEY}&q={city.capitalize()}").json()
            session['city_data'] = response
            return redirect(url_for('success'))
        elif 1 < days <= 10:
            response = requests.get(f"{API_URL_DAYS}?key={API_KEY}&q={city.capitalize()}&days={days}").json()
            for data_item in response["forecast"]["forecastday"]:
                data_item.pop("hour", None)
                data_item.pop("astro", None)
            session['city_data'] = response
            return redirect(url_for('success'))
        else:
            return redirect(url_for('failed'))
    elif lat_and_long_form.validate_on_submit():
        latitude = round(float(lat_and_long_form.data.get('latitude')), 4)
        longitude = round(float(lat_and_long_form.data.get('longitude')), 4)
        days = int(lat_and_long_form.data.get('days'))
        session['user_days_input'] = days
        if days == 1:
            response = requests.get(f"{API_URL_CURRENT}?key={API_KEY}&q={latitude},{longitude}").json()
            session['lat_and_long'] = response
            return redirect(url_for('success'))
        elif 1 < days <= 10:
            response = requests.get(f"{API_URL_DAYS}?key={API_KEY}&q={latitude},{longitude}&days={days}").json()
            for data_item in response["forecast"]["forecastday"]:
                data_item.pop("hour", None)
                data_item.pop("astro", None)
            session['lat_and_long'] = response
            return redirect(url_for('success'))
        else:
            return redirect(url_for('failed'))
    return render_template('home.html', form1=city_form, form2=lat_and_long_form)


@app.route("/success")
def success():
    city_data = session.get('city_data')
    l_data = session.get('lat_and_long')
    user_days_input = session.get('user_days_input')
    if city_data:
        if user_days_input == 1:
            city_name = city_data['location']['name']
            country = city_data['location']['country']
            temp = city_data['current']['temp_c']
            condition = city_data['current']['condition']['text']
            condition_photo = city_data['current']['condition']['icon']
            user_d = user_days_input
            session.clear()
            return render_template('success.html', city=city_name, country=country, temperature=temp,
                                   weather_condition=condition, weather_icon=condition_photo, user_days=user_d)
        elif user_days_input > 1:
            city_name = city_data['location']['name']
            country = city_data['location']['country']
            user_d = user_days_input
            session.clear()
            return render_template("success.html", weather_days=city_data, city=city_name,
                                   country=country, user_days=user_d)
    elif l_data:
        if user_days_input == 1:
            city_name = l_data['location']['name']
            country = l_data['location']['country']
            temp = l_data['current']['temp_c']
            condition = l_data['current']['condition']['text']
            condition_photo = l_data['current']['condition']['icon']
            user_d = user_days_input
            session.clear()
            return render_template('success.html', city=city_name, country=country, temperature=temp,
                                   weather_condition=condition, weather_icon=condition_photo, user_days=user_d)
        elif user_days_input > 1:
            city_name = l_data['location']['name']
            country = l_data['location']['country']
            user_d = user_days_input
            session.clear()
            return render_template("success.html", weather_days=l_data, city=city_name,
                                   country=country, user_days=user_d)
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
    if form.validate_on_submit():
        message = form.data.get('send_us_msg')
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(EMAIL, PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs="bahaeddiine12@gmail.com",
                msg=f"Subject:Weather app message.\n\n{message}"
            )
        return redirect(url_for('home'))
    return render_template("contactus.html", form=form)


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


if __name__ == '__main__':
    app.run(debug=True)
