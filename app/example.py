from django.contrib.auth import get_user_model

User = get_user_model()

instance = User.objects.create() # save User data in the database

instance.save()

instance.delete()
