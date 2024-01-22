from django.db import models

#Raw Data
class Data(models.Model):
    date = models.DateTimeField()
    crude_stk = models.IntegerField()
    crude_stk_spr = models.IntegerField()
    gas_stk = models.IntegerField()
    dist_stk = models.IntegerField()

#Week-wise Data
class WeekWiseData(models.Model):
    week_no = models.IntegerField()
    year = models.IntegerField()
    stk = models.IntegerField() #will change depending on commodity selected

#Month-wise Data
class MonthWiseData(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    stk = models.FloatField()

#Week-wise Difference
class WeekWiseDifferenceData(models.Model):
    week_diff = models.CharField(max_length=10)
    year = models.IntegerField()
    stk = models.IntegerField() #will change depending on commodity selected

#Summer Analysis
class SummerData(models.Model):
    date = models.DateTimeField()
    stk = models.FloatField()

#Average min max 2023 analysis
class AggDataWeekMonth(models.Model):
    week_month = models.IntegerField()
    avg = models.FloatField()
    minimum = models.IntegerField()
    maximum = models.IntegerField()
    data_2023 = models.IntegerField()

#Monthwise builds and draws
class MonthwiseBuildDraw(models.Model):
    year = models.IntegerField()
    curr_month_stk = models.FloatField()
    prev_month_stk = models.FloatField()
    build_or_draw = models.CharField(max_length=1)

#Yearwise builds draws
class YearwiseBuildDraw(models.Model):
    date = models.DateTimeField()
    stk = models.IntegerField()
    diff = models.FloatField()

