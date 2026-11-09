import sys
import re
from passporteye import read_mrz


def extract_turkish_passport_data(image_path):
    """
    Extracts all data from a Turkish passport image, handling common OCR errors.
    """
    try:
        mrz_data = read_mrz(image_path)
    except Exception as e:
        return {'success': False, 'error': f"An error occurred with passporteye: {e}"}

    if mrz_data:
        mrz_dict = mrz_data.to_dict()

        # Clean the TC number (remove padding)
        tc_number = mrz_dict.get('personal_number', '').replace('<', '').strip()

        # Format birth date properly
        birth_raw = mrz_dict.get('date_of_birth', '')
        birth_formatted = ''
        if birth_raw and len(birth_raw) == 6:
            # Handle century ambiguity. Assumes current year is ~2025.
            # If YY is e.g., 00-25, it's 20YY. If it's 26-99, it's 19YY.
            birth_year_prefix = '20' if int(birth_raw[0:2]) < 25 else '19'
            birth_formatted = f"{birth_year_prefix}{birth_raw[0:2]}-{birth_raw[2:4]}-{birth_raw[4:6]}"

        # Format expiry date
        expiry_raw = mrz_dict.get('expiration_date', '')
        expiry_formatted = ''
        if expiry_raw and len(expiry_raw) == 6:
            expiry_formatted = f"20{expiry_raw[0:2]}-{expiry_raw[2:4]}-{expiry_raw[4:6]}"

        # --- ROBUST NAME CLEANING LOGIC ---
        raw_given_names = mrz_dict.get('names', '')

        # 1. Find where the padding starts. Padding is defined as 3 or more
        #    consecutive characters that are '<', 'k', or 's' (common OCR errors for '<').
        padding_match = re.search(r'[<ks]{3,}', raw_given_names)

        # 2. If we found a padding block, truncate the string to get only the name.
        if padding_match:
            name_part = raw_given_names[:padding_match.start()]
        else:
            # Otherwise, the whole string is the name.
            name_part = raw_given_names

        # 3. In the clean name part, replace the official '<' separator with a space.
        cleaned_given_names = name_part.replace('<', ' ').strip()

        # Get raw MRZ text if available
        raw_mrz_lines = []
        if 'raw_text' in mrz_data.aux:
            raw_mrz_lines = mrz_data.aux['raw_text'].split('\n')

        return {
            'success': True,

            # Cleaned Data
            'surname': mrz_dict.get('surname', ''),
            'given_names': cleaned_given_names,
            'passport_number': mrz_dict.get('number', ''),
            'tc_number': tc_number,
            'nationality': mrz_dict.get('nationality', ''),
            'birth_date': birth_formatted,
            'expiry_date': expiry_formatted,
            'sex': mrz_dict.get('sex', ''),
            'valid': mrz_dict.get('valid', False),
            'accuracy_score': mrz_dict.get('valid_score', 0),

            # Raw Data
            'raw_data': {
                'surname': mrz_dict.get('surname', ''),
                'given_names': raw_given_names,
                'passport_number': mrz_dict.get('number', ''),
                'personal_number': mrz_dict.get('personal_number', ''),
                'birth_date': birth_raw,
                'expiry_date': expiry_raw,
                'mrz_lines': raw_mrz_lines
            }
        }
    else:
        return {'success': False, 'error': 'No MRZ found in the image.'}


# --- To run this script directly ---
if __name__ == "__main__":
    # !!! IMPORTANT: Replace this with the actual path to your passport image file !!!
    image_file_path = sys.argv[1] if len(sys.argv) > 1 else "samples/Tr_sample1.jpg"

    print(f"🔍 Extracting data from '{image_file_path}'...")
    result = extract_turkish_passport_data(image_file_path)

    if result['success']:
        print("\n" + "─" * 40)
        print("🇹🇷 Turkish Passport Data Extracted Successfully 🇹🇷")
        print("─" * 40)
        print(f"Name         : {result['given_names']} {result['surname']}")
        print(f"TC Number    : {result['tc_number']}")
        print(f"Passport No. : {result['passport_number']}")
        print(f"Birth Date   : {result['birth_date']}")
        print(f"Expiry Date  : {result['expiry_date']}")
        print(f"Sex          : {result['sex']}")
        print(f"MRZ Valid    : {result['valid']}")
        print(f"Accuracy     : {result['accuracy_score']}%")

        print("\n--- Raw Data for Debugging ---")
        print(f"Raw surname        : '{result['raw_data']['surname']}'")
        print(f"Raw given names    : '{result['raw_data']['given_names']}'")
        print(f"Raw personal number: '{result['raw_data']['personal_number']}'")

        if result['raw_data']['mrz_lines']:
            print("\n--- Raw MRZ Lines ---")
            for i, line in enumerate(result['raw_data']['mrz_lines'], 1):
                print(f"Line {i}: '{line}'")
        print("─" * 40)
    else:
        print(f"\n❌ ERROR: {result['error']}")