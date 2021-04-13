from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketIO = SocketIO(app, cors_allowed_origins="*")
conn = psycopg2.connect(
    host="ec2-34-230-149-169.compute-1.amazonaws.com",
    database="d7pml5pkjic32v",
    user="hpqvlmmjobbfyn",
    password="1eaf6697e7cb6c35fc065f42d18b3f81240c3207854405890f8269b4ce01e0de",
    port="5432"
)
cur = conn.cursor()
response_mimetype = 'application/json'


@socketIO.on('time')
def handle_timestamp(patient_timer_data_object):
    print(patient_timer_data_object)
    for patientEmail in patient_timer_data_object['patientEmail']:
        cur.execute("INSERT INTO time_tracker(start_time, end_time, total_seconds, total_active_seconds, patient_email, provider_email, jwt_token, screen_type, cpt_codes) VALUES (to_timestamp(CAST({0} as bigint)/1000), to_timestamp(CAST({1} as bigint)/1000), {2}, {3}, '{4}', '{5}', '{6}', '{7}', '{8}');".format(patient_timer_data_object['start_time'], patient_timer_data_object['end_time'], patient_timer_data_object['total_seconds'], patientEmail, patient_timer_data_object['providerEmail'],patient_timer_data_object['jwt'], patient_timer_data_object['screen_type'], patient_timer_data_object['cpt_codes']))
    conn.commit()
    print("Success")


if __name__ == '__main__':
    socketIO.run(app)
