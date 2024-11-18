from ..DataBase.db_utils import dbUtils as db

class TrainingProgram:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration  
    
    def create_training_program(self):
        data = (self.name, self.duration)
        db.add_data('trainingprogram', data)

    @staticmethod
    def delete_training_program(name):
        id = db.get_data('id', 'trainingprogram', name)[0]
        db.delete_data('trainingprogram', id)

    def list_of_training_programs():
        return db.show_table('trainingprogram')