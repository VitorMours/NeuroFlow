from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from src.models import db


def admin_add_views(admin: Admin, views: list):
    for view in views:
        model_name = view.__name__.lower()
        admin.add_view(
            ModelView(
                view,
                db.session,
                name=view.__name__,  # Nome exibido no admin
                endpoint=f"{model_name}_admin_entity"  # Nome único interno
            )
        )
