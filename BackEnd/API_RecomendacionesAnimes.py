from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import os
import html
import random

app = Flask(__name__)

vers = "0.0.1"

# ============================
# VARIABLES GLOBALES
# ============================

corrMatrix = None
anime = None
ratings = None

# ============================
# FUNCIÓN DE ENTRENAMIENTO
# ============================

def entrenar_modelo():
    """Carga los CSV y genera la matriz de correlación de animes."""
    global corrMatrix, anime, ratings

    base_path = os.getcwd()
    anime_file = os.path.join(base_path, "anime.csv")
    ratings_file = os.path.join(base_path, "rating.csv")

    anime_cols = ['anime_id', 'name', 'genre', 'type', 'episodes', 'rating', 'members']
    ratings_cols = ['user_id', 'anime_id', 'rating']

    anime = pd.read_csv(anime_file, names=anime_cols, header=0, encoding="utf-8")
    ratings = pd.read_csv(ratings_file, names=ratings_cols, header=0, encoding="utf-8")

    anime['name'] = anime['name'].apply(html.unescape)
    anime['episodes'] = anime['episodes'].replace('Unknown', np.nan).astype(float)
    anime['genre'] = anime['genre'].fillna('Unknown')
    anime['rating'] = anime['rating'].fillna(anime['rating'].mean())
    anime['type'] = anime['type'].fillna('Unknown')
    anime = anime.dropna(subset=['episodes', 'rating', 'type', 'genre'])

    ratings = ratings[ratings['rating'] != -1]
    ratings = ratings.dropna(subset=['user_id', 'anime_id', 'rating'])
    ratings = ratings.rename(columns={"rating": "user_rating"})
    anime = anime.rename(columns={"rating": "anime_rating"})

    ratings_with_name = ratings.merge(anime[['anime_id', 'name']], on='anime_id', how='inner')
    ratings_with_name['name'] = ratings_with_name['name'].astype('category')
    ratings_with_name['user_id'] = ratings_with_name['user_id'].astype('category')

    # Filtrar animes populares
    anime_counts = ratings_with_name['name'].value_counts()
    popular_animes = anime_counts[anime_counts > 400].index
    filtered = ratings_with_name[ratings_with_name['name'].isin(popular_animes)]

    ratings_pivot = filtered.pivot_table(
        index='user_id',
        columns='name',
        values='user_rating',
        aggfunc='mean',
        observed=True
    ).astype('float32')

    corrMatrix = ratings_pivot.corr(method='pearson', min_periods=250)
    print("✅ Entrenamiento completado. Matriz de correlación generada.")



###     EndPoints
@app.route("/version", methods=["GET"])
def version():
    return jsonify({"version": vers}), 200

@app.route("/entrenar", methods=["POST"])
def entrenar():
    try:
        entrenar_modelo()
        return jsonify({"mensaje": "Modelo entrenado correctamente"}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error durante el entrenamiento: {str(e)}"}), 500


@app.route("/recomendar", methods=["POST"])
def recomendar():
    global corrMatrix

    if corrMatrix is None:
        return jsonify({"error": "El modelo no está entrenado. Llama primero a /entrenar"}), 400

    try:
        user_ratings = request.json  # Diccionario enviado desde consola
        if not user_ratings:
            return jsonify({"error": "Debes enviar un JSON con las calificaciones del usuario"}), 400

        # Filtrar solo animes conocidos
        available_animes = [a for a in user_ratings.keys() if a in corrMatrix.columns]
        if not available_animes:
            return jsonify({"error": "Ninguno de los animes enviados está en el modelo"}), 400

        myRatings = pd.Series({anime: user_ratings[anime] for anime in available_animes})

        simCandidates = pd.Series(dtype='float64')
        for anime_name, rating_value in myRatings.items():
            sims = corrMatrix[anime_name].dropna()
            sims = sims.map(lambda x: x * rating_value)
            simCandidates = pd.concat([simCandidates, sims])

        simCandidates = simCandidates.groupby(simCandidates.index).sum()
        simCandidates.sort_values(inplace=True, ascending=False)
        filteredSims = simCandidates.drop(myRatings.index, errors='ignore')

        top_recommendations = filteredSims.head(10).to_dict()

        return jsonify({
            "usuario_ratings": user_ratings,
            "recomendaciones_top_10": top_recommendations
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error generando recomendaciones: {str(e)}"}), 500


@app.route("/animes", methods=["GET"])
def obtener_animes():
    """Devuelve 50 animes aleatorios [id, nombreAnime]."""
    global anime

    if anime is None:
        return jsonify({"error": "Los datos de anime no están cargados. Llama primero a /entrenar"}), 400

    try:
        sample = anime.sample(n=50, random_state=random.randint(0, 9999))
        lista = sample[['anime_id', 'name']].values.tolist()
        return jsonify({"animes": lista}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"No se pudieron obtener los animes: {str(e)}"}), 500


# ============================
# MAIN
# ============================

if __name__ == "__main__":
    app.run(debug=True)
