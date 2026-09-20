# %%
# this adaptation of the original script takes the lists of bsb-identifiers from the NFDI Incubator Fund project and downloads the corresponding images from the BSB server. The script can be used to reproduce the original processing steps and image harvesting results of the project.
# venv = base

import requests
from PIL import Image
from io import BytesIO
import os
import json
from tqdm.notebook import tqdm
import random
import datetime

import tensorflow as tf
import numpy as np

# %%
# APIs for working with IIIF
BASE_URL = "https://api.digitale-sammlungen.de/iiif/image/v2"
MANIFEST_URL = "https://api.digitale-sammlungen.de/iiif/presentation/v2"

# %%
# Load the classification model
model = tf.keras.models.load_model('classification_model.keras')

# %%
# File path - replace with path to TXT file containing bsb-identifiers of selected books (see folder 'historical_tables_dataset)
file_path = 'NFDI_234_bsb_identifiers.txt'

# %%
with open(file_path, 'r', encoding='utf-8') as file:
    data = file.readlines()
    print(len(data))
    book_id = data[0].strip()
    print(book_id)

# %%
# Initialize counter
processed = 0
book_count = 0
skipped_books = 0
i = 0

try:
    # Open and read the textfile
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()
        data = data[i:i+10] # add limit for testing purposes
    
    for book in data:
        processed += 1
        if processed > 10: # other means to add limit
            break
        book_id = book.strip()
        manifest_url = f"{MANIFEST_URL}/{book_id}/manifest"
        manifest_response = requests.get(manifest_url)
        manifest_response.raise_for_status()
        manifest = manifest_response.json()
        canvases = manifest['sequences'][0]['canvases']

        sample_size = int(len(canvases) * 1) # set lower value for sampling
        sampled_values = random.sample(range(1, len(canvases) + 1), sample_size)
        sampled_values.sort()

        output_dir = rf"path_to_folder\{book_id}" # rename as needed
        selected_pages = sampled_values
        size = "full" # alternative 'pct:50'
        save_manifest = False # change to False if necessary

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Get selected canvases and extract identifiers
        identifiers = []

        canvas_subset = [canvases[i-1] for i in selected_pages]
        for canvas in canvas_subset:
            image_url = canvas['images'][0]['resource']['service']['@id']
            identifier = image_url.split('/')[-1]
            identifiers.append(identifier)

        # Download pages
        for page_num, identifier in zip(selected_pages, tqdm(identifiers, desc="Downloading pages")):
            output_path = os.path.join(output_dir, f"page_{page_num:04d}.png") # change to tif, jpg or png as needed

            # Skip if file already exists
            if os.path.exists(output_path):
                continue
                
            try:
                # Construct IIIF URL and get image
                image_url = f"{BASE_URL}/{identifier}/full/{size}/0/default.png" # change to jpg, tif or png as needed
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                # When loaded directly as done below, the following line is not necessary, but we do need it to save the image below
                image = Image.open(BytesIO(image_response.content))

                # Classify image
                # Define dimensions to match training
                img_width, img_height = 299, 299

                # Load directly and preprocess (replaces temporary buffer and load and preprocess)
                img = tf.keras.utils.load_img(BytesIO(image_response.content), target_size=(img_width, img_height))
                img_array = tf.keras.utils.img_to_array(img)
                img_array = tf.expand_dims(img_array, 0)
                img_array = img_array / 255.0
                
                # Get prediction
                predictions = model.predict(img_array)

                class_names = ['Table', 'Text', 'TextAndTable', 'Title']
                predicted_class = np.argmax(predictions[0])
                confidence = predictions[0][predicted_class]
                print(f"Predicted Class: {class_names[predicted_class]}")
                print(f"Confidence: {confidence:.2f}")
                    
                # Log the classification results
                log_entry = {
                    'book_id': book_id,
                    'page_num': page_num,
                    'predicted_class': class_names[predicted_class],
                    'confidence': float(confidence),
                    'timestamp': datetime.datetime.now().isoformat()
                }
                    
                # Append to log file using async write
                log_file = os.path.join(output_dir, 'classification_log.jsonl')
                with open(log_file, 'a') as f:
                    f.write(json.dumps(log_entry) + '\n')

                # Save if the image is classified as a Table
                if class_names[predicted_class] == 'Table':
                    # Create a directory for tables if it doesn't exist
                    tables_dir = os.path.join(os.path.dirname(output_path), 'tables_png')
                    os.makedirs(tables_dir, exist_ok=True)
                        
                    # Generate filename with page number and confidence score
                    table_filename = f"{book_id}_{page_num}_conf_{confidence:.2f}.png" # change to tif, jpg or png as needed
                    table_path = os.path.join(tables_dir, table_filename)
                        
                    # Save the table image
                    image.save(table_path, "PNG") # change to TIFF, JPEG or PNG as needed; specify quality=100 for JPEG
                    print(f"Saved table image: {table_filename}")

                # Save if the image is classified as Text and Table
                elif class_names[predicted_class] == 'TextAndTable':
                    # Create a directory for text-and-tables if it doesn't exist
                    text_and_tables_dir = os.path.join(os.path.dirname(output_path), 'text_and_tables_png')
                    os.makedirs(text_and_tables_dir, exist_ok=True)
                        
                    # Generate filename with page number and confidence score
                    text_and_table_filename = f"{book_id}_{page_num}_conf_{confidence:.2f}.png" # change to tif, jpg or png
                    text_and_table_path = os.path.join(text_and_tables_dir, text_and_table_filename)
                        
                    # Save the text-and-table image
                    image.save(text_and_table_path, "PNG") # change to TIF, JPEG or PNG as needed; specify quality=100 for JPEG
                    print(f"Saved text-and-table image: {text_and_table_filename}")

                else:
                    print(f"Skipping non-table image on page {page_num}")
                        
            except Exception as e:
                print(f"Error downloading page {page_num}: {e}")

        print("Download complete!")

        # Create filtered manifest if requested
        if save_manifest:
            # Save manifest
            manifest_path = os.path.join(output_dir, 'manifest.json')
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2)

        book_count += 1
    else:
        skipped_books += 1

    # Print total count
    print(f"\nTotal books processed: {book_count}")
    print(f"\nTotal books skipped (no BSB field): {skipped_books}")
        
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found")
except json.JSONDecodeError:
    print("Error: Invalid JSON format")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")


