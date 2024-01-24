from rest_framework import serializers
from .models import *
from .models import Data

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ['id', 'date', 'crude_stk', 'crude_stk_spr', 'gas_stk', 'dist_stk']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['Date'] = data.pop('date')
        data['EIA US CRUDE STK'] = data.pop('crude_stk')
        data['EIA US CRUDE STK SPR'] = data.pop('crude_stk_spr')
        data['EIA US GAS STK'] = data.pop('gas_stk')
        data['EIA US DIST STK'] = data.pop('dist_stk')

        return data

class PercentageYearlySerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentageYearly
        fields = ['id', 'year', 'spr_per', 'gas_per', 'dist_per']

class WeekwiseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekWiseData
        fields = ['id', 'week_no', 'year', 'stk']

class MonthwiseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthWiseData
        fields = ['id', 'month', 'year', 'stk']

class PercentageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentageData
        fields = ['id', 'date', 'spr_per', 'gas_per', 'dist_per']

class WeekWiseDifferenceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekWiseDifferenceData
        fields = ['id', 'week_diff', 'year', 'stk']

class SummerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummerData
        fields = ['id', 'date', 'stk']

class AggDataWeekMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = AggDataWeekMonth
        fields = ['id', 'week_month', 'avg', 'minimum', 'maximum', 'data_2023']

class MonthwiseBuildDrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthwiseBuildDraw
        fields = ['id', 'year', 'curr_month_stk', 'prev_month_stk', 'build_or_draw']

class YearwiseBuildDrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearwiseBuildDraw
        fields = ['id', 'date', 'stk', 'diff']

class BuildDrawPercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildDrawPercentage
        fields = ['id', 'month', 'build_per', 'draw_per']

class BuildDrawPercentageWeeklySerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildDrawPercentageWeekly
        fields = ['id', 'week', 'build_per', 'draw_per']