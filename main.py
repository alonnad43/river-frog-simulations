"""
Main Script for River Frog Project

Description:
Coordinates the entire workflow for data extraction, integration, validation,
and material selection. The user may choose between using a SolidWorks file,
a tailored Python data importer, or basic YAML configuration data.
If any critical error occurs, the program stops execution for debugging.
"""

import os
import logging
import pandas as pd  # for final material selection steps, if needed

from utils import load_config
from structural_components import StructuralComponents
from structural_data_importer import StructuralDataImporter
from text_extractor import TextExtractor
from graph_reader import GraphReader
from alloy_data_unifier import AlloyDataUnifier
from data_validator import DataValidator
from material_selector import MaterialSelector


class Main:
    def __init__(self):
        """
        Loads configuration settings from the YAML file.
        Adjust the path to config.yaml if needed.
        """
        self.config = load_config(r"C:\Users\ramaa\Documents\frog5thriver\config.yaml")
        logging.basicConfig(level=logging.INFO)

    def run(self):
        """
        Main workflow:
          1. Prompt user for structural data source (SolidWorks, Python importer, or config).
          2. Extract text (OCR) from the DjVu path in config (option 3).
          3. Extract graph data (from images).
          4. Unify text + graph data.
          5. Validate data (text, graph, unified).
          6. (Optional) Convert unified data to a DataFrame for material selection.
          7. (Optional) Secondary checks on the selected materials.
        """
        user_input = input("Enter 1 for SolidWorks, 2 for Python data importer, 3 for YAML configuration: ").strip()

        # --------------------------------------------------------------------
        # Step 1: Structural data source
        # --------------------------------------------------------------------
        if user_input == '1':
            # Use StructuralComponents if a SolidWorks file is provided
            solidworks_file = self.config.get("solidworks_file", None)
            if not solidworks_file:
                raise RuntimeError("SolidWorks file not specified in configuration.")
            structural_data = StructuralComponents(solidworks_file, self.config).extract_component_data()

        elif user_input == '2':
            # Use StructuralDataImporter if a tailored Python file is provided
            data_file = self.config.get("data_file", None)
            if not data_file:
                raise RuntimeError("Data file for structural import not specified in configuration.")
            structural_data = StructuralDataImporter(data_file, self.config).import_structural_data()

        else:
            # Otherwise, use basic data from configuration
            structural_data = self.config.get("basic_data", {})

            # ----------------------------------------------------------------
            # Step 2: Text Extraction from DjVu (using djvu_path from config)
            # ----------------------------------------------------------------
            djvu_path = self.config["paths"].get("djvu_path", "")
            if not djvu_path or not os.path.isfile(djvu_path):
                raise RuntimeError(f"No valid DjVu file found at {djvu_path}")

            # Provide the single djvu_path as the input to TextExtractor
            input_files = [djvu_path]
            text_extractor = TextExtractor(input_files, self.config)
            text_data = text_extractor.process_files()

            # ----------------------------------------------------------------
            # Step 3: Graph Extraction
            # (Assumes you have images in config["graph_input_dir"] or similar)
            # ----------------------------------------------------------------
            graph_reader = GraphReader(self.config)
            graph_data = graph_reader.process_files()

            # ----------------------------------------------------------------
            # Step 4: Unify Text + Graph Data
            # ----------------------------------------------------------------
            # The new AlloyDataUnifier might require text_data, graph_data, and config
            # or it might just take text_data, graph_data in the constructor.
            # Adjust as per your updated code signature.
            alloy_data_unifier = AlloyDataUnifier(text_data, graph_data, self.config)
            unified_data = alloy_data_unifier.unify_data()

            # ----------------------------------------------------------------
            # Step 5: Validate Data
            # ----------------------------------------------------------------
            # The new DataValidator might expect text_data, graph_data, unified_data, config
            # or something else, depending on your updated code signature.
            data_validator = DataValidator(
                text_data=text_data,
                graph_data=graph_data,
                unified_data=unified_data,
                config=self.config
            )
            try:
                data_validator.validate_data()
                # data_validator.format_and_align_data()  # optional
                # data_validator.export_data_to_csv("unified_data.csv")  # optional
            except ValueError as e:
                logging.error(f"Validation Error: {e}")
                return  # Stop execution if critical validation fails

            # ----------------------------------------------------------------
            # Step 6 (Optional): Material Selection
            # ----------------------------------------------------------------
            # If your updated MaterialSelector expects a DataFrame of numeric columns:
            # Convert the unified_data (dict) to a DataFrame.
            # Then pass it to MaterialSelector. Adjust column names to match your data.
            if not unified_data:
                logging.warning("No unified data found. Skipping material selection.")
            else:
                # Example: Convert dict -> DataFrame
                materials_df = pd.DataFrame.from_dict(unified_data, orient='index')
                # For ranking, we typically need numeric columns. Convert if needed:
                # e.g., materials_df["strength"] = pd.to_numeric(materials_df["strength"], errors='coerce').fillna(0)

                # The new MaterialSelector might just take materials_df
                # or it might require (materials_df, config, application, weights).
                application = self.config.get("application", "pontoons")
                weights = {
                    "strength": 0.3,
                    "density": -0.2,  # negative if lower density is better
                    # etc.
                }

                selector = MaterialSelector(materials_df)
                ranked_df = selector.rank_materials(application, weights)
                print("Ranked Materials (example):")
                print(ranked_df)

                best_material = selector.select_material(application, weights)
                print(f"Best Material for {application}: {best_material}")

            # ----------------------------------------------------------------
            # Step 7 (Optional): Secondary Checks
            # ----------------------------------------------------------------
            # If your SecondaryChecker wants a DataFrame + config, do:
            # Or if it wants selected_materials, adapt accordingly.
            # e.g.:
            # secondary_checker = SecondaryChecker(ranked_df, self.config)
            # check_report = secondary_checker.check_materials("pontoons")
            # secondary_checker.visualize_validation_report(check_report)


if __name__ == "__main__":
    main = Main()
    main.run()
