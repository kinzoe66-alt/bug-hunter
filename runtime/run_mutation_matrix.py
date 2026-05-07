
from runtime.anomaly_logger import persist_anomaly

# Wrap printing of differences to also persist them
for mutation_name, diff_data in mutation_matrix.items():
    headers = diff_data.get("headers", {})
    differences = diff_data.get("differences", {})
    
    if differences:  # only log if a real difference exists
        filename = persist_anomaly(
            mutation_name,
            headers,
            differences,
        )
        print(f"Persisted anomaly: {filename}")
