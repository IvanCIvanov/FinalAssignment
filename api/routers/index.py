from . import orders, order_details, users, payments


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(users.router)
    app.include_router(payments.router)