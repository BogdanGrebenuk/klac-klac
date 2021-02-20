from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.order.controllers import create_order, get_orders
from app.order.services import OrderCreator
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

    # controllers

    create_order = ext_aiohttp.View(
        create_order,
        passenger_mapper=mappers.passenger_mapper,
        order_mapper=mappers.order_mapper,
        order_transformer=order_transformer,
        order_creator=order_creator
    )

    get_orders = ext_aiohttp.View(
        get_orders,
        driver_mapper=mappers.driver_mapper,
        order_mapper=mappers.order_mapper,
        order_transformer=order_transformer,
    )