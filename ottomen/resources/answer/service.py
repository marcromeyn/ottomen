from ...core import Service
from .models import Answer, Label


class AnswerService(Service):
    __model__ = Answer


class LabelService(Service):
    __model__ = Label

    def save_or_get_labels(self, output_names):
        if output_names is None or len(output_names) == 0:
            return []
        saved_malwares = self.filter(Label.name.in_(output_names)).all()
        saved_names = [x.name for x in saved_malwares]
        malwares_left = [mw for mw in output_names if mw not in saved_names]
        to_save = []

        for mw_name in malwares_left:
            mw = Label(name=mw_name)
            to_save.append(mw)
            saved_malwares.append(mw)
        self.save(to_save)

        return saved_malwares
