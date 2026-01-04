# CineML: Advanced Movie Recommender System

<img src="cineMl.png" alt="CineML Logo" width="70%">

An intelligent movie recommendation system built with machine learning that analyzes over 1 million movies to provide personalized recommendations. The system uses TF-IDF vectorization and cosine similarity to find movies with similar content, themes, and characteristics.

## 🎬 Features

- **1M+ Movie Database**: Comprehensive dataset with detailed movie information
- **Real-time Recommendations**: Instant suggestions based on content similarity
- **Interactive Web Interface**: Clean, user-friendly Streamlit application
- **Movie Posters**: Real movie posters fetched from TMDB API
- **Batch Loading**: Progressive loading for better performance
- **Smart Caching**: Optimized API calls with intelligent caching


## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Machine Learning**: Scikit-learn (TF-IDF, Cosine Similarity, KNN)
- **Data Processing**: Pandas, NumPy
- **Text Processing**: NLTK
- **API Integration**: TMDB API for movie posters
- **Deployment**: Render (Cloud Platform)

## 📊 Algorithm

The recommendation system uses:

1. **TF-IDF Vectorization**: Converts movie descriptions into numerical vectors
2. **Cosine Similarity**: Measures similarity between movies based on content
3. **K-Nearest Neighbors**: Finds the most similar movies efficiently
4. **Content-Based Filtering**: Recommends movies based on plot, genre, and keywords

## 🏗️ Project Structure

```
Movie-Recommender-1M/
├── app.py                          # Main Streamlit application
├── artifacts/
│   ├── movies.pkl                  # Processed movie dataset
│   └── all_neighbors.pkl          # Pre-computed similarity indices
├── data/
│   └── TMDB_movie_dataset_v11.csv # Raw dataset (1M+ movies)
├── Recommender system.ipynb       # Model training notebook
├── requirements.txt               # Python dependencies
├── render.yaml                    # Render deployment config
├── Procfile                       # Process configuration
└── setup.sh                       # Deployment setup script
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.7+
- Git

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/D3V-S4NJ4Y/CineML-Movie-Recommender.git
cd CineML-Movie-Recommender
```

2. **Create virtual environment**
```bash
python -m venv movie-env
source movie-env/bin/activate  # On Windows: movie-env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the app**
Open your browser and go to `http://localhost:8501`

## 🌐 Deployment on Render

### Automatic Deployment

1. **Fork this repository** to your GitHub account

2. **Connect to Render**
   - Go to [Render Dashboard](https://render.com/)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Deploy**
   - Click "Apply" to start deployment
   - Your app will be live at `https://your-app-name.onrender.com`

### Manual Deployment

1. **Create Web Service**
   - Go to Render Dashboard
   - Click "New" → "Web Service"
   - Connect GitHub repository

2. **Configure Service**
   - **Name**: movie-recommender-app
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

## 📈 Model Performance

- **Dataset Size**: 1,209,193 movies
- **Features Used**: Overview, Genres, Keywords, Production Companies
- **Vectorization**: TF-IDF with 10,000 features
- **Similarity Metric**: Cosine Similarity
- **Recommendation Speed**: < 1 second for 100 recommendations

## 🎯 How It Works

1. **Data Preprocessing**
   - Extract relevant features (overview, genres, keywords)
   - Clean and normalize text data
   - Apply stemming using Porter Stemmer

2. **Feature Engineering**
   - Combine all text features into tags
   - Convert to TF-IDF vectors
   - Build similarity matrix using cosine similarity

3. **Recommendation Generation**
   - Find K-nearest neighbors for selected movie
   - Rank by similarity score
   - Fetch movie posters from TMDB API
   - Display results with progressive loading

## 🔑 API Configuration

The app uses TMDB API for movie posters. The API key is included for demo purposes, but for production use:

1. Get your API key from [TMDB](https://www.themoviedb.org/settings/api)
2. Replace the API key in `app.py`
3. Consider using environment variables for security

## 🚀 Performance Optimizations

- **Caching**: Streamlit caching for API calls and computations
- **Batch Loading**: Load recommendations in batches of 10
- **Session Management**: Retry strategy for API failures
- **Progressive Display**: Show results as they load
- **Optimized Vectors**: Pre-computed similarity indices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TMDB**: For providing the comprehensive movie database
- **Streamlit**: For the amazing web framework
- **Scikit-learn**: For machine learning algorithms
- **Render**: For free hosting platform

## 📞 Contact

- **Author**: Your Name
- **Email**: your.email@example.com
- **LinkedIn**: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- **GitHub**: [Your GitHub](https://github.com/yourusername)

---

⭐ **Star this repository if you found it helpful!**