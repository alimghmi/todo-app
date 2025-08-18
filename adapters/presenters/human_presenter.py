from usecases.ports import Presenter


class HumanPresenter(Presenter):

    def success(self, data):
        msg = ""
        if isinstance(data, list):
            for item in data:
                for k, v in item.items():
                    msg += f"\t{k}= {v}\n"
                msg += "\n"
        elif isinstance(data, dict):
            for k, v in data.items():
                msg += f"\t{k}= {v}\n"

        return msg

    def fail(self, message, *, status=400):
        return f"{message} [{status} status code]"
