from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()


class PatientLookup(BaseModel):
    first_name: str
    last_name: str
    dob: str


@app.post("/patients/lookup")
def lookup_patient(data: PatientLookup):

    db = sqlite3.connect("Hospital_Data_Generator/hospital.db")

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT patient_id
        FROM patients
        WHERE first_name = ?
        AND last_name = ?
        AND dob = ?
        """,
        (
            data.first_name,
            data.last_name,
            data.dob
        )
    )

    patient = cursor.fetchone()

    db.close()

    if patient:
        return {
            "status": "returning",
            "patient_id": patient[0]
        }

    return {
        "status": "new",
        "patient_id": None
    }



class DoctorAvailability(BaseModel):
    specialty: str
    day: str
    duration_minutes: int


@app.post("/doctors/availability")
def doctor_availability(data: DoctorAvailability):

    db = sqlite3.connect("Hospital_Data_Generator/hospital.db")

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT doc_id,
               doctor_name,
               time_slot
        FROM doctor_schedule
        WHERE specialty = ?
        AND day_of_week = ?
        AND is_booked = 0
        """,
        (
            data.specialty,
            data.day
        )
    )

    slots = cursor.fetchall()

    db.close()

    return slots

class AppointmentBooking(BaseModel):
    patient_id: str
    doc_id: str
    time_slot: str


@app.post("/appointments/book")
def book_appointment(data: AppointmentBooking):

    db = sqlite3.connect("Hospital_Data_Generator/hospital.db")

    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE doctor_schedule
        SET is_booked = 1
        WHERE doc_id = ?
        AND time_slot = ?
        """,
        (
            data.doc_id,
            data.time_slot
        )
    )

    db.commit()

    db.close()

    return {
        "status": "success"
    }