from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.whitelist.controllers import promote_driver

class WhiteListPackageContainer(containers.DeclarativeContainer):
    application_utils = providers.DependenciesContainer()

    mappers = providers.DependenciesContainer()

    # services

    promote_driver = ext_aiohttp.View(
        promote_driver,
        whitelist_mapper=mappers.whitelist_mapper,
        validator=application_utils.validator,
        driver_mapper=mappers.driver_mapper
    )