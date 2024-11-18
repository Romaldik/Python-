from ..DataBase.db_utils import dbUtils as db

class Sponsor:
    def __init__(self, name):
        self.name = name

    def create_sponsor(self):
        data = (self.name, self.duration)
        db.add_data('trainingprogram', data)

    @staticmethod
    def delete_sponsor(name):
        id = db.get_data('id', 'trainingprogram', name)[0]
        db.delete_data('trainingprogram', id)

    def list_of_sponsors():
        return db.show_table('trainingprogram')