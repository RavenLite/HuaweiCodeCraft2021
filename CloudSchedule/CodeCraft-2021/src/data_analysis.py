import read_file
import matplotlib

class training_data_analysis(object):

    def __init__(self):
        training_data = read_file.get_training_data()
        self.server_type_num = training_data.get_server_type_num()
        self.server_type_list = training_data.get_server_type_list()
        self.vm_type_num = training_data.get_vm_type_num()
        self.vm_type_list = training_data.get_vm_type_list()
        self.daily_num = training_data.get_daily_num()
        self.daily_queue_list = training_data.get_daily_queue_list()
        self.analysis()

    def analysis(self):
        pass




def get_analysis():
    tda = training_data_analysis()
    tda.analysis()


if __name__ == "__main__":
    get_analysis()