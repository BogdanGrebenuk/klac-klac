from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.order.controllers import (
    create_order,
    get_orders,
    get_order_status,
    update_order_status
)
from app.order.services import OrderCreator, OrderTimeoutChecker
from app.order.transformers import OrderTransformer


class OrderPackageContainer(containers.DeclarativeContainer):
    application_utils = providers.DependenciesContainer()

    mappers = providers.DependenciesContainer()

    # services

    order_transformer = providers.Singleton(OrderTransformer)

    order_creator = providers.Singleton(
        OrderCreator,
        validator=application_utils.validator
    )

    order_timeout_checker = providers.Singleton(
        OrderTimeoutChecker,
        order_mapper=mappers.order_mapper,
        agreement_mapper=mappers.agreement_mapper,
        logger=application_utils.logger
    )

    # controllers

    create_order = ext_aiohttp.View(
        create_order,
        passenger_mapper=mappers.passenger_mapper,
        order_mapper=mappers.order_mapper,
        order_transformer=order_transformer,
        order_creator=order_creator,
        order_timeout_checker=order_timeout_checker
    )

    get_orders = ext_aiohttp.View(
        get_orders,
        driver_mapper=mappers.driver_mapper,
        passenger_mapper=mappers.passenger_mapper,
        order_mapper=mappers.order_mapper,
        order_transformer=order_transformer,
    )

    get_order_status = ext_aiohttp.View(
        get_order_status,
        driver_mapper=mappers.driver_mapper,
        passenger_mapper=mappers.passenger_mapper,
        order_mapper=mappers.order_mapper,
        agreement_mapper=mappers.agreement_mapper,
    )

    update_order_status = ext_aiohttp.View(
        update_order_status,
        order_mapper=mappers.order_mapper,
        driver_mapper=mappers.driver_mapper,
        order_transformer=order_transformer,
    )