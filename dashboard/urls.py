"""
URL configuration for dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dashboard import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('raw/', views.raw_chart_basic),
    path('raw/weekwise/', views.raw_chart_weekwise),
    path('raw/monthwise/', views.raw_chart_monthwise),
    #path('raw/percentage/', views.raw_chart_percentage),
    path('raw/percentage/yearly/', views.raw_chart_percentage_yearly),
    path('simple/weekwise_diff/', views.simple_chart_weekwise_diff),
    path('simple/summer_analysis/', views.simple_chart_summer_analysis),
    path('simple/aggregate_analysis/weekwise/', views.simple_chart_weekwise_aggregations),
    path('simple/aggregate_analysis/monthwise/', views.simple_chart_monthwise_aggregations),
    path('advanced/build_draw/monthwise/', views.advanced_chart_build_draw_curr_prev_month),
    path('advanced/build_draw/yearwise/', views.advanced_chart_build_draw_years),
    path('advanced/build_draw/percentage/', views.advanced_chart_build_draw_percentage),
    path('advanced/build_draw/percentage/weekly/', views.advanced_chart_build_draw_percentage_weekly)
]

