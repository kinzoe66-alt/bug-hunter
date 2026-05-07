class RuntimeMemory:

    def __init__(self):

        self._data = {}

    def set(
        self,
        key: str,
        value
    ):

        self._data[key] = value

        return value

    def get(
        self,
        key: str,
        default=None
    ):

        return self._data.get(
            key,
            default
        )

    def require(
        self,
        key: str
    ):

        if key not in self._data:

            raise KeyError(
                f"Missing runtime memory key: {key}"
            )

        return self._data[key]

    def snapshot(self):

        return dict(self._data)