#Question 2: Do django signals run in the same thread as the caller? Please support your answer with a code snippet that conclusively proves your stance.
# The code does not need to be elegant and production ready, we just need to understand your logic.
import threading
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User )
def user_saved_handler(sender, instance, **kwargs):
    print(f"Signal received in thread: {threading.current_thread().name}")
    # Simulate a long-running task
    time.sleep(2)
    print("Signal processing done in thread:", threading.current_thread().name)

# Simulating saving a user instance
def save_user():
    print(f"Saving user in thread: {threading.current_thread().name}")
    user = User(username='test_user')
    user.save()
    print("User  saved in thread:", threading.current_thread().name)

# Create a new thread to save the user
user_thread = threading.Thread(target=save_user, name='User Thread')
user_thread.start()
user_thread.join()

print("Main thread:", threading.current_thread().name)
