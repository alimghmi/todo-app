from usecases.ports import Presenter


class JsonPresenter(Presenter):

    def success(self, data):
        return {"ok": True, "data": data}

    def fail(self, message: str, *, status: int = 400):
        return {"ok": False, "error": {"message": message, "status": status}}
