import pandas as pd

results = {
    "Ridge": [0.559,"NaN", 0.522,"NaN"],
    "RF": [0.476, "NaN",0.653,"NaN"],
    "RidgeCV": [0.559, "NaN", 0.522,"NaN"],
    "RFCV": [0.473, "NaN", 0.657,"NaN"],
    "GB": [0.476, "NaN", 0.653,"NaN"],
    "GBCV": [0.471, "NaN", 0.661,"NaN"],
    "Simple_Ens": [0.466, "NaN", 0.668,"NaN"],
    "Voting": [0.466, "NaN", 0.668,"NaN"],
    "Stack": [0.465, "NaN", 0.669,"NaN"],
    "10_Fold_Stack": [0.481, 0.013, 0.639, 0.015]
}

results_df = pd.DataFrame(results, index=["RMSE", "RMSE Uncertainty", "R²", "R² Uncertainty"])

print(results_df.T)