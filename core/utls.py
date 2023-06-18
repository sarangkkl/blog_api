from django.core.mail import send_mail





def response_structure(data, status, message,error,total_pages=None,page_number=None)->dict:
    """
        This function will enforce a standard response structure for all the API responses
    """
    response = {
        'data': data,
        'status': status,
        'message': message,
        'error':error,
        
    }

    if total_pages is not None:
        response['total_pages'] = total_pages
    if page_number is not None:
        response['page_number'] = page_number
    
    return response


class Notification:
    def __init__(self,recipient:str,message:str,) -> None:
        self.recipient = recipient
        self.message = message
    
    def send(self):
        send_mail(
        "Subject here",
        "Here is the message.",
        "gauravsah674@gmail.com",
        ["sarangkkl2@example.com"],
        fail_silently=False,)
        pass