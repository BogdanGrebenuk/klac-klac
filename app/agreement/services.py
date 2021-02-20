from app.agreement.domain.entity import Agreement


class AgreementCreator:

    async def create_agreement(self, create_agreement_dto):
        agreement = Agreement(
            id=create_agreement_dto.id,
            driver_id=create_agreement_dto.driver_id,
            order_id=create_agreement_dto.order_id
        )

        return agreement
