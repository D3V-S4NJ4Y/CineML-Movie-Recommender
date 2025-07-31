from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# REPO_NAME = "ML Based Movies Recommender System"
AUTHOR_NAME = "BAPPY AHMED"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = ['streamlit']


setup(
    name=SRC_REPO,
    version="0.0.1",
    author = AUTHOR_NAME,
    author_email="entbappy73@gmail.com",
    description="A small local packages for ML based movies recommendations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/entbappy/ML-Based-Movies-Recommender-System",
    packages=[SRC_REPO],
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)