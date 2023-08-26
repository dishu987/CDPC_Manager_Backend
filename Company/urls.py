from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('add/', views.CompanyAddView.as_view(), name='add_company'),
    path('list/', views.CompanyListView.as_view(), name='company_list'),
    path('filter-companies/', views.CompanyFilterAPIView.as_view(), name='company-filter'),
    path('details/', views.CompanyDetailsView.as_view(), name='company_details'),
    path('job-tags/', views.CompanyJobTagsView.as_view(), name='company_job_tags'),
    path('hiring-tags/', views.CompanyHiringTagsView.as_view(), name='company_hiring_tags'),
    path('comments/', views.CommentsListView.as_view(), name='company_comments'),
    path('comments/add/', views.AddCommentView.as_view(), name='add_comment'),
    path('comments/delete/<int:comment_id>', views.CommentDeleteAPIView.as_view(), name='delete_comment'),
    path('status/<int:pk>', views.CompanyStatusAPIView.as_view(), name='company_status'),
    path('blacklist/remove/<int:pk>', views.CompanyBlacklistRemoveAPIView.as_view(), name='company_blacklist_remove'),
    path('blacklist/add/<int:pk>', views.CompanyBlacklistAddAPIView.as_view(), name='company_blacklist_add'),
    path('download/', views.DownloadCompaniesAPIView.as_view(), name='download_companies'),
]