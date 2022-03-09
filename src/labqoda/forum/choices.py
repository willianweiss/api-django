PENDING = 1
APPROVED = 2
DISAPPROVED = 3

STATUS = (
    (PENDING, "Aguardando Moderação"),
    (APPROVED, "Aprovado"),
    (DISAPPROVED, "Reprovado"),
)


STATUS_BY_SERIALIZER = (
    (PENDING, "PENDING"),
    (APPROVED, "APPROVED"),
    (DISAPPROVED, "DISAPPROVED"),
)
