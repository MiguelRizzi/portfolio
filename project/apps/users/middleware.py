from users.models import Message
from users.models import Review

class UnreadMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        unread_messages_count = Message.objects.filter(is_read=False).count()
        unapproved_reviews_count = Review.objects.filter(is_approved=False).count()
        total_count =unapproved_reviews_count + unread_messages_count
        request.unread_messages_count = unread_messages_count
        request.unapproved_reviews_count = unapproved_reviews_count
        request.total_count = total_count
        response = self.get_response(request)
        return response