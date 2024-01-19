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