def recall_at(ground_truth, books2, at=10):
    matches = set(ground_truth["id"]) & set(books2.head(at)["id"])
    return len(matches) / len(ground_truth)


def precision_at(ground_truth, books2, at=10):
    matches = set(ground_truth["id"]) & set(books2.head(at)["id"])
    return len(matches) / at
