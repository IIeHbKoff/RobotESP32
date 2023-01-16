def skill_wrapper(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self._telemetry.errors = f"{self.class_name}: {e}"
    return wrapper
