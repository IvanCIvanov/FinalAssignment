from . import orders, order_details, users, payments, menu_items, recipes, resources, sandwiches


def load_routes(app):



    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(users.router)
    #app.include_router(payments.router)
    app.include_router(menu_items.router)
    app.include_router(recipes.router)
    app.include_router(resources.router)
    app.include_router(sandwiches.router)
