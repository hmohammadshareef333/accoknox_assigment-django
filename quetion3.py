#Question 3: By default do django signals run in the same database transaction as the caller? Please support your answer with a code snippet that conclusively proves your stance. 
# The code does not need to be elegant and production ready, we just need to understand your logic.
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# Define a simple model
class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()

@receiver(post_save, sender=UserProfile)
def user_profile_saved_handler(sender, instance, **kwargs):
    print("Signal received for UserProfile:", instance.username)
    # Simulate a condition that raises an error
    if instance.username == "invalid_user":
        raise ValidationError("Invalid username!")

# Function to save a user profile
def save_user_profile(username):
    try:
        with transaction.atomic():  # Start a transaction
            user_profile = UserProfile(username=username, email=f"{username}@example.com")
            user_profile.save()  # This will trigger the post_save signal
            print("User Profile saved:", user_profile.username)
    except ValidationError as e:
        print("Error occurred:", e)

# Test with a valid username
print("Testing with valid username:")
save_user_profile("valid_user")

# Test with an invalid username
print("\nTesting with invalid username:")
save_user_profile("invalid_user")
