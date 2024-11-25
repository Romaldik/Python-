from ..DataBase.db_utils import dbUtils as db

class Sponsor:
    def __init__(self, name):
        self.name = name

    def create_sponsor(self):
        db.add_data('sponsor', (self.name))

    @staticmethod
    def delete_sponsor(name):
        id = db.get_data('id', 'sponsor', name, 'name')
        db.delete_data('sponsor', id)

    def list_of_sponsors():
        return db.show_table('sponsor')