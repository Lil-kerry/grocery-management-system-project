from rest_framework import serializers

class SMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    message = serializers.CharField(max_length=160)
    carrier = serializers.ChoiceField(choices=[('safaricom', 'Safaricom'), ('telkom', 'Telkom'), ('airtel', 'Airtel')])
