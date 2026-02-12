from azure.storage.blob import BlobServiceClient
import os

# Your exact Connection String from the screenshot
conn_str = "AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;DefaultEndpointsProtocol=http;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"

def push_to_azurite():
    local_file = "simulated_nosql/results.json"
    container_name = "datasets"
    
    if not os.path.exists(local_file):
        print(f"❌ ERROR: File '{local_file}' not found. Run your processing script first!")
        return

    try:
        # Connect using your screenshot's string
        service_client = BlobServiceClient.from_connection_string(conn_str)
        container_client = service_client.get_container_client(container_name)
        
        # Create container if missing
        if not container_client.exists():
            container_client.create_container()
            print(f"Created container: {container_name}")

        # Upload the processed JSON
        blob_client = container_client.get_blob_client("results.json")
        with open(local_file, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        
        print("✅ SUCCESS: Data sent to Azurite successfully!")
        print(f"URL: http://127.0.0.1{container_name}/results.json")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    push_to_azurite()
