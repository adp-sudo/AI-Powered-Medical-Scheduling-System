from faker import Faker
from transformers import pipeline
import pandas as pd
import random

fake = Faker()

generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)

patients = []

conditions = [
    "Hypertension",
    "Type 2 Diabetes",
    "Asthma",
    "GERD",
    "Hypothyroidism",
    "Anxiety",
    "Arthritis",
    "Migraine"
]

medications = [
    "Metformin",
    "Lisinopril",
    "Atorvastatin",
    "Levothyroxine",
    "Omeprazole",
    "Albuterol"
]

allergies = [
    "Penicillin",
    "Peanuts",
    "Latex",
    "Sulfa drugs",
    "No known allergies"
]

insurance_companies = [
    "LIC",
    "HDFC",
    "ICICI",
    "ACKO",
    "Max Life"
]


def generate_medical_history(age, gender):

    patient_conditions = random.sample(
        conditions,
        random.randint(1, 3)
    )

    patient_meds = random.sample(
        medications,
        random.randint(1, 2)
    )

    allergy = random.choice(allergies)

    prompt = f"""<|system|>
You are a medical records assistant.

Generate a realistic synthetic medical history.
Write 3-5 complete sentences.
Do not use bullet points.
Do not repeat the prompt.
</s>

<|user|>
Age: {age}
Gender: {gender}

Conditions: {', '.join(patient_conditions)}

Medications: {', '.join(patient_meds)}

Allergy: {allergy}
</s>

<|assistant|>
"""

    result = generator(
        prompt,
        max_new_tokens=120,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.2,
        truncation=True
    )

    generated_text = result[0]["generated_text"]

    history = generated_text.split("<|assistant|>")[-1].strip()

    if len(history) < 30:
        history = (
            f"The patient has a history of "
            f"{', '.join(patient_conditions)}. "
            f"Current medications include "
            f"{', '.join(patient_meds)}. "
            f"Known allergy: {allergy}."
        )

    return history


for i in range(1, 51):

    gender = random.choice(["Male", "Female"])

    dob = fake.date_of_birth(
        minimum_age=18,
        maximum_age=90
    )

    age = pd.Timestamp.today().year - dob.year

    medical_history = generate_medical_history(
        age,
        gender
    )

    profile = {
        "patient_id": f"P{i:03d}",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "dob": dob.strftime("%m/%d/%Y"),
        "gender": gender,
        "phone": fake.phone_number(),
        "email": fake.email(),
        "insurance_company": random.choice(insurance_companies),
        "member_id": fake.bothify(text="MEM#####"),
        "group_number": fake.bothify(text="GRP###"),
        "medical_history": medical_history
    }

    patients.append(profile)

patients_df = pd.DataFrame(patients)

patients_df.to_csv(
    "patients.csv",
    index=False
)

specialties = [
    "Cardiology",
    "Dermatology",
    "Orthopedics",
    "Neurology",
    "Pediatrics"
]

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]

time_slots = [
    "09:00 AM",
    "10:00 AM",
    "11:00 AM",
    "01:00 PM",
    "02:00 PM",
    "03:00 PM"
]

doctor_schedule = []

for doc_num in range(1, 11):

    doctor_name = f"Dr. {fake.name()}"
    specialty = random.choice(specialties)

    for day in days:
        for slot in time_slots:

            doctor_schedule.append({
                "doc_id": f"D{doc_num:03d}",
                "doctor_name": doctor_name,
                "specialty": specialty,
                "day_of_week": day,
                "time_slot": slot,
                "is_booked": random.choice(
                    [True, False]
                )
            })

doctor_df = pd.DataFrame(
    doctor_schedule
)

doctor_df.to_csv(
    "doctors_schedule.csv",
    index=False
)

print("Generated patients.csv")
print("Generated doctors_schedule.csv")
print(f"Patients: {len(patients_df)}")
print(f"Doctor slots: {len(doctor_df)}")