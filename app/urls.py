from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("<int:author_id>/", views.author_detail, name="author detail"),
    path("add_textbook/", views.add_textbook, name = "add_textbook"),
    path("delete_textbook/", views.delete_textbook, name = "delete textbook"),
    path("textbooks/<int:textbook_id>/", views.textbook, name = "textbook"),
    path("edit_textbooks/<int:textbook_id>/", views.edit_textbook, name = "edit textbook"),
    path("edit_chapters/<int:chapter_id>/", views.edit_chapter, name = "edit chapter"),
    path("chapters/<int:chapter_id>", views.chapter, name='chapter'),
    path("add_chapter/", views.add_chapter, name = "add chapter"),
    path("delete_chapter/", views.delete_chapter, name = "delete chapter"),
    path("download_chapter/<int:chapter_id>", views.download_chapter, name = "download chapter"),
    path("publish_chapter/<int:chapter_id>", views.publish_chapter, name = "publish chapter"),
    path("unpublish_chapter/<int:chapter_id>", views.unpublish_chapter, name = "unpublish chapter"),
    path("chapter_responses/<int:chapter_id>/", views.chapter_response, name = "chapter response"),
    path("chapter_summaries/<int:chapter_id>/", views.chapter_summary, name = "chapter summary"),
    path("chapter_matrix/<int:chapter_id>/", views.chapter_matrix, name = "chapter matrix"),

]