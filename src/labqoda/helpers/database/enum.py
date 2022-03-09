class EnumDatabaseMixin:
    @classmethod
    def get_database_max_length(cls):
        return max(len(i.value) for i in cls)

    @classmethod
    def get_database_choices(cls):
        return [(i.value, i.value) for i in cls]
