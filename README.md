# Online News Popularity Analysis

## Overview
This repository contains our analysis of online news popularity, exploring the factors that contribute to article engagement and developing models to predict article shares, content categorization, and topicality clustering via supervised and unsupervised learning techniques.

## Repository Structure

- **article_shares_classification_clustering.ipynb**: Core code for our analysis, containing all data preprocessing, model development, evaluation, and visualizations.

- **article_shares_classification_clustering_report.pdf**: Comprehensive report detailing our methodology, findings, and conclusions.

- **OnlineNewsPopularity.csv**: Original dataset containing features of online news articles.

- **Sample Files**:
  - `all_features_v2_sample.pkl`/`all_features_v2_sample.parquet`: Sample of our feature-engineered dataset.
  - `title_embeddings_sample.npy`/`content_embeddings_sample.npy`: Sample text embeddings generated from article titles and content.

## Project Highlights

- **Supervised Learning**: We developed regression models to predict article shares and classification models to categorize articles.

- **Unsupervised Learning**: We explored natural groupings within articles to identify patterns that might not be captured by predefined categories.

- **Applications**:
  1. Ad pricing framework that categorizes articles by expected share volume
  2. Automated content classification system for efficient article categorization

## Data Source

The original dataset is from the UCI Machine Learning Repository: [Online News Popularity Data Set](https://archive.ics.uci.edu/ml/datasets/Online+News+Popularity)

## Authors

- Kyle Ziegler, Venkat Panyam, Chris Roy
