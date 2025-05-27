import matplotlib.pyplot as plt
from transform.data_type_export.dto import EntityDTO
from typing import List

def plot_entity_distribution(entities: List[EntityDTO], title="Entity Distribution"):
    counts = [e.count for e in entities]
    names = [e.text for e in entities]

    plt.figure(figsize=(10, 6))
    plt.bar(names, counts)
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()
