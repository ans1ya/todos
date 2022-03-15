from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('mytodos',views.TodosViewset,basename='mytodos')
router.register('modeltodos',views.TodosModelViewset,basename='modelview')

urlpatterns=[
    path('todos/',views.TodosView.as_view()),
    # api/v1/todos/{id}
     path('todos/<int:id>',views.TodoDetails.as_view()),
    path('mixins/todos/',views.TodosMixinView.as_view()),
    path('mixins/todos/<int:id>',views.TodosDetailMixin.as_view()),
    path('accounts/signup/',views.UsercreationView.as_view()),

]+router.urls