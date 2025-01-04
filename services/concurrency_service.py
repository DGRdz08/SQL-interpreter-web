import portalocker

class ConcurrencyService:
    @staticmethod
    def lock_csv(path_to_csv):
        return portalocker.Lock(path_to_csv, mode='r+') 
