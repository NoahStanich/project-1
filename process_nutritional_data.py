from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json
import os
# Copy and replace this exact string in BOTH scripts
connect_str = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"

def process_data():
    # 1. Setup connection to local Azurite
    conn_str = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    
    container_name = 'datasets'
    blob_name = 'All_Diets.csv'

    # 2. Download from "Cloud" (Azurite)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    stream = blob_client.download_blob().readall()
    
    # 3. Process Data
    df = pd.read_csv(io.BytesIO(stream))
    # Note: Ensure column names match your CSV exactly (check for spaces/caps)
    avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

    # 4. Save to "NoSQL" (JSON file)
    output_dir = 'simulated_nosql'
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    
    result = avg_macros.reset_index().to_dict(orient='records')
    with open(f'{output_dir}/results.json', 'w') as f:
        json.dump(result, f, indent=4)

    return "Success: Data processed from Azurite and saved to JSON."

if __name__ == "__main__":
    print(process_data())
