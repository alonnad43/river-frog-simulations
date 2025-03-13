import pandas as pd

class AlloyDataUnifier:
    """
    Merges alloy data from multiple sources into a single unified dictionary.
    Also identifies missing or invalid data and provides a summary of any issues.
    """

    def __init__(self, text_data, graph_data, config=None):
        """
        Initializes the AlloyDataUnifier with text and graph data dictionaries.

        Parameters:
        - text_data: Dictionary containing text-based alloy data (from OCR).
        - graph_data: Dictionary containing graph-based alloy data.
        - config: Optional configuration dictionary (not required for merging,
                  but available if the unifier needs thresholds, etc. later).
        """
        # Start with a copy of text_data, so we don't mutate the original
        merged_data = text_data.copy()

        # Merge graph_data into merged_data (text_data takes precedence in conflicts)
        for alloy_key, graph_values in graph_data.items():
            if alloy_key in merged_data:
                merged_data[alloy_key].update(graph_values)
            else:
                merged_data[alloy_key] = graph_values

        self.alloy_data = merged_data
        self.config = config
        self.issues = []

    def unify_data(self):
        """
        Converts self.alloy_data into a DataFrame, fills missing data with 'N/A',
        and converts it back to a dictionary. Then checks for missing or invalid data.

        Returns:
        - unified_dict: A dictionary containing the final unified data.
        """
        # Convert dictionary to DataFrame (keys = alloy names, columns = properties)
        df = pd.DataFrame.from_dict(self.alloy_data, orient='index')

        # Fill missing values with 'N/A'
        df.fillna('N/A', inplace=True)

        # Convert back to dictionary
        unified_dict = df.to_dict(orient='index')

        # Check for missing or invalid data
        self._check_for_issues(unified_dict)

        return unified_dict

    def _check_for_issues(self, unified_dict):
        """
        Identifies missing or invalid numeric fields in the unified dictionary
        and populates self.issues with descriptive messages.
        """
        for alloy_name, traits in unified_dict.items():
            missing_traits = []
            invalid_traits = []

            for trait, value in traits.items():
                # If it's 'N/A', record it as missing
                if value == 'N/A':
                    missing_traits.append(trait)
                else:
                    # Try converting to float to see if it's numeric
                    try:
                        float(value)
                    except ValueError:
                        invalid_traits.append(trait)

            if missing_traits:
                self.issues.append(
                    f"Alloy '{alloy_name}' is missing traits: {', '.join(missing_traits)}."
                )
            if invalid_traits:
                self.issues.append(
                    f"Alloy '{alloy_name}' has invalid numeric values for traits: {', '.join(invalid_traits)}."
                )

    def report_issues(self):
        """
        Summarizes any issues found during unification.
        Returns a success message if no issues exist.
        """
        if self.issues:
            return "\n".join(self.issues)
        else:
            return "No issues found. All alloy data is complete and valid."
