import pandas as pd
import logging

class DataValidator:
    """
    Validates text, graph, and unified data for consistency, then optionally
    exports the unified dictionary to a CSV file.
    """

    def __init__(self, text_data=None, graph_data=None, unified_data=None, config=None):
        """
        Initializes the DataValidator with text, graph, and unified data dictionaries.
        :param text_data: Dictionary containing text-based alloy data (OCR results).
        :param graph_data: Dictionary containing graph-based alloy data.
        :param unified_data: Dictionary containing merged text+graph data (from AlloyDataUnifier).
        :param config: Optional configuration settings (e.g., thresholds or file paths).
        """
        self.text_data = text_data if text_data else {}
        self.graph_data = graph_data if graph_data else {}
        self.unified_data = unified_data if unified_data else {}
        self.config = config if config else {}
        logging.basicConfig(level=logging.INFO)

    def validate_data(self):
        """
        Ensures the text_data, graph_data, and unified_data are not empty.
        Raises ValueError if any required dictionary is empty.
        """
        # If your workflow requires all three to be non-empty, enforce that here:
        if not self.text_data:
            raise ValueError("Text data dictionary is empty. Cannot validate.")
        if not self.graph_data:
            raise ValueError("Graph data dictionary is empty. Cannot validate.")
        if not self.unified_data:
            raise ValueError("Unified data dictionary is empty. Cannot validate.")

        logging.info("DataValidator: All data dictionaries are non-empty. Validation passed.")

    def format_and_align_data(self):
        """
        (Optional) Demonstrates how you might align text_data and graph_data if needed:
          - Eliminates duplicates
          - If there's a conflict, prioritize text data
        Then updates self.unified_data accordingly.
        Modify or remove if your unifier already handles these tasks.
        """
        # Example approach:
        for alloy_name in self.text_data:
            text_info = self.text_data[alloy_name]
            graph_info = self.graph_data.get(alloy_name, {})

            cleaned_data = {}

            # Merge text_info, overriding conflicts with text_data
            for trait, text_val in text_info.items():
                graph_val = graph_info.get(trait)
                if graph_val is not None:
                    if text_val != graph_val:
                        logging.warning(
                            f"Conflict in alloy '{alloy_name}' for trait '{trait}'. "
                            f"Text data = {text_val}, Graph data = {graph_val}. "
                            "Prioritizing text data."
                        )
                    cleaned_data[trait] = text_val
                else:
                    cleaned_data[trait] = text_val

            # Add any graph traits not in text
            for trait, g_val in graph_info.items():
                if trait not in cleaned_data:
                    cleaned_data[trait] = g_val

            # Update unified_data with the merged result
            self.unified_data[alloy_name] = cleaned_data

        logging.info("Data alignment between text_data and graph_data complete.")

    def export_data_to_csv(self, output_path):
        """
        Exports the unified data dictionary to a CSV file.
        - Missing data is marked as 'missing data'.
        - The first column is 'Alloy Name' (dictionary key).
        :param output_path: File path where CSV will be saved.
        :return: The path of the exported CSV file.
        """
        if not self.unified_data:
            raise ValueError("Unified data dictionary is empty. Nothing to export.")

        # Convert the unified_data dictionary to a DataFrame
        df = pd.DataFrame.from_dict(self.unified_data, orient='index')

        # Fill missing data
        df.fillna('missing data', inplace=True)

        # Save to CSV
        df.to_csv(output_path, index_label='Alloy Name')
        logging.info(f"Data exported to CSV at: {output_path}")
        return output_path


# Example usage (test/demo)
if __name__ == "__main__":
    # Suppose we have these sample dictionaries:
    sample_text_data = {
        "SS.1": {"density": "7.9", "strength": "250"},
        "CA.1": {"density": "8.2", "strength": "N/A"},
    }
    sample_graph_data = {
        "SS.1": {"strength": "260"},  # conflict with text
        "CA.1": {"strength": "300"},
        "WA.1": {"strength": "320"},
    }
    sample_unified_data = {
        "SS.1": {"density": "7.9", "strength": "250"},
        "CA.1": {"density": "8.2", "strength": "N/A"},
        "WA.1": {"density": "invalid_data", "strength": "320"},
    }

    validator = DataValidator(
        text_data=sample_text_data,
        graph_data=sample_graph_data,
        unified_data=sample_unified_data
    )

    # 1) Validate dictionaries aren't empty
    try:
        validator.validate_data()
    except ValueError as e:
        print(e)

    # 2) (Optional) Align text & graph data, updating unified_data
    validator.format_and_align_data()

    # 3) Export final unified_data to CSV
    validator.export_data_to_csv("example_output.csv")