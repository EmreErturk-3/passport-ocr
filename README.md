

# 🇹🇷 Turkish Passport Data Extractor

This Python script is designed to extract key information from the Machine Readable Zone (MRZ) of a Turkish passport image. It uses the `passporteye` library with a custom layer of logic to handle common OCR errors, clean the data, and format it for easy use.

## ✨ Features

  - **Robust Data Extraction**: Parses the MRZ to get the passport holder's name, passport number, TC number, dates of birth and expiry, and more.
  - **Intelligent OCR Correction**: Includes a regular expression to handle common OCR misreadings of the `<` padding character as `k` or `s`.
  - **Clean & Formatted Output**: Formats dates into `YYYY-MM-DD` and cleans up the Turkish Republic ID number (TC Number) and names by removing padding.
  - **Debugging Support**: Provides both the cleaned, final data and the raw data from the MRZ for troubleshooting.

## 🛠️ Prerequisites

This script requires the **Tesseract OCR engine** and the `passporteye` Python library.

1.  **Install Tesseract OCR**:

      * **Windows**: Download and install the Tesseract executable. During the installation, ensure you select the **Turkish language data** (`tur.traineddata`) for optimal accuracy.
      * **macOS**: Use Homebrew: `brew install tesseract`.
      * **Linux (Debian/Ubuntu)**: Use APT: `sudo apt install tesseract-ocr tesseract-ocr-tur`.

2.  **Add Tesseract to System PATH**:

      * The Tesseract executable must be in your system's PATH. Windows installers often handle this automatically. For macOS and Linux, package managers typically do the same.

3.  **Install Python Libraries**:

      * Install `passporteye` and `pytesseract` via pip:
        ```bash
        pip install passporteye pytesseract
        ```

4.  **Configure Tesseract Path in the Script (Optional)**:

      * If you encounter a `TesseractNotFoundError`, you may need to manually specify the path to the Tesseract executable in your script. Add the following line at the top of your `.py` file, updating the path to match your installation.
        ```python
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Example for Windows
        ```

## 🚀 How to Use

1.  **Save the Script**: The script is `passport_mrz.py`; pass an image path as the first argument.

2.  **Update the Image Path**: Modify the `image_file_path` variable in the `if __name__ == "__main__":` block to point to your passport image file.

3.  **Run the Script**: Execute the file from your terminal.

    ```bash
    python passport_mrz.py samples/Tr_sample1.jpg
    ```

### Example Output

A successful run will produce a clear, formatted output of the extracted data:

```
🔍 Extracting data from 'sample/sample1.jpg'...

────────────────────────────────────────
🇹🇷 Turkish Passport Data Extracted Successfully 🇹🇷
────────────────────────────────────────
Name         : GIVEN NAMES
TC Number    : 12345678901
Passport No. : T12345678
Birth Date   : 1990-01-01
Expiry Date  : 2029-10-02
Sex          : M
MRZ Valid    : True
Accuracy     : 95%

--- Raw Data for Debugging ---
Raw surname        : 'SURNAME'
Raw given names    : 'GIVEN<NAMES<<<<<<<<<<<<<<<<<<'
Raw personal number: '12345678901<<<<<<<<<<<<<'

--- Raw MRZ Lines ---
Line 1: 'P<TURSURNAME<<GIVEN<NAMES<<<<<<<<<<<<<<<<<<'
Line 2: 'T12345678<9TUR1234567M291002912345678901<<<<<'
────────────────────────────────────────
```

## 📜 Code Explanation

The `extract_turkish_passport_data` function is the core of the script. It first uses `passporteye.read_mrz()` to get the raw MRZ data. Then, it applies custom logic:

  * A regular expression (`re.search(r'[<ks]{3,}', raw_given_names)`) is used to find and remove the `<` padding characters, which are often misread by OCR.
  * The `personal_number` is cleaned to extract only the 11-digit TC Number.
  * Dates are formatted from `YYMMDD` to `YYYY-MM-DD`, with a rule to infer the century for birth dates (e.g., `< 25` is assumed to be `20xx`, `> 25` is assumed to be `19xx`).
  * Finally, it returns a dictionary with both the cleaned and raw data for comprehensive results.
## Samples

`samples/` holds public **specimen** passports only (ICAO "Utopia", Turkish "ÖRNEK" and French
"SPECIMEN" documents). No real person's data is included.
