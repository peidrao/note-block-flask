from services.hello import HelloWorld


def register_endpoints(app):
    hello = HelloWorld.as_view(name='helloworld')
    app.add_url_rule('/', view_func=hello)


# api.add_resource(HelloWorld, '/')
# api.add_resource(ProfileSignupView, '/signup')
# api.add_resource(ProfileLoginView, '/login')

# api.add_resource(ProfileMeView, '/me')

# api.add_resource(ProfileListView, '/profile')
# api.add_resource(ProfileDetailsView, '/profile/<int:profile_id>')

# api.add_resource(NoteListView, '/notes')
# api.add_resource(ProfileMeNotes, '/me/notes/')
