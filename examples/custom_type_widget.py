from niceforms import factory, UIComponent

print(factory._widgets)

class MyNewWidget(UIComponent):
    def render(self) -> None:
        pass

factory.insert_new_widget(field_type=int, widget_type=MyNewWidget)

print(factory._widgets)