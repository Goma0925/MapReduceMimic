class Context:
    """
    This class is responsible for storing the (key, val_tuple) pairs after mapping, combining, and reducing.
    In each phase and each worker, a different instance of Context will be used.
    """
    def __init__(self):
        self.key_val_pairs = []
        """
        key_val_pair tuple's signature
            key_val_pair = (key, [val,...])
        """

    def write(self, key: str, val: str):
        val_tuple = (val)
        key_val_pair = (key, val_tuple)
        self.key_val_pairs.append(key_val_pair)

    def get_key_val_pairs(self):
        return self.key_val_pairs

    def clear(self):
        self.key_val_pairs.clear()
