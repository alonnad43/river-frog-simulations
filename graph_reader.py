"""
GraphReader Module

Description:
Extracts numerical data from graph images (e.g., stress–strain curves) using image processing,
OCR, and DeepGraph analysis. Identifies axis labels, units, and data points,
organizing the extracted information for further integration.
"""

import os
import logging
import cv2
import pandas as pd
import pytesseract

# Removed unused imports: re, numpy, matplotlib.pyplot

# Configure logging
logging.basicConfig(level=logging.INFO)


class GraphReader:
    def __init__(self, config):
        """
        Initializes the GraphReader with configuration settings.

        Parameters:
        - config: Dictionary containing paths and thresholds for graph processing.
        """
        self.config = config
        # Retrieve input and output directories from the 'paths' section of the YAML
        self.input_dir = config.get("paths", {}).get("graph_input_dir", "")
        self.output_dir = config.get("paths", {}).get("graph_output", "")

        # Check if output_dir is provided
        if not self.output_dir:
            raise RuntimeError("Graph output directory is not specified in the configuration.")

        os.makedirs(self.output_dir, exist_ok=True)

        os.makedirs(self.output_dir, exist_ok=True)


    @staticmethod
    def preprocess_image(image_path):
        """
        Preprocesses a graph image to enhance data extraction.

        Parameters:
        - image_path: Path to the graph image.

        Returns:
        - Preprocessed image (numpy array) or None if processing fails.
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                logging.warning(f"Unable to read graph image: {image_path}")
                return None
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.medianBlur(gray, 5)
            thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY, 11, 2)
            return thresh
        except Exception as e:
            logging.error(f"Error in preprocessing graph image: {e}")
            return None


    @staticmethod
    def check_tesseract_installed():
        """
        Checks if Tesseract OCR is installed.
        """
        try:
            pytesseract.get_tesseract_version()
            logging.info("Tesseract OCR is installed.")
        except Exception as e:
            logging.error("Tesseract OCR is not installed or not configured properly.")
            raise RuntimeError("Tesseract OCR is not installed.")


    @staticmethod
    def identify_axis_properties(image):
        """
        Identifies axis labels and scales from a preprocessed graph image.

        Parameters:
        - image: Preprocessed graph image.

        Returns:
        - Dictionary with axis properties.
        """
        # Dummy implementation; replace with actual OCR/regex parsing
        axis_props = {"x_label": "Time", "y_label": "Stress", "x_scale": 1, "y_scale": 1}
        return axis_props


    @staticmethod
    def map_pixels_to_data(pixels, axis_properties):
        """
        Maps pixel coordinates to actual data values based on axis properties.

        Parameters:
        - pixels: List of pixel coordinates.
        - axis_properties: Dictionary with axis scaling information.

        Returns:
        - List of data points.
        """
        # Dummy mapping; replace with actual conversion logic
        data_points = [p * axis_properties.get("x_scale", 1) for p in pixels]
        return data_points


    @staticmethod
    def analyze_data(data):
        """
        Analyzes extracted numerical data.

        Parameters:
        - data: Numerical data (e.g., a pandas DataFrame).

        Returns:
        - Dictionary with analysis results.
        """
        analysis_results = {"mean": data.mean(), "std": data.std()}
        return analysis_results

    def extract_data_points(self, image_path):
        """
        Extracts data points from a graph image.

        Parameters:
        - image_path: File path of the graph image.

        Returns:
        - List of data points or None if extraction fails.
        """
        preprocessed = self.preprocess_image(image_path)
        if preprocessed is None:
            return None

        edges = cv2.Canny(preprocessed, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            logging.warning(f"No contours found in image: {image_path}")
            return None

        largest_contour = max(contours, key=cv2.contourArea)

        # Convert largest_contour to a NumPy array if it is a UMat
        if hasattr(largest_contour, 'get'):
            largest_contour = largest_contour.get()

        pixels = [pt[0][0] for pt in largest_contour]
        axis_props = self.identify_axis_properties(preprocessed)
        data_points = self.map_pixels_to_data(pixels, axis_props)
        return data_points

    def process_files(self):
        """
        Processes all graph images in the input directory.

        Returns:
        - Dictionary of aggregated data from all graph images.
        """
        all_data = {}
        if not os.path.isdir(self.input_dir):
            logging.error("Graph input directory not found.")
            return all_data

        for file in os.listdir(self.input_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff')):
                image_path = os.path.join(self.input_dir, file)
                logging.info(f"Processing graph image: {image_path}")
                data_points = self.extract_data_points(image_path)
                if data_points:
                    all_data[file] = data_points
        return all_data


    def save_data(self, data):
        """
        Saves the extracted graph data to a CSV file.

        Parameters:
        - data: Dictionary of extracted data.
        """
        try:
            output_file = os.path.join(self.output_dir, "graph_data.csv")
            df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data.items()]))
            df.to_csv(output_file, index=False)
            logging.info(f"Graph data saved to {output_file}")
        except Exception as e:
            logging.error(f"Error saving graph data: {e}")
            raise RuntimeError("Failed to save graph data.")


# Example usage:
def run():
    """
    Runs the graph reader process.
    """
    config = {
        "graph_input_dir": "path/to/graph/images",
        "graph_output": "output/graphs"
    }
    reader = GraphReader(config)
    data = reader.process_files()
    reader.save_data(data)


if __name__ == '__main__':
    run()
