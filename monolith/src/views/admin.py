from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from src.models import db

class AnalyticsViews(BaseView):
    @expose('/')
    def index(self):
        return self.render("admin/analytics.html")

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

    admin.add_view(AnalyticsViews(name="Analytics", endpoint="analytics"))

