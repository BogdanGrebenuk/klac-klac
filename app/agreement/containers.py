from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.agreement.controllers import create_agreement, get_agreements, select_agreement, get_current_agreement
from app.agreement.services import AgreementCreator
from app.agreement.transformers import AgreementTransformer


class AgreementPackageContainer(containers.DeclarativeContainer):
    application_utils = providers.DependenciesContainer()

    mappers = providers.DependenciesContainer()

    # services

    agreement_transformer = providers.Singleton(
        AgreementTransformer,
        user_mapper=mappers.user_mapper
    )

    agreement_creator = providers.Singleton(
        AgreementCreator,
    )

    # controllers

    create_agreement = ext_aiohttp.View(
        create_agreement,
        agreement_creator=agreement_creator,
        driver_mapper=mappers.driver_mapper,
        agreement_mapper=mappers.agreement_mapper,
        order_mapper=mappers.order_mapper,
        agreement_transformer=agreement_transformer
    )

    get_agreements = ext_aiohttp.View(
        get_agreements,
        passenger_mapper=mappers.passenger_mapper,
        agreement_mapper=mappers.agreement_mapper,
        agreement_transformer=agreement_transformer,
        order_mapper=mappers.order_mapper
    )

    select_agreement = ext_aiohttp.View(
        select_agreement,
        passenger_mapper=mappers.passenger_mapper,
        agreement_mapper=mappers.agreement_mapper,
        order_mapper=mappers.order_mapper,
        agreement_transformer=agreement_transformer
    )

    get_current_agreement = ext_aiohttp.View(
        get_current_agreement,
        driver_mapper=mappers.driver_mapper,
        agreement_mapper=mappers.agreement_mapper,
        order_mapper=mappers.order_mapper,
    )