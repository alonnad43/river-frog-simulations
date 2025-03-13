import pandas as pd


class SecondaryChecker:
    """
    Performs secondary validation checks on a DataFrame of alloys based on
    component-specific thresholds defined in the configuration.
    """

    def __init__(self, alloy_df, config):
        """
        :param alloy_df: A pandas DataFrame containing columns like 'Material', 'Buoyancy', 'Strength', 'Cost', etc.
        :param config: A dictionary with thresholds, typically config["default_thresholds"][component]
                       Example:
                       config["default_thresholds"] = {
                           "pontoons": {
                               "buoyancy_min": 100,
                               "strength_min": 200,
                               "cost_max": 150
                           },
                           "frame": {
                               "strength_min": 300,
                               "cost_max": 200
                           },
                           ...
                       }
        """
        self.alloy_df = alloy_df.copy()  # Keep a copy of the DataFrame
        self.config = config  # Configuration with thresholds, etc.

    def check_materials(self, component):
        """
        Validates each alloy in self.alloy_df against thresholds for the specified component.

        :param component: A string (e.g., "pontoons", "frame", "anchors").
        :return: A list of dictionaries, each containing:
                 {
                   'Material': <str>,
                   'Status': 'Pass' or 'Fail',
                   'Reason': <str if Fail, else None>
                 }
        """
        # Retrieve thresholds for this component from the config
        # If not found, fallback to an empty dict
        component_thresholds = self.config.get("default_thresholds", {}).get(component, {})

        validation_report = []

        for _, row in self.alloy_df.iterrows():
            material_name = row.get("Material", "Unknown")
            entry = {"Material": material_name, "Status": "Pass"}

            # Example property checks:
            # Buoyancy check
            if "buoyancy_min" in component_thresholds and "Buoyancy" in row:
                try:
                    if float(row["Buoyancy"]) < component_thresholds["buoyancy_min"]:
                        entry["Status"] = "Fail"
                        entry["Reason"] = f"Buoyancy below {component_thresholds['buoyancy_min']}"
                except ValueError:
                    entry["Status"] = "Fail"
                    entry["Reason"] = "Buoyancy not numeric"

            # Strength check
            if entry["Status"] == "Pass" and "strength_min" in component_thresholds and "Strength" in row:
                try:
                    if float(row["Strength"]) < component_thresholds["strength_min"]:
                        entry["Status"] = "Fail"
                        entry["Reason"] = f"Strength below {component_thresholds['strength_min']}"
                except ValueError:
                    entry["Status"] = "Fail"
                    entry["Reason"] = "Strength not numeric"

            # Cost check
            if entry["Status"] == "Pass" and "cost_max" in component_thresholds and "Cost" in row:
                try:
                    if float(row["Cost"]) > component_thresholds["cost_max"]:
                        entry["Status"] = "Fail"
                        entry["Reason"] = f"Cost above {component_thresholds['cost_max']}"
                except ValueError:
                    entry["Status"] = "Fail"
                    entry["Reason"] = "Cost not numeric"

            # Add more checks if needed (e.g., corrosion_resistance_min, etc.)

            validation_report.append(entry)

        return validation_report

    def visualize_validation_report(self, report):
        """
        Prints each material's validation status and reason (if any).
        :param report: A list of dictionaries from check_materials().
        """
        for item in report:
            material = item["Material"]
            status = item["Status"]
            reason = item.get("Reason")
            if reason:
                print(f"{material}: {status} (Reason: {reason})")
            else:
                print(f"{material}: {status}")


# Example usage (test/demo)
if __name__ == "__main__":
    # Sample data
    data = {
        "Material": ["AlloyA", "AlloyB", "AlloyC"],
        "Buoyancy": [90, 120, 130],
        "Strength": [180, 350, 400],
        "Cost": [140, 160, 100]
    }
    df = pd.DataFrame(data)

    # Sample config
    sample_config = {
        "default_thresholds": {
            "pontoons": {
                "buoyancy_min": 100,
                "strength_min": 200,
                "cost_max": 150
            },
            "frame": {
                "strength_min": 300,
                "cost_max": 200
            }
        }
    }

    checker = SecondaryChecker(df, sample_config)
    report = checker.check_materials("pontoons")

    print("Validation Report for 'pontoons':")
    checker.visualize_validation_report(report)
