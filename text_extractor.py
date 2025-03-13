"""
TextExtractor Module

Description:
Extracts textual data from DjVu files and images using OCR.
Processes technical documents to extract alloy properties such as yield strength,
tensile strength, and heat treatment details. The extracted data is stored in a
structured format for further analysis.
"""

""" write for each function what it does and what it returns """
import os
import logging
import re
import pytesseract
from PIL import Image
import cv2
import numpy as np
import json

# Configure logging
logging.basicConfig(level=logging.INFO)


# In text_extractor.py


class TextExtractor:
    """
    Automates the process of extracting text and specific alloy properties from
    DjVu files or images using OCR.
    """

    def __init__(self, input_files, config):
        """
        Initializes the TextExtractor with input files and configuration settings.

        Parameters:
        - input_files: List of file paths to process.
        - config: Dictionary containing configuration settings (paths, properties, regex patterns).
        """
        self.input_files = input_files
        self.config = config
        self.valid_files = []

        # Validate Input Files
        for file_path in self.input_files:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.valid_files.append(file_path)
            else:
                logging.warning(f"File not found or inaccessible: {file_path}")

        if not self.valid_files:
            logging.error("No valid input files found.")
            raise RuntimeError("No valid input files found.")

        # Instead of checking for keys that don't exist in the YAML, extract from available sections:
        # Use the text output path from the 'paths' section as the output directory.
        self.output_dir = self.config.get("paths", {}).get("text_output_from_text_reader", "output")

        # Use mechanical properties from 'properties_to_search_for'
        self.properties_to_extract = self.config.get("properties_to_search_for", {}).get(
            "mechanical_properties_to_search_for", {})

        # Use alloy patterns directly from the YAML
        self.alloy_patterns = self.config.get("alloy_patterns", [])

        # Check that we have at least one property extraction pattern and alloy patterns
        if not self.properties_to_extract or not self.alloy_patterns:
            logging.error("Critical configuration settings are missing: properties or alloy patterns.")
            raise RuntimeError("Critical configuration settings are missing.")

        os.makedirs(self.output_dir, exist_ok=True)

        # Define supported image extensions
        self.image_extensions = ['.jpg', '.jpeg', '.png', '.tif', '.tiff']

        # Internal Data Structures
        self.extracted_texts = {}  # {file_name: text}
        self.alloy_data = {}       # {alloy_name: {property: value}}

    @staticmethod
    def preprocess_image(image_path):
        """
        Applies advanced image preprocessing to enhance OCR accuracy.

        Parameters:
        - image_path: Path to the image.

        Returns:
        - Preprocessed image (numpy array) or None if processing fails.
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                logging.warning(f"Unable to read image: {image_path}")
                return None
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            kernel = np.ones((3, 3), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            return opening
        except Exception as e:
            logging.error(f"Error during image preprocessing: {e}")
            return None


    @staticmethod
    def extract_text(image):
        """
        Performs OCR on the preprocessed image to extract text.

        Parameters:
        - image: Preprocessed image (numpy array).

        Returns:
        - Extracted text (string) or empty string if extraction fails.
        """
        try:
            pil_image = Image.fromarray(image)
            extracted_text = pytesseract.image_to_string(pil_image)
            if not extracted_text.strip():
                logging.warning("No text extracted from the image.")
            return extracted_text
        except Exception as e:
            logging.error(f"Error during text extraction: {e}")
            return ""

    def identify_alloys(self, text):
        """
        Identifies alloy names in the text using regex patterns.

        Parameters:
        - text: Extracted text.

        Returns:
        - List of identified alloy names.
        """
        try:
            alloys = []
            for pattern in self.alloy_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                alloys.extend(matches)
            if not alloys:
                logging.warning("No alloys identified in the text.")
            else:
                logging.info(f"Identified Alloys: {alloys}")
            return alloys
        except Exception as e:
            logging.error(f"Error identifying alloys: {e}")
            return []


    def extract_properties(self, text):
        """
        Extracts key mechanical properties and heat treatment info from the text.

        Parameters:
        - text: Extracted text.

        Returns:
        - Dictionary of extracted properties.
        """
        try:
            properties = {}
            for prop_name, patterns in self.properties_to_extract.items():
                for pattern in patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        value = match.group(1)
                        properties[prop_name] = value
                        logging.info(f"Extracted {prop_name}: {value}")
                        break
                else:
                    logging.warning(f"Property '{prop_name}' not found.")
                    properties[prop_name] = None
            return properties
        except Exception as e:
            logging.error(f"Error during property extraction: {e}")
            return {}


    def save_data(self):
        """
        Saves the extracted texts and structured alloy data to files.
        """
        try:
            texts_dir = os.path.join(self.output_dir, 'texts')
            os.makedirs(texts_dir, exist_ok=True)
            for file_name, text in self.extracted_texts.items():
                base_name = os.path.splitext(os.path.basename(file_name))[0]
                text_file_path = os.path.join(texts_dir, f"{base_name}.txt")
                with open(text_file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
            data_file_path = os.path.join(self.output_dir, 'alloy_data.json')
            with open(data_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.alloy_data, f, indent=4)
            logging.info(f"Data saved successfully in {self.output_dir}")
        except Exception as e:
            logging.error(f"Error during data saving: {e}")


    def process_files(self):
        """
        Processes each valid file through preprocessing, OCR, alloy identification,
        and property extraction.

        Returns:
        - The unified alloy data.
        """
        for file in self.valid_files:
            logging.info(f"Processing file: {file}")
            ext = os.path.splitext(file)[1].lower()
            if ext == '.djvu':
                images = self.convert_djvu_to_images(file)
                if not images:
                    continue
            elif ext in self.image_extensions:
                images = [file]
            else:
                logging.warning(f"Unsupported file type: {file}")
                continue

            for image in images:
                preprocessed = self.preprocess_image(image)
                if preprocessed is None:
                    continue
                text = self.extract_text(preprocessed)
                if not text:
                    continue
                self.extracted_texts[image] = text
                alloys = self.identify_alloys(text)
                for alloy in alloys:
                    properties = self.extract_properties(text)
                    if alloy not in self.alloy_data:
                        self.alloy_data[alloy] = properties
                    else:
                        self.alloy_data[alloy].update(properties)
        self.save_data()
        return self.alloy_data

    def convert_djvu_to_images(self, djvu_file):
        """
        Converts a DjVu file to a list of image file paths using djvu.decode.

        Parameters:
        - djvu_file: File path of the DjVu document.

        Returns:
        - List of image file paths.
        """
        try:
            import djvu.decode
        except ImportError:
            logging.error("The 'djvu.decode' module is not installed. Please install it to process DjVu files.")
            return []

        try:
            # פותחים את קובץ ה־DjVu עם הספרייה
            doc = djvu.decode.open(djvu_file)
            logging.info(f"Opened DjVu file using djvu.decode: {djvu_file}")

            images = []
            for page_index, page in enumerate(doc.pages):
                # ננסה לייצר תמונת PIL מכל עמוד
                # page.render() מחזיר אובייקט RenderedPage, שממנו אפשר להפיק תמונת PIL
                rendered = page.render()
                pil_image = rendered.get_pilimage()

                image_path = os.path.join(
                    self.output_dir,
                    f"{os.path.splitext(os.path.basename(djvu_file))[0]}_page{page_index + 1}.png"
                )

                pil_image.save(image_path, format="PNG")
                images.append(image_path)

            logging.info(f"Converted {djvu_file} to {len(images)} image(s) using djvu.decode.")
            return images

        except Exception:
            logging.exception("Error converting DjVu to images with djvu.decode:")
            return []


