import pandas as pd
import os
import pickle
import re
import string
from parser import get_details

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics


def clean_data(df):
    df.drop_duplicates(subset=["Resume"], keep="first", inplace=True)
    df.reset_index(inplace=True, drop=True)
    return df


def clean_resume(text: str):
    details, text = get_details(text)

    # clean links
    text = re.sub(r"http\S+", " ", text)

    # remove all punctuation
    expr = re.escape(string.punctuation)
    text = re.sub(r"[{}]".format(expr), " ", text)

    # remove all non ascii
    text = re.sub(r"[^\x00-\x7f]", " ", text)

    # remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text


def train_knn():
    df = pd.read_csv("UpdatedResumeDataSet.csv", encoding="utf-8")
    df = clean_data(df)
    df["Clean"] = df["Resume"].apply(clean_resume)

    le = LabelEncoder()
    df["Category"] = le.fit_transform(df["Category"])

    resumes = df["Clean"].values
    categories = df["Category"].values

    # vectorize resume data by vocab by TF-IDF strategy
    vectorizer = TfidfVectorizer(sublinear_tf=True, stop_words="english")
    vectorizer.fit(resumes)
    features = vectorizer.transform(resumes)

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        categories,
        test_size=0.2,
        shuffle=True,
        stratify=categories,
        random_state=2024,
    )

    # choose highest freq label in neighbors
    model = KNeighborsClassifier()
    model.fit(X_train, y_train)

    # print(f"train accuracy {model.score(X_train, y_train)}")
    # print(f"test accuracy {model.score(X_test, y_test)}")
    # print(f"classifying {model}")
    #
    # pred = model.predict(X_test)
    # print(metrics.classification_report(y_test, pred, zero_division=True))

    return model, le, vectorizer


class ResumeKNN:
    model: KNeighborsClassifier = None
    encoder: LabelEncoder = None
    vectorizer: TfidfVectorizer = None

    def __init__(self):
        self.model, self.encoder, self.vectorizer = train_knn()

    def get_categories(self):
        return self.encoder.classes_

    def predict(self, data):
        if isinstance(data, str):
            data = [data]
        if not isinstance(data, list):
            print(f"predict with {type(data)}")
            assert False

        data = [clean_resume(x) for x in data]
        features = self.vectorizer.transform(data)
        pred = self.model.predict(features)
        return self.encoder.inverse_transform(pred)

    def predict_proba(self, data):
        if not isinstance(data, list):
            data = [data]

        data = [clean_resume(x) for x in data]
        features = self.vectorizer.transform(data)
        return self.model.predict_proba(features)


def get_job_weights(job):
    df = pd.read_csv("UpdatedResumeDataSet.csv", encoding="utf-8")
    df = clean_data(df)
    df["Clean"] = df["Resume"].apply(clean_resume)
    df = df[df["Category"] == job]
    sample = df["Clean"].to_list()
    knn = ResumeKNN()
    weights = knn.vectorizer.transform(sample).todense()
    tokens = knn.vectorizer.get_feature_names_out()
    for j in range(len(sample)):
        res = [(weights[j, i].item(), tokens[i]) for i in range(len(tokens))]
        res = sorted(res, key=lambda x: x[0], reverse=True)
        for a, b in res[:30]:
            print(a, b)
        print()


def test():
    df = pd.read_csv("UpdatedResumeDataSet.csv", encoding="utf-8")
    df = clean_data(df)
    df["Clean"] = df["Resume"].apply(clean_resume)
    sample = df["Clean"].sample(30).to_list()
    knn = ResumeKNN()
    print(knn.get_categories())
    print(knn.predict(sample))


if __name__ == "__main__":
    get_job_weights("Data Science")
    # test()
