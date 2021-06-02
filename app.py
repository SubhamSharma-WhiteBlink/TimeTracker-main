from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketIO = SocketIO(app, cors_allowed_origins="*")
conn = psycopg2.connect(
    host="ec2-35-174-35-242.compute-1.amazonaws.com",
    database="d91ofjqab30922",
    user="pcvevvbafeeklx",
    password="1068584413e6fb20c45fff08b6563bd55b1618a4530ea6fdb2d115181246aa30",
    port="5432"
)
cur = conn.cursor()
response_mimetype = 'application/json'
print("Success")


@socketIO.on('time')
def handle_timestamp(patient_timer_data_object):
    print(patient_timer_data_object)
    if patient_timer_data_object['type'] == "INSERT_TIME":
        for patientEmail in patient_timer_data_object['patientEmail']:
            cur.execute("INSERT INTO time_tracker(start_time, end_time, total_seconds, total_active_seconds, patient_email, provider_email, jwt_token, screen_type, cpt_codes) VALUES (to_timestamp(CAST({0} as bigint)/1000), to_timestamp(CAST({1} as bigint)/1000), {2}, {3}, '{4}', '{5}', '{6}', '{7}', '{8}');".format(patient_timer_data_object['start_time'], patient_timer_data_object['end_time'], patient_timer_data_object['total_seconds'], patient_timer_data_object['total_active_seconds'],patientEmail, patient_timer_data_object['providerEmail'],patient_timer_data_object['jwt'], patient_timer_data_object['screen_type'], patient_timer_data_object['cpt_codes']))
    conn.commit()
    print("Success")


if __name__ == '__main__':
    socketIO.run(app)
