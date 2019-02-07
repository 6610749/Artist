from app import models , db , app
from flask_admin.contrib.sqla import ModelView 
from flask_admin import  Admin, expose ,form , AdminIndexView  
from flask_admin.menu import MenuLink
from flask import Markup , session , redirect , flash , render_template

# the home page for admin 
class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        if not app.config["ADMIN_VERIFICATION"]:
            return self.render(self._template)
        if "admin" in session : 
            if session["admin"] :
                return self.render(self._template)
        return redirect('/dashboard_login')

class ProtectedView(ModelView):
    def is_accessible(self):
        if app.config["ADMIN_VERIFICATION"]:
            if "admin" in session : 
                if session["admin"] : 
                    return True
            return False
        return True

class ArtistView(ProtectedView):
    column_exclude_list = ['performances','association']
    form_excluded_columns = ['performances','association']

    def _list_thumbnail(view, context, model, name):
        if not model.image :
            return 'No image'

        return Markup(
            """
            <img src="%s" width="100px" height="100px">
            """ % model.image
        )

    column_formatters = {
        'image': _list_thumbnail 
    }

class PerformanceView(ProtectedView):
    #column_searchable_list = ['title','artists']
    column_filters = ['title' , 'artists']
    form_excluded_columns = ['association']
    column_list = ['title','artists','date','omgevinf','description','price','link']


admin = Admin(app=app,index_view=MyHomeView())

admin.add_view(ArtistView(models.Artist, db.session))
admin.add_view(ProtectedView(models.Omgevinf, db.session))
admin.add_view(PerformanceView(models.Performance, db.session))


if app.config["ADMIN_VERIFICATION"]:
    admin.add_link(MenuLink(name='Logout', category='', url='/admin_logout'))
