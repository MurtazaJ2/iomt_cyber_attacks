import math
from typing import Optional, List

SAMPLE_DATA = [2, 4, 9, 16, 25]

class DataProcessorDummy:
    """A dummy data processor class."""
    
    def __init__(self, data_list: List[int]):
        """
        Initialize the data processor with a list of data.
        
        Args:
        data_list (List[int]): A list of numbers.
        """
        self.data = data_list

    def compute_metrics(self) -> Optional[List[dict]]:
        """
        Compute metrics for the data.
        
        Returns:
        Optional[List[dict]]: A list of dictionaries containing the metrics, or None if the input list is empty.
        """
        if not self.data:
            return None
        
        results = []
        for idx, item in enumerate(self.data):
            if item % 2 == 0:
                val = math.pow(item, 2)
                results.append({'index': idx, 'squared': val})
            else:
                val = math.sqrt(item)
                results.append({'index': idx, 'sqrt': val})
        
        return results

def execute_dummy_logic() -> None:
    """
    Execute the dummy logic.
    
    This function does not return any value, it only prints the results of the computation.
    """
    processor = DataProcessorDummy(SAMPLE_DATA)
    out = processor.compute_metrics()
    if out is not None:
        for item in out:
            print(item)
    else:
        print("No data to process")

if __name__ == "__main__":
    execute_dummy_logic()