from flask import Flask
from flask_graphql import GraphQLView
from database import db_session
from schema import schema

# 1. Initialize our Flask Application
app = Flask(__name__)

# 2. Add /graphql Rule
# This lets the flask application route to the GraphQL API.
# It automatically provides a GraphiQL test interface in the browser if `graphiql=True`.
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enabled for easy testing
    )
)

# 3. Request Teardown
# It is important to clean up sessions after requests so that connections are freed up.
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    print("====================================")
    print("Starting Study Room Booking API...")
    print("1. Visit http://127.0.0.1:5000/graphql for testing.")
    print("2. Ensure you have run 'python seed_data.py' beforehand to create DB tables.")
    print("====================================")
    app.run(debug=True, port=5000)
