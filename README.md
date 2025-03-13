Below is a **revised README.md** that updates your existing one with a more comprehensive overview of all files. It emphasizes how each module fits into the larger **River Frog Simulations** workflow and includes suggestions for usage and structure.

---

# **River Frog Simulations**

## **Overview**
The **River Frog Simulations** repository is part of a larger initiative (the **River Frog Project**) to develop a **flood-resistant debris interception system** for **Nahal Be’er Sheva**. It leverages Python-based automation for **material selection**, **structural data processing**, and **validation** to ensure the interceptor is robust, cost-effective, and adaptable to real-world flood conditions.

---

## **Project Objectives**
1. **Automate Material Selection**: Evaluate mechanical properties from **DjVu/PDF** documents and **graphical data**.
2. **Structural Analysis**: Run **stress-strain** and **flood-resilience** simulations on potential materials.
3. **Unified Data Management**: Merge text, graph, and user-provided data into a single, **validated** dataset.
4. **Prototype Testing**: Provide insights for physical prototypes and further research in the field.

---

## **Core Components & Key Scripts**
Below is an overview of each module, what it does, and how it contributes to the project.

### 1. **Main Execution**
- **`main.py`**  
  *Orchestrates the entire workflow.*  
  1. Imports structural data (via **SolidWorks**, Python importer, or direct config).  
  2. Extracts text from **DjVu** or **PDF** (`text_extractor.py`).  
  3. Processes **graph images** (`graph_reader.py`).  
  4. Merges text + graph data (`alloy_data_unifier.py`).  
  5. Validates everything (`data_validator.py`).  
  6. Optionally **ranks materials** and runs **secondary checks** (`material_selector.py`, `secondary_checker.py`).

### 2. **Data Extraction & Processing**
- **`text_extractor.py`**  
  *Extracts textual data from DjVu/PDF docs using OCR.*  
  - Identifies **alloy patterns** (e.g., SS.123) and extracts **mechanical properties**.  
  - Saves results in a structured JSON or text files.

- **`graph_reader.py`**  
  *Digitizes stress-strain or other engineering graphs.*  
  - Uses image processing (OpenCV) + OCR to parse **axis labels**, **data points**, and **scales**.  
  - Outputs CSV or dict-based data for integration.

- **`alloy_data_unifier.py`**  
  *Combines extracted text data with graph data.*  
  - Consolidates overlapping records into a single dataset.  
  - Provides a final dictionary or DataFrame for subsequent validation.

- **`data_validator.py`**  
  *Checks extracted data for consistency & completeness.*  
  - Ensures each alloy has all required properties.  
  - Reports missing or invalid values.

### 3. **Material Selection & Validation**
- **`material_selector.py`**  
  *Ranks materials based on weighted criteria.*  
  - Supports **positive weights** (where higher is better) and **negative weights** (where lower is better, e.g., cost, density).  
  - Outputs a ranked DataFrame of potential materials.

- **`secondary_checker.py`**  
  *Performs advanced threshold checks.*  
  - Verifies if materials meet **application-specific** requirements (e.g., **pontoons**, **frames**, **anchors**).  
  - Generates a validation report.

### 4. **Structural Components & Data Import**
- **`structural_components.py`** & **`structural_data_importer.py`**  
  *Placeholder modules* for integrating with **SolidWorks** or custom Python data for structural analyses.  
  - Currently stubbed out; expand them as you incorporate real structural data.

### 5. **Utilities & Configuration**
- **`utils.py`**  
  *General helper functions.*  
  - Logs errors/warnings, creates directories, loads YAML config, etc.

- **`config.yaml`**  
  *Central configuration file.*  
  - Specifies **file paths**, **alloy patterns**, **property thresholds**, and **weights** for different components.  
  - Adjust values here to tailor the project’s behavior.

### 6. **Additional Files**
- **`metal_1.py`** / **`tryle 2.py`**  
  - Demonstrate **metal diffusion** analysis with linear or error-function fitting.  
  - Loads CSV data and produces **graphs** to evaluate diffusion coefficients over time.

- **`trails.py`**  
  - A small script showing how to fetch or test external data (e.g., from GitHub, SourceForge).

---

## **Repository Structure**
```
river-frog-simulations/
├─ main.py
├─ material_selector.py
├─ alloy_data_unifier.py
├─ secondary_checker.py
├─ graph_reader.py
├─ text_extractor.py
├─ data_validator.py
├─ structural_components.py
├─ structural_data_importer.py
├─ utils.py
├─ metal_1.py
├─ tryle 2.py
├─ trails.py
├─ config.yaml
├─ data/
│   ├─ ...
├─ prototypes/
│   ├─ ...
├─ README.md
```

---

## **Getting Started**

### **1. Installation**
- **Python 3.8+** recommended
- Install dependencies:
  ```bash
  pip install numpy pandas matplotlib scipy opencv-python pyyaml pytesseract
  ```

### **2. Configure Project**
- Update **`config.yaml`** with your file paths, alloy patterns, thresholds, and weights.

### **3. Run the Full Pipeline**
```bash
python main.py
```
1. Prompts you to pick your **data source** (SolidWorks, Python importer, config).  
2. Extracts text, processes graphs, merges + validates data.  
3. Optionally **ranks materials** for your specific application (pontoons, frame, anchors).

---

## **Usage Examples**

**Text Extraction Only:**
```bash
python text_extractor.py
```
- Extracts **OCR** data from a DjVu/PDF and saves to JSON.

**Graph Digitization Only:**
```bash
python graph_reader.py
```
- Reads images (from `paths.graph_output`) and outputs numeric data.

**Material Selection:**
```bash
python material_selector.py
```
- Reads your compiled data (in `data/unified`) and ranks it by **yield strength, tensile strength, density**, etc.

---

## **Contributing**
1. **Fork** the repo & clone your fork.  
2. **Create a branch** for your feature (`git checkout -b feature-xyz`).  
3. Commit & push, then **open a Pull Request**.

If you have suggestions or find bugs, please open an **Issue**.

---

## **License**
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

### **Contact**
For questions or collaboration:
- **Project Lead**: [@alonnad43](https://github.com/alonnad43)  
- **Email**: alonnad@post.bgu.ac.il  

---

**Enjoy exploring River Frog Simulations!** Please feel free to open an Issue or Pull Request with improvements or new features.
