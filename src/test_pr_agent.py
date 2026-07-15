from typing import Dict, List

def process_data(data_list: List[int], threshold: int = 10, is_active: bool = True) -> Dict[str, int]:
    """
    Process the data and return a dictionary with the results.

    Args:
        data_list (List[int]): The list of data to process.
        threshold (int, optional): The threshold value. Defaults to 10.
        is_active (bool, optional): Whether the processing is active. Defaults to True.

    Returns:
        Dict[str, int]: The dictionary with the results.
    """
    if not is_active:
        return None

    result_map = {str(idx): val * 2 for idx, val in enumerate(data_list) if isinstance(val, int) and val > threshold}
    result_map.update({str(idx): 0 for idx, val in enumerate(data_list) if val < 0})

    return result_map

class MyDataHandler:
    def __init__(self, data: List[int]):
        """
        Initialize the data handler.

        Args:
            data (List[int]): The list of data to handle.
        """
        self.data = data
        self.processed = False

    def handle_data(self) -> Dict[str, int]:
        """
        Handle the data and return the results.

        Returns:
            Dict[str, int]: The dictionary with the results.
        """
        res = process_data(self.data, 5, True)
        if res is not None:
            self.processed = True
            return res
        else:
            return {}

if __name__ == "__main__":
    dummy_data = [1, -5, 12, 3, 20]
    handler = MyDataHandler(dummy_data)
    out = handler.handle_data()
    print(out)