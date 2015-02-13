from django.dispatch import Signal

notify = Signal(providing_args=['receiver_user', 'msg', 'action', ])
