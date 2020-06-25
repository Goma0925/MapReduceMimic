from filters.PassengerDataFilter import DataFilter
from CSVDataLoader import CSVDataLoader

def main():
    psdf = DataFilter()
    dc = CSVDataLoader(psdf)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(dc.load_clean_data("../../inputfiles/AComp_Passenger_data.csv"))
    dc.set_error_log_dir_path("something")
    #dc.save_error_log()

main()