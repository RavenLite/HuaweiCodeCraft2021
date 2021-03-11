
# TrainingData Class, structures each training data
class TrainingData(object):

    def __init__(self, server_type_num, server_type_list, vm_type_num, vm_type_list, day_num, daily_queue_list):
        # number
        self.server_type_num = server_type_num
        # list of tuple
        self.server_type_list = server_type_list
        # number
        self.vm_type_num = vm_type_num
        # list of tuple
        self.vm_type_list = vm_type_list
        # number
        self.day_num = day_num
        # list of DailyQueue
        self.daily_queue_list = daily_queue_list


class DailyQueue(object):

    def __init__(self, queue_length, queue_info):
        # number
        self.queue_length = queue_length
        # list of tuple
        self.queue_info = queue_info


def read_file():
    f = open('../../training_data/training-1.txt')


def get_training_data():
    training_data = TrainingData()
    return training_data
