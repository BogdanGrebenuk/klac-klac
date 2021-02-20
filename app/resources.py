def setup_routes(app):
    container = app.container

    app.router.add_route(
        'POST', '/register', container.user.register_user.as_view()
    )
    app.router.add_route(
        'POST', '/login', container.user.authenticate_user.as_view()
    )
    app.router.add_route(
        'POST', '/logout', container.user.logout_user.as_view()
    )
    app.router.add_route(
        'GET', '/api/users', container.user.get_users.as_view()
    )
    app.router.add_route(
        'GET',  '/api/users/{user_id}', container.user.get_user.as_view()
    )
    app.router.add_route(
        'POST', '/api/orders', container.order.create_order.as_view()
    )
    app.router.add_route(
        'GET', '/api/orders', container.order.get_orders.as_view()
    )
    app.router.add_route(
        'GET', '/api/orders/{order_id}', container.order.get_order_status.as_view()
    )
    app.router.add_route(
        'POST', '/api/agreements', container.agreement.create_agreement.as_view()
    )
    app.router.add_route(
        'GET', '/api/orders/{order_id}/agreements', container.agreement.get_agreements.as_view()
    )
    app.router.add_route(
        'POST', '/api/agreements/{agreement_id}/select', container.agreement.select_agreement.as_view()
    )
    app.router.add_route(
            'POST', '/api/blacklist', container.blacklist.ban_driver.as_view()
        )