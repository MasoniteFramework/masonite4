def validate(*rules, redirect=None, back=None):
    def decorator(func, rules=rules):
        def wrapper(*args, **kwargs):
            from wsgi import container

            request = container.make("Request")
            errors = request.validate(*rules)
            if errors:
                if redirect:
                    return request.redirect(redirect).with_errors(errors).with_input()
                if back:
                    return request.back().with_errors(errors).with_input()
                return errors
            else:
                return container.resolve(func)

        return wrapper

    return decorator
