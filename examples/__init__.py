"""Примеры использования."""
from pprint import pprint

from pydantic import BaseModel


# def render(self) -> None:
#     """Render the form UI."""
#     schema = self.model.model_json_schema()
#     properties = schema.get("properties", {})
#
#     with ui.card().classes(
#             f"w-full {DEFAULT_FORM_WIDTH} mx-auto shadow-lg rounded-xl overflow-hidden"
#     ):
#         Header(title=self.title, description=schema.get('description')).render()
#         widgets = [p for p in properties]
#         Body(widgets=widgets).render()
#         self._render_body(properties)
#         self._render_footer_buttons()

class User(BaseModel):
    """Some description"""
    name: str
    age: int
    email: str
    arr: list[str]

#
# {'description': 'Some description',
#  'properties': {'age': {'title': 'Age', 'type': 'integer'},
#                 'email': {'title': 'Email', 'type': 'string'},
#                 'name': {'title': 'Name', 'type': 'string'}},
#  'required': ['name', 'age', 'email'],
#  'title': 'User',
#  'type': 'object'}

pprint(User.model_fields)
