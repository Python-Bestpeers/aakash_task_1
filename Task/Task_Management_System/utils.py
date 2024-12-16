from django.conf import settings
from django.core.mail import send_mail


def send_update_mail(task):
    try:
        subject = "Task Assigned"
        message = f"""Task : {task.title},
                    Description: {task.description},
                    Assigned By: {task.assigned_by.first_name},
                    Priority: {task.priority}
                    Start Date: {task.start_date},
                    End Date: {task.end_date},
                    Current Status:{task.status}
        """
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [task.assigned_to.email]
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception:
        return False


def send_update_status(task):
    try:
        subject = "Task Status Update"
        message = f"""
        Task: {task.title},
        Description: {task.description},
        Assigned By: {task.assigned_by.first_name},
        Priority: {task.priority},
        Start Date: {task.start_date},
        End Date: {task.end_date},
        Current Status: {task.status}
        """
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [task.assigned_by.email]

        if not recipient_list:
            print("Recipient list is empty. Email not sent.")
            return False

        send_mail(subject, message, email_from, recipient_list)
        print("Email sent successfully.")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
