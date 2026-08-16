from flask import Flask, render_template, request
import pickle
import logging
import os

app = Flask(__name__)

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

# Median subscription age used during training, for the "is_loyal" feature.
# Update this if you retrain the model on different data.
SUBSCRIPTION_AGE_MEDIAN = 1.36

# Create logs folder if not exists
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:

        is_tv_subscriber = float(request.form["is_tv_subscriber"])
        is_movie_package_subscriber = float(
            request.form["is_movie_package_subscriber"]
        )
        subscription_age = float(
            request.form["subscription_age"]
        )
        bill_avg = float(
            request.form["bill_avg"]
        )
        remaining_contract = float(
            request.form["remaining_contract"]
        )
        service_failure_count = float(
            request.form["service_failure_count"]
        )
        download_avg = float(
            request.form["download_avg"]
        )
        upload_avg = float(
            request.form["upload_avg"]
        )
        download_over_limit = float(
            request.form["download_over_limit"]
        )

        # Engineered features (must match the notebook's feature engineering exactly)
        bill_per_age = bill_avg / (subscription_age + 1)
        total_usage = download_avg + upload_avg
        usage_ratio = download_avg / (upload_avg + 1)
        is_loyal = 1 if subscription_age > SUBSCRIPTION_AGE_MEDIAN else 0
        has_both_services = 1 if (is_tv_subscriber == 1 and is_movie_package_subscriber == 1) else 0
        high_failure = 1 if service_failure_count > 2 else 0
        is_over_limit = 1 if download_over_limit > 0 else 0

        features = [[
            is_tv_subscriber,
            is_movie_package_subscriber,
            subscription_age,
            bill_avg,
            remaining_contract,
            service_failure_count,
            download_avg,
            upload_avg,
            download_over_limit,
            bill_per_age,
            total_usage,
            usage_ratio,
            is_loyal,
            has_both_services,
            high_failure,
            is_over_limit
        ]]

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        if prediction == 1:
            result = "⚠️ HIGH CHURN RISK"
        else:
            result = "✅ CUSTOMER LIKELY TO STAY"

        logging.info(
            f"Prediction={result}, "
            f"Probability={round(probability*100,2)}%"
        )

        return render_template(
            "index.html",
            prediction=result,
            probability=round(probability * 100, 2)
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction=f"Error: {str(e)}"
        )


if __name__ == "__main__":
    app.run(debug=True)