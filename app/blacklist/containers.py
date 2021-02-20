from dependency_injector import containers, providers
from dependency_injector.ext import aiohttp as ext_aiohttp

from app.blacklist.controllers import ban_driver

class BlackListPackageContainer(containers.DeclarativeContainer):
    application_utils = providers.DependenciesContainer()

    mappers = providers.DependenciesContainer()

    # services

    ban_driver = ext_aiohttp.View(
        ban_driver,
        blacklist_mapper=mappers.blacklist_mapper,
        validator=application_utils.validator
    )