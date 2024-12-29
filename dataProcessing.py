import smtplib as smtp
from email.mime.text import MIMEText
from datetime import datetime

EMAIL = "hythamhex@gmail.com"
PASSWORD = "sklp rlgf ijsh gvju"

def check_data(data):
    checks_list = {
        "data_incomplete": True if len(data) < 15 else False,
        "total_score": sum([int(x) for x in data.values() if x.isdigit()]) - (int(data["age"]) if "age" in data else 0),
        "name": data["name"],
        "age": data["age"] if "age" in data else 0,
        "email": data["email"],

        "chills_sweating": int(data["chills_sweating"]) if "chills_sweating" in data else 0,
        "chronic_illnesses": int(data["chronic_illnesses"]) if "chronic_illnesses" in data else 0,
        "close_contact": int(data["close_contact"]) if "close_contact" in data else 0,
        "cough": int(data["cough"]) if "cough" in data else 0,
        "diarrhea": int(data["diarrhea"]) if "diarrhea" in data else 0,
        "fatigue": int(data["fatigue"]) if "fatigue" in data else 0,
        "fever": int(data["fever"]) if "fever" in data else 0,
        "flu_vaccine": int(data["flu_vaccine"]) if "flu_vaccine" in data else 0,
        "headaches_eyes": int(data["headaches_eyes"]) if "headaches_eyes" in data else 0,
        "nasal_congestion": int(data["nasal_congestion"]) if "nasal_congestion" in data else 0,
        "nausea": int(data["nausea"]) if "nausea" in data else 0,
        "shortness_breath": int(data["shortness_breath"]) if "shortness_breath" in data else 0,
        "sore_throat": int(data["sore_throat"]) if "sore_throat" in data else 0,
        "symptom_length": int(data["symptom_length"]) if "symptom_length" in data else 0,
        "symptom_worse": int(data["symptom_worse"]) if "symptom_worse" in data else 0,

        "message_body": ""
    }

    if checks_list["data_incomplete"]:
        checks_list["message_body"] += "It seems like you have left a few fields empty, but it's okay, we can still help you out. "
    
    checks_list["message_body"] += f"""Based on the information you have provided, we have calculated a total RISK score of {checks_list["total_score"]} out of 41 (the lower, the better). """

    if 7 <= checks_list["total_score"] <= 10:
        checks_list["message_body"] += ("It doesn't look like you have flu or any other viral illness, but you always consult your doctor often given how you suffer from a cronic illness. " if checks_list["cronic_illnesses"] == 1 else "You seem to be healthy! Nonetheless, it's always good to keep an eye on your health!! ")
    else:
        # now we check if they have any of the symptoms... these aren't well defined, so we'll just use some arbitrary values
        if checks_list["fever"] <= 2 and (checks_list["cough"] == 2 or checks_list["shortness_breath"] == 2 or checks_list["sore_throat"] == 2) and checks_list["fatigue"] == 2:
            checks_list["message_body"] += "You seem to be showing symptoms of a viral illness. Please consult your doctor immediately."

        elif checks_list["fever"] >= 2 and (checks_list["cough"] == 3 or checks_list["nasal_congestion"] >= 2 or checks_list["headaches_eyes"] >= 2) and checks_list["fatigue"] == 2:
            checks_list["message_body"] += "You seem to be showing symptoms of COVID-19. Please consult your doctor immediately."

        elif checks_list["nausea"] == 1 or checks_list["diarrhea"] == 1 and checks_list["fatigue"] >= 3:
            checks_list["message_body"] += "You might be having stomach flu... Please consult your doctor immediately."

        elif 0 < checks_list["symptom_length"] <= 2 and checks_list["symptom_worse"] == 1 and checks_list["fatigue"] == 4 and checks_list["headaches_eyes"] == 4:
            checks_list["message_body"] += "You seem to be showing symptoms of a viral illness. Please consult your doctor immediately."

        elif 0 < checks_list["symptom_length"] == 3 or checks_list["symptom_worse"] == 2 and checks_list["fatigue"] == 4 and checks_list["total_score"] >= 32 and checks_list["chronic_illnesses"] == 1:
            checks_list["message_body"] += "Your situation needs urgent attention!!! Consult your doctor immediately."

        elif checks_list["symptom_worse"] == 2 and 20 <= checks_list["total_score"] <= 25:
            checks_list["message_body"] += "Your symptoms seem to be getting worse. Please consult your doctor immediately."

        elif checks_list["symptom_worse"] == 2 and checks_list["total_score"] >= 26:
            checks_list["message_body"] += "Your symptoms seem to be getting worse. Please consult your doctor immediately."

        else:
            checks_list["message_body"] += "There are signs of tiredness and fatigue, but it doesn't seem to be anything serious. However, it's always good to consult your doctor."

    print(checks_list["message_body"])
    return checks_list




def send_email(data):
    date_today = datetime.now().strftime("%d/%m/%Y")

    message = MIMEText(f"""Hello {data["name"]},\n\n
    We have received your health survey results for {date_today}.\n
    {data["message_body"]}\n\n
    Best regards,\n
    The Health Survey Team""")

    message["Subject"] = "Health Survey Results"
    message["From"] = EMAIL
    message["To"] = data["email"]

    try:

        with smtp.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, data["email"], message.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")






