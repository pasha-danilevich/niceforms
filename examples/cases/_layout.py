from functools import wraps
from typing import Optional

from nicegui import ui


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


class TheCard(ui.card):
    def __init__(self, clickable: bool = False, max_width: bool = True, p: int = 2):
        super().__init__()
        self.classes(f'shadow-lg rounded-2xl border-0 bg-white p-{p}')
        if clickable:
            self.classes('hover:shadow-xl transition-shadow cursor-pointer')
        if max_width:
            self.classes('max-w-md')


class TheNavigation:
    def __init__(
        self,
        view_arrow_back: bool = True,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        self.view_arrow_back = view_arrow_back
        self.title = title
        self.description = description

    def render(self) -> None:
        with ui.column().classes('w-full h-full gap-4'):
            # Контейнер для заголовка и описания
            with ui.column().classes(
                'w-full gap-4 md:flex md:flex-row md:items-start md:items-stretch'
            ):
                if self.view_arrow_back:
                    with TheCard(max_width=False, clickable=True).classes(
                        'md:w-auto md:flex-shrink-0 w-full justify-center px-4'
                    ).on('click', handler=ui.navigate.back):
                        ui.icon('arrow_back', size='lg').classes('text-2xl')

                if self.title:
                    if self.description:
                        style = 'md:w-auto md:flex-shrink-0 w-full justify-center'
                    else:
                        style = 'w-full justify-center'

                    with TheCard(max_width=False).classes(style):
                        with ui.row().classes('items-center gap-3 p-3'):
                            ui.label(self.title).classes(
                                'text-lg font-bold text-gray-800 dark:text-white'
                            )

                # Описание категории (занимает оставшееся пространство на десктопе)
                if self.description:
                    with TheCard(max_width=False).classes('md:flex-1 w-full'):
                        with ui.column().classes('w-full gap-2 p-3'):
                            ui.label(self.description).classes(
                                'text-sm text-gray-600 dark:text-gray-400'
                                ' text-justify p-1'
                            )
