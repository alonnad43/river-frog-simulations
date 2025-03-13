import pandas as pd


class MaterialSelector:
    """
    Ranks and selects materials based on specified criteria and weights.
    Each material is represented as a row in a pandas DataFrame.
    """

    def __init__(self, materials_df):
        """
        Initializes the MaterialSelector with a pandas DataFrame of material properties.

        :param materials_df: A DataFrame containing columns like 'Material', 'Strength', 'Cost', etc.
                             Example structure:
                                 Material  Buoyancy  Strength  Cost  CorrosionResistance ...
                                 Material_A     100       300   100                    8
                                 Material_B     120       500   200                    7
                                 ...
        """
        self.materials_df = materials_df.copy()  # Keep an internal copy to avoid modifying the original

    def rank_materials(self, application, weights):
        """
        Ranks the materials based on the provided weights for the specified application.

        :param application: A string representing the application context (e.g., 'Pontoons', 'Frame').
                            (Not strictly required for the calculation, but may be useful for logging.)
        :param weights: A dictionary mapping property -> weight (float).
                        Example: {'Buoyancy': 0.4, 'Strength': 0.3, 'Cost': -0.2, 'Corrosion Resistance': 0.2}
                        Positive weight means "higher is better", negative weight means "lower is better".
        :return: A DataFrame of materials ranked by 'Weighted Score' (descending).
        """
        # Create a copy so we don't overwrite self.materials_df
        ranked_df = self.materials_df.copy()

        # Initialize the Weighted Score column
        ranked_df['Weighted Score'] = 0.0

        # Calculate weighted scores
        for criterion, weight in weights.items():
            if criterion in ranked_df.columns:
                # Fill missing values with 0 or a default if needed
                ranked_df[criterion] = pd.to_numeric(ranked_df[criterion], errors='coerce').fillna(0)
                ranked_df['Weighted Score'] += ranked_df[criterion] * weight
            else:
                print(f"Warning: Criterion '{criterion}' is missing from the DataFrame. Skipping...")

        # Sort by Weighted Score (descending)
        ranked_df.sort_values(by='Weighted Score', ascending=False, inplace=True)

        return ranked_df

    def select_material(self, application, weights):
        """
        Selects the best material (highest Weighted Score) for the given application.

        :param application: String representing the application (e.g., 'Pontoons').
        :param weights: Dictionary mapping property -> weight.
        :return: The name (string) of the top-ranked material.
        """
        ranked_materials = self.rank_materials(application, weights)
        # Return the 'Material' value of the first row
        return ranked_materials.iloc[0]['Material']


# Example usage (test/demo)
if __name__ == "__main__":
    # Sample data
    data = {
        'Material': ['Material_A', 'Material_B', 'Material_C'],
        'Buoyancy': [100, 120, 80],
        'Strength': [300, 500, 400],
        'Cost': [100, 200, 150],
        'Corrosion Resistance': [8, 7, 9],
        'Impact Resistance': [9, 8, 8]
    }

    # Convert to DataFrame
    materials_df = pd.DataFrame(data)

    # Initialize the selector
    selector = MaterialSelector(materials_df)

    # Example weights (positive means "higher is better", negative means "lower is better" for cost)
    weights = {
        'Buoyancy': 0.4,
        'Strength': 0.3,
        'Cost': -0.2,
        'Corrosion Resistance': 0.2,
        'Impact Resistance': 0.1
    }

    # Rank the materials
    ranked = selector.rank_materials("Pontoons", weights)
    print("Ranked Materials:")
    print(ranked)

    # Select the best material
    best_material = selector.select_material("Pontoons", weights)
    print(f"\nBest Material for Pontoons: {best_material}")
