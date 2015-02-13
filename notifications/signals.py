from django.dispatch import Signal

notify = Signal(providing_args = ['sender', 'receiver_user', 'action',])
