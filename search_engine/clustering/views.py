from django.shortcuts import render
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# NLTK resources download
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load and preprocess documents
csv_path = '/Users/np-bri-mbp-01/Downloads/IR_Assignment/search_engine/clustering/news.csv'
dataframe = pd.read_csv(csv_path, encoding='latin-1')
docs = dataframe['Summary']

stop_words_set = set(stopwords.words('english'))
lemmatizer_instance = WordNetLemmatizer()

processed_documents = []
for doc in docs:
    tokenized_words = nltk.word_tokenize(doc)
    cleaned_words = [lemmatizer_instance.lemmatize(word.lower()) for word in tokenized_words if word.isalnum() and word.lower() not in stop_words_set]
    processed_documents.append(' '.join(cleaned_words))

# Perform clustering
num_clusters = min(len(docs), 3)
tfidf_vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_df=0.95, min_df=4)
X_matrix = tfidf_vectorizer.fit_transform(processed_documents)

kmeans_instance = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
kmeans_instance.fit(X_matrix)

# Calculate silhouette score
pca_instance = PCA(n_components=2)
X_reduced_matrix = pca_instance.fit_transform(X_matrix.toarray())
silhouette_avg_score = silhouette_score(X_reduced_matrix, kmeans_instance.labels_)
print("Silhouette Score:", silhouette_avg_score)

# Get top words for each cluster
centroids_order = kmeans_instance.cluster_centers_.argsort()[:, ::-1]
terms = tfidf_vectorizer.get_feature_names_out()
top_words_clusters = {}
for i in range(num_clusters):
    top_words_clusters[i] = [terms[ind] for ind in centroids_order[i, :10]]
    print(f"Cluster {i} top words: {top_words_clusters[i]}")

# View function to handle the cluster view
def cluster_view(request):
    return render(request, 'cluster.html')

# View function to handle the cluster result
def cluster_result(request):
    if request.method == 'POST':
        new_document = request.POST.get('document')
        tokenized_new_doc = nltk.word_tokenize(new_document)
        cleaned_new_doc = [lemmatizer_instance.lemmatize(word.lower()) for word in tokenized_new_doc if word.isalnum() and word.lower() not in stop_words_set]
        processed_new_doc = ' '.join(cleaned_new_doc)
        
        new_X_matrix = tfidf_vectorizer.transform([processed_new_doc])
        predicted_cluster = kmeans_instance.predict(new_X_matrix)[0]
        
        cluster_category_mapping = {0: "Entertainment", 1: "Politics", 2: "Economics"}
        cluster_category = cluster_category_mapping.get(predicted_cluster, 'unknown')

        context = {
            'cluster_category': cluster_category,
            # 'silhouette_avg': silhouette_avg_score,
        }
        return render(request, 'result.html', context)

    return render(request, 'cluster.html')
