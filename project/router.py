from app.api.viewsets import userviewsets
from rest_framework import routers
 
router = routers.DefaultRouter()
router.register('app', userviewsets, basename ='user_api')