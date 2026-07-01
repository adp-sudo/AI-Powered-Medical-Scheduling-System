from AI_Hospital_Scheduler.ai.tools import lookup_patient

result = lookup_patient.invoke(

    {

        "first_name": "David",

        "last_name": "Smith",

        "dob": "04/11/1967"

    }

)

print(result)