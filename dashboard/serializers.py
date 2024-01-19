from rest_framework import serializers
from .models import Data, WeekWiseData, MonthWiseData, WeekWiseDifferenceData, SummerData

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

class WeekwiseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekWiseData
        fields = ['id', 'week_no', 'year', 'stk']

class MonthwiseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthWiseData
        fields = ['id', 'month', 'year', 'stk']

class WeekWiseDifferenceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekWiseDifferenceData
        fields = ['id', 'week_diff', 'year', 'stk']

class SummerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummerData
        fields = ['id', 'date', 'stk']
    
