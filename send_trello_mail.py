import sys
import datetime
import smtplib
from trello import TrelloClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_list_of_cards(listname):
    card_name_list = {}
    client = TrelloClient(
        api_key    = '#####################################',
        api_secret = '#####################################'
    )
    all_boards = client.list_boards()
    last_board = all_boards[0]
    all_lists = last_board.list_lists()
    for list in all_lists:
        if list.name == listname :
            all_cards = list.list_cards()
            for card in all_cards:
                card_name_list[card.name] = listname
    return card_name_list


def send_mail(sender_address, sender_pass, receiver_address, mail_Subject, mail_content):
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = mail_Subject   

    message.attach(MIMEText(mail_content, 'html'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls() 
    session.login(sender_address, sender_pass) 
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


def get_content_for_availability_mail():
    mail_content_data = {}
    mail_content_data["Date"] = str(datetime.date.today())
    mail_content_data["Availability"] = "11:00 P.M. to 8:00 P.M."
    mail_content_data["Mode of Availability"] = "Call, Slack, Whatsapp, Email, Zoom, Meet"
    in_progress_tasks = get_list_of_cards("In Progress") 
    to_be_started_tasks = get_list_of_cards("To Be Started")
    mail_content_data["Tasks"] = { **in_progress_tasks, **to_be_started_tasks }
    return mail_content_data


def get_content_for_daily_status_mail():
    mail_content_data = {}
    mail_content_data["Date"] = str(datetime.date.today())
    in_progress_tasks = get_list_of_cards("In Progress") 
    done_tasks = get_list_of_cards("Done")
    mail_content_data["Tasks"] = { **done_tasks, **in_progress_tasks}
    return mail_content_data


def send_availability_mail(sender_address, sender_pass, receiver_address):
    mail_Subject = "Availability mail | " + str(datetime.date.today())
    mail_content_data = get_content_for_availability_mail()
    mail_content_body = """ <tr>
                                <th>Tasks</th>
                                <th>Status</th>
                            </tr>
                        """
    for task in mail_content_data["Tasks"] :
        mail_content_body += """<tr>
                                    <td>"""+ task +"""</td>
                                    <td>"""+ mail_content_data["Tasks"][task] + """</td>
                                <tr>
                            """
    mail_content = """<html>
    <head>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 5px;
            }
            th {
                background-color: #7FFFD4;
                color: black;
            }
            td {
                text-align: left;
            }
        </style>
    </head>
    <body>
        <p>Hi Team,<br>
        This will be my today's work schedule,
        </p>
        <table>
            <tr>
                <th>Availability</th>
                <td>""" + mail_content_data["Availability"] + """</td>
            </tr>
            <tr>
                <th>Mode of Availability</th>
                <td>""" + mail_content_data["Mode of Availability"] + """</td>
            </tr>
            <tr>
                <th>Date</th>
                <td>""" + mail_content_data["Date"] + """</td>
            </tr>
        </table>
        <p></p>
        <table>
""" + mail_content_body + """
        </table>
        <p>Thanks and regards,<br>
        Nishant Prakash
        </p>
</body>
</html>
    """
    send_mail(sender_address, sender_pass, receiver_address, mail_Subject, mail_content)


def send_daily_status_mail(sender_address, sender_pass, receiver_address):
    mail_Subject = "Daily Status mail | " + str(datetime.date.today())
    mail_content_data = get_content_for_daily_status_mail()
    mail_content_body = """ <tr>
                                <th>Tasks</th>
                                <th>Status</th>
                            </tr>
                        """
    for task in mail_content_data["Tasks"] :
        mail_content_body += """<tr>
                                    <td>"""+ task +"""</td>
                                    <td>"""+ mail_content_data["Tasks"][task] + """</td>
                                <tr>
                            """
    mail_content = """<html>
    <head>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 5px;
            }
            th {
                background-color: #7FFFD4;
                color: black;
            }
            td {
                text-align: left;
            }
        </style>
    </head>
    <body>
        <p>Hi Team,<br>
        Please find my daily status below,
        </p>
        <table>
            <tr>
                <th>Date</th>
                <td>""" + mail_content_data["Date"] + """</td>
            </tr>
        </table>
        <p></p>
        <table>
""" + mail_content_body + """
        </table>
        <p>Thanks and regards,<br>
        Nishant Prakash
        </p>
</body>
</html>
    """
    send_mail(sender_address, sender_pass, receiver_address, mail_Subject, mail_content)

def main():
    mail_type = str(sys.argv[1])
    sender_address    = '###############################'
    sender_pass       = '###############################'
    receiver_address  = '###############################'
    #receiver_address = '###############################'

    if mail_type == "a":
        send_availability_mail(sender_address, sender_pass, receiver_address)
    elif mail_type == "d":
        send_daily_status_mail(sender_address, sender_pass, receiver_address)
    else:
        print("Argument must be passed as either 'a'(availability) or 'd'(daily status) ")


if __name__ == "__main__":
    main()
