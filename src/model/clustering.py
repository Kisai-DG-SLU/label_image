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
            # Use larger eps for better clustering with typical feature scales
            self.model = DBSCAN(eps=3.0, min_samples=5)
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

        # Count clusters (excluding noise points labeled -1)
        unique_labels = np.unique(self.labels_)
        n_clusters_found = len(unique_labels)

        # Handle case where all points are noise or only one cluster found
        valid_labels = self.labels_[self.labels_ != -1]
        if len(np.unique(valid_labels)) < 2:
            # Not enough clusters for silhouette and Davies-Bouldin scores
            silhouette = np.nan
            db_index = np.nan
            cluster_sizes = np.array([])
        else:
            # Calculate silhouette score (higher is better)
            silhouette = silhouette_score(features, self.labels_)

            # Calculate Davies-Bouldin index (lower is better)
            db_index = davies_bouldin_score(features, self.labels_)

            # Calculate cluster sizes
            if -1 not in self.labels_:
                cluster_sizes = np.bincount(self.labels_ + 1)
            else:
                cluster_sizes = np.bincount(self.labels_[self.labels_ != -1] + 1)

        return {
            "silhouette_score": silhouette,
            "davies_bouldin_index": db_index,
            "n_clusters_found": n_clusters_found,
            "cluster_sizes": cluster_sizes,
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
