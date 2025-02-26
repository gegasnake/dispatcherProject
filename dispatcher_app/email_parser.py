import imaplib
import email
import re

# Account credentials
IMAP_SERVER = "imap.gmail.com"


def parse_email(email_text):
    """
    Extract order-related details from the email text.
    """
    data = {}

    # Extract Pick-Up Location
    pickup_match = re.search(r'Pick-Up\s*\*\s*(.*?)\*', email_text, re.DOTALL)
    if pickup_match:
        data['pickup_location'] = pickup_match.group(1).strip()

    # Extract Pick-Up Date
    pickup_date_match = re.search(r'Pick-Up.*?\*\s*.*?\*\s*(.*?)\s*Delivery', email_text, re.DOTALL)
    if pickup_date_match:
        data['pickup_date'] = pickup_date_match.group(1).strip()

    # Extract Delivery Location
    delivery_match = re.search(r'Delivery\s*\*\s*(.*?)\*', email_text, re.DOTALL)
    if delivery_match:
        data['delivery_location'] = delivery_match.group(1).strip()

    # Extract Delivery Date
    delivery_date_match = re.search(r'Delivery.*?\*\s*.*?\*\s*(.*?)\s*\d+ STOPS', email_text, re.DOTALL)
    if delivery_date_match:
        data['delivery_date'] = delivery_date_match.group(1).strip()

    # Extract Stops and Miles
    stops_miles_match = re.search(r'(\d+ STOPS, \d+ MILES)', email_text)
    if stops_miles_match:
        data['stops_miles'] = stops_miles_match.group(1).strip()

    # Extract Load Type
    load_type_match = re.search(r'\*Load Type: \*(.*?)\n', email_text)
    if load_type_match:
        data['load_type'] = load_type_match.group(1).strip()

    # Extract Vehicle Required
    vehicle_match = re.search(r'\*Vehicle required: \*(.*?)\n', email_text)
    if vehicle_match:
        data['vehicle_required'] = vehicle_match.group(1).strip()

    # Extract Pieces
    pieces_match = re.search(r'\*Pieces: \*(.*?)\n', email_text)
    if pieces_match:
        data['pieces'] = pieces_match.group(1).strip()

    # Extract Weight
    weight_match = re.search(r'\*Weight: \*(.*?)\n', email_text)
    if weight_match:
        data['weight'] = weight_match.group(1).strip()

    # Extract Dimensions
    dimensions_match = re.search(r'\*Dimensions: \*(.*?)\n', email_text)
    if dimensions_match:
        data['dimensions'] = dimensions_match.group(1).strip()

    # Extract Notes
    notes_match = re.search(r'\*Notes: \*(.*?)\n', email_text)
    if notes_match:
        data['notes'] = notes_match.group(1).strip()

    return data


def read_emails(user_email, imap_password):
    """
    Connect to the IMAP server using the provided email and password,
    read emails, and parse them.
    """
    try:
        myMail = imaplib.IMAP4_SSL(IMAP_SERVER)
        myMail.login(user_email, imap_password)
        myMail.select("Inbox")

        _, data = myMail.search(None, "ALL")
        mailIdList = data[0].split()
        parsed_orders = []

        for count in mailIdList:
            typ, data = myMail.fetch(count, '(RFC822)')
            for response in data:
                if isinstance(response, tuple):
                    myMsg = email.message_from_bytes(response[1])
                    for part in myMsg.walk():
                        if part.get_content_type() == 'text/plain':
                            parsed_data = parse_email(part.get_payload())
                            parsed_orders.append(parsed_data)

        myMail.close()
        myMail.logout()
        return parsed_orders
    except imaplib.IMAP4.error as e:
        print(f"IMAP login failed: {e}")
        raise Exception("Failed to connect to the email server")


