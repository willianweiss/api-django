from rest_framework import serializers


class CustomChoicesField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super(CustomChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[int(obj) - 1]

    def to_internal_value(self, data):
        for _choices in self._choices:
            if bool(data in _choices):
                return _choices[0]

        return data
