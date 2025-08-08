import os,sys,requests
from zipfile import ZipFile

def download_zip_file(url, output_dir):
    response = requests.get(url, stream=True)
    os.makedirs(output_dir, exist_ok=True)
    if response.status_code == 200:
        filename = os.path.join(output_dir, "downloaded.zip")
      
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"Downloaded zip file : {filename}")
        return filename
    else:
        raise Exception(f"Failed to download file: Status code {response.status_code}")

def extract_zip_file(zip_filename, output_dir):

    with ZipFile(zip_filename, "r") as zip_file:
        zip_file.extractall(output_dir)
    
    print(f"Extracted files written to: {output_dir}")
    print("Removing the zip file")
    os.remove(zip_filename)

def fix_json_dict(output_dir):
    import json
    file_path = os.path.join(output_dir,"dict_artists.json")
    with open(file_path, "r") as f:
        data = json.load(f)

    with open(os.path.join(output_dir,"fixed_da.json"), "w", encoding="utf-8") as f_out:
        for key, value in data.items():
            record = {"id": key, "related_ids": value}
            json.dump(record, f_out, ensure_ascii=False)
            f_out.write("\n")
        print (f"File {file_path} has been fixed and written to {output_dir} as fixed_da.json")
    print("Removing the original file")
    os.remove(file_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Extraction path is required")
        print("Exame Usage:")
        print("python3 execute.py /home/ardent-sharma/Data/Extraction")
    else:
        try:
            print("Starting Extraction Engine...")
            EXTRACT_PATH = sys.argv[1]
            KAGGLE_URL = "https://storage.googleapis.com/kaggle-data-sets/1993933/3294812/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20250628%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250628T075038Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=2082e7ae514ed7398f77ed43b80890b9b76de7c92676a59b5f26a4b7a376e5790ea9f1b7cfd354b76fad5bf2800dd1b9b17068326adf0d0c08b7e8d2cd7afc964678e8a700af71a46743ee946d17dda3be1de05fc5a17db4c223d8fc8d02dc31cd5aa1f7629ab8e98c6ea069b5fa3ff0ed05d0e6d1840d279616c06c2b442bbf40aaf0a20e683ee605c44e8a4d618c07c6f7d17a06b35b7068e7460732ea6ad2f4cf164ccb40543c5fe1f56b6c1376ccf7a2fd323316251710ea530ce288f505519265b10d39ffd308632bf4e62c43fcdb9bedbc3425b151c4d4594c4efd32f084d8e8962b18be642e535d8060f10449d0b482611cabfe640650185a25bfad63"
            zip_filename = download_zip_file(KAGGLE_URL, EXTRACT_PATH)
            extract_zip_file(zip_filename, EXTRACT_PATH)
            fix_json_dict(EXTRACT_PATH)
            print("Extraction Sucessfully Completed!!!")
        except Exception as e:
            print(f"Error: {e}")