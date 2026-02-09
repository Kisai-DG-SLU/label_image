"""
Clustering module for BrainScanAI.

Provides clustering algorithms for weak labeling of MRI images.
"""

import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import davies_bouldin_score, silhouette_score


class ClusterLabeler:
    """Generate weak labels using clustering algorithms."""

    def __init__(self, n_clusters: int = 5, algorithm: str = "kmeans"):
        self.n_clusters = n_clusters
        self.algorithm = algorithm
        self.model = None
        self.labels_ = None

    def fit(self, features: np.ndarray) -> np.ndarray:
        """Fit clustering model and return cluster labels."""
        if self.algorithm == "kmeans":
            self.model = KMeans(n_clusters=self.n_clusters, random_state=42)
        elif self.algorithm == "dbscan":
            self.model = DBSCAN(eps=0.5, min_samples=5)
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")

        if self.model is None:
            raise RuntimeError("Clustering model initialization failed")

        self.labels_ = self.model.fit_predict(features)
        return self.labels_

    def evaluate(self, features: np.ndarray) -> dict:
        """Evaluate clustering quality."""
        if self.labels_ is None:
            raise ValueError("Model must be fitted first")

        # Calculate silhouette score (higher is better)
        silhouette = silhouette_score(features, self.labels_)

        # Calculate Davies-Bouldin index (lower is better)
        db_index = davies_bouldin_score(features, self.labels_)

        # Count clusters
        unique_labels = np.unique(self.labels_)
        n_clusters_found = len(unique_labels)

        return {
            "silhouette_score": silhouette,
            "davies_bouldin_index": db_index,
            "n_clusters_found": n_clusters_found,
            "cluster_sizes": (
                np.bincount(self.labels_ + 1)
                if -1 not in self.labels_
                else np.bincount(self.labels_[self.labels_ != -1] + 1)
            ),
        }

    def reduce_dimensions(
        self, features: np.ndarray, method: str = "pca", n_components: int = 2
    ) -> np.ndarray:
        """Reduce feature dimensions for visualization."""
        if method == "pca":
            reducer = PCA(n_components=n_components, random_state=42)
        elif method == "tsne":
            reducer = TSNE(n_components=n_components, random_state=42, perplexity=30)
        else:
            raise ValueError(f"Unsupported reduction method: {method}")

        return reducer.fit_transform(features)
