from functools import wraps

from nicegui import ui


def base(route_handler):
    @wraps(route_handler)
    async def async_wrapper(*args, **kwargs):
        ui.query('body').style(
            'background: linear-gradient(160deg, #eff6ff 0%, #93aeff 100%);'
            'min-height: 100vh;'
        )
        return await route_handler(*args, **kwargs)

    return async_wrapper
