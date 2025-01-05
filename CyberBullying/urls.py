from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path("Register.html", views.Register, name="Register"),
	       path("Login.html", views.Login, name="Login"),
	       path("Admin.html", views.Admin, name="Admin"),
	       path("Signup", views.Signup, name="Signup"),
	       path("UserLogin", views.UserLogin, name="UserLogin"),
	       path("AdminLogin", views.AdminLogin, name="AdminLogin"),
	       path("ViewUsers.html", views.ViewUsers, name="ViewUsers"),
	       path("AddCyberMessages.html", views.AddCyberMessages, name="AddCyberMessages"),
	       path("RunAlgorithms.html", views.RunAlgorithms, name="RunAlgorithms"),
	       path("RunAlgorithm", views.RunAlgorithm, name="RunAlgorithm"),
	       path("MonitorPost.html", views.MonitorPost, name="MonitorPost"),
	       path("AddBullyingWords", views.AddBullyingWords, name="AddBullyingWords"),
	       path("SendPost.html", views.SendPost, name="SendPost"),
	       path("PostSent", views.PostSent, name="PostSent"),
	       path("ViewUserPost.html", views.ViewUserPost, name="ViewUserPost"),
]