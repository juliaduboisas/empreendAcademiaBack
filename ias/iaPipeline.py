import pandas as pd
import numpy as np
import warnings

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, KFold, LeaveOneOut, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.exceptions import ConvergenceWarning
from ctgan import CTGAN
from google.colab import files

def runAIPipeline():
    newModel: modelResults
    results = []

    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    uploaded = files.upload()

    df = pd.read_csv("../database.csv")

    # Retira colunas não utilizadas no treino
    df_model = df.drop(columns=["Nome", "aluno_id", "unidade"])

    # Converte Status para binário
    df_model["Status"] = df_model["Status"].map({"Cancelou": 1, "Ativo": 0})

    # Remove a coluna de objetivo (vai entrar depois como variável categórica one-hot)
    df_model = df_model.drop(columns=["Objetivo"])

    # Normalizacao
    num_cols = df_model.drop(columns=["Status"]).columns

    scaler = StandardScaler()
    df_model[num_cols] = scaler.fit_transform(df_model[num_cols])

    real_data = df_model.copy()

    # CTGAN
    # Somente Status é categórico
    discrete_columns = ['Status']

    ctgan = CTGAN(
        epochs=300,
        batch_size=16,
        generator_dim=(128,128),
        discriminator_dim=(128,128),
        pac=1,
        verbose=True
    )

    ctgan.fit(real_data, discrete_columns)

    synthetic_data = ctgan.sample(10000)

    # Separacao treino/teste
    X_real = real_data.drop(columns=["Status"])
    y_real = real_data["Status"]

    X_synth = synthetic_data.drop(columns=["Status"])
    y_synth = synthetic_data["Status"]

    X_train, X_test, y_train, y_test = train_test_split(X_synth, y_synth, test_size=0.2, random_state=42)


    # Arvore de Decisao e Regressao Logistica
    models = {
        "Árvore de Decisão": DecisionTreeClassifier(max_depth=5, random_state=42),
        "Regressão Logística": LogisticRegression(penalty="l1", solver="saga", max_iter=10000, random_state=42)
    }

    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        print("\n====================")
        print(f"MODELO: {name}")
        print("====================")
        print("Acurácia :", accuracy_score(y_test, pred))
        print("Precisão :", precision_score(y_test, pred))
        print("Recall   :", recall_score(y_test, pred))
        print("F1-score :", f1_score(y_test, pred))

        newModel.setAlgorithm(name)
        newModel.setCrossValidation("none")
        newModel.setSyntheticData("CTGAN")
        newModel.setAccuracy(accuracy_score(y_test, pred))
        newModel.setPrecision(precision_score(y_test, pred))
        newModel.setRecall(recall_score(y_test, pred))
        newModel.setF1(f1_score(y_test, pred))

        results.append(newModel)


    # Validacao Cruzada (K-fold e LOO)
    for name, model in models.items():
        print("\n" + "#"*25, name.upper(), "#"*25)

        print("\n--- K-FOLD (dados reais) ---")
        kf = KFold(n_splits=10, shuffle=True, random_state=42)
        print("Acurácia:", np.mean(cross_val_score(model, X_real, y_real, cv=kf, scoring='accuracy')))
        print("Precisão:", np.mean(cross_val_score(model, X_real, y_real, cv=kf, scoring='precision')))
        print("Recall  :", np.mean(cross_val_score(model, X_real, y_real, cv=kf, scoring='recall')))
        print("F1      :", np.mean(cross_val_score(model, X_real, y_real, cv=kf, scoring='f1')))

        newModel.setAlgorithm(name)
        newModel.setCrossValidation("K-Fold")
        newModel.setSyntheticData("none")
        newModel.setAccuracy(accuracy_score(y_test, pred))
        newModel.setPrecision(precision_score(y_test, pred))
        newModel.setRecall(recall_score(y_test, pred))
        newModel.setF1(f1_score(y_test, pred))

        results.append(newModel)


        print("\n--- METODO LOO (dados reais) ---")
        loo = LeaveOneOut()
        preds, trues = [], []
        for tr, te in loo.split(X_real):
            model.fit(X_real.iloc[tr], y_real.iloc[tr])
            preds.append(model.predict(X_real.iloc[te])[0])
            trues.append(y_real.iloc[te])

        print("Acurácia:", accuracy_score(trues, preds))
        print("Precisão:", precision_score(trues, preds))
        print("Recall  :", recall_score(trues, preds))
        print("F1      :", f1_score(trues, preds))

        newModel.setAlgorithm(name)
        newModel.setCrossValidation("Leave-One-Out")
        newModel.setAccuracy(accuracy_score(y_test, pred))
        newModel.setPrecision(precision_score(y_test, pred))
        newModel.setRecall(recall_score(y_test, pred))
        newModel.setF1(f1_score(y_test, pred))

        results.append(newModel)

    return results


