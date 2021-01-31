from rest_framework import serializers
from buspark.models import Driver, Bus


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ('name', 'bus_model', 'year_of_prod', 'velocity')


class DriverSerializer(serializers.ModelSerializer):
    bus = BusSerializer(many=True)
    class Meta:
        model = Driver
        fields = ('id', 'name', 'surname', 'date_of_birth', 'bus', 'age')
        depth = 1

    def create(self, validated_data):
        bus_data = validated_data.pop('bus')
        driver = Driver.objects.create(**validated_data)
        for bus in bus_data:
            try:
                current_bus = Bus.objects.get(name=bus['name'],
                                              bus_model=bus['bus_model'],
                                              year_of_prod=bus['year_of_prod'],
                                              velocity=bus['velocity'])
                # print('должен быть добавлен имеющийся Bus')
            except Bus.DoesNotExist:
                current_bus = Bus.objects.create(driver=driver, **bus)
                # print('создан новый Bus')
            driver.bus.add(current_bus.id)
        return driver

    def update(self, instance, validated_data):
        if validated_data.get('bus'):
            bus_data = validated_data.pop('bus')
            instance.bus.through.objects.filter(driver_id=instance.id).delete()
            for bus in bus_data:
                try:
                    current_bus = Bus.objects.get(name=bus['name'],
                                                  bus_model=bus['bus_model'],
                                                  year_of_prod=bus['year_of_prod'],
                                                  velocity=bus['velocity'])
                    # print('должен быть добавлен имеющийся Bus')
                except Bus.DoesNotExist:
                    current_bus = Bus.objects.create(driver=instance, **bus)
                    # print('создан новый Bus')
                instance.bus.add(current_bus.id)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class TravelDriverSerializer(serializers.ModelSerializer):
    bus = BusSerializer(many=True)
    travel_time = serializers.CharField()
    class Meta:
        model = Driver
        fields = ('id', 'name', 'surname', 'date_of_birth', 'bus', 'age', 'travel_time')
        depth = 1

