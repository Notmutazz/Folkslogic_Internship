import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump
import matplotlib.pyplot as plt
import sys
df = pd.read_csv("sales_data_24m.csv")
df["MonthIndex"] = df["Year"] * 100 + df["Month_Number"]
features = ["Advertising_Spend","Website_Visits","Discount_Rate","Month_Number"]
X = df[features].values
y = df["Sales"].values
scaler = StandardScaler()
Xs = scaler.fit_transform(X)
tscv = TimeSeriesSplit(n_splits=4)
rfs = []
ridges = []
scores = []
for train_index, test_index in tscv.split(Xs):
    X_train, X_test = Xs[train_index], Xs[test_index]
    y_train, y_test = y[train_index], y[test_index]
    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)
    rpred = rf.predict(X_test)
    rscore = r2_score(y_test, rpred)
    rfs.append((rf, rscore))
    ridge = Ridge(alpha=1.0)
    ridge.fit(X_train, y_train)
    pred_ridge = ridge.predict(X_test)
    r2r = r2_score(y_test, pred_ridge)
    ridges.append((ridge, r2r))
    scores.append((rscore, r2r))
best_rf, best_rf_score = max(rfs, key=lambda x: x[1])
best_ridge, best_ridge_score = max(ridges, key=lambda x: x[1])
print("RandomForest best R2:", round(best_rf_score,4))
print("Ridge best R2:", round(best_ridge_score,4))
X_full = Xs
y_full = y
future_months = []
last_month = int(df["Month_Number"].iloc[-1])
for i in range(1,7):
    mnum = last_month + i
    ad = int(df["Advertising_Spend"].tail(3).mean())
    visits = int(df["Website_Visits"].tail(3).mean())
    disc = round(float(df["Discount_Rate"].tail(3).mean()),1)
    future_months.append([ad,visits,disc,mnum])
X_future = scaler.transform(np.array(future_months))
pred_future = best_rf.predict(X_future)
future_index = np.arange(len(y_full), len(y_full)+len(pred_future))
plt.figure(figsize=(10,4))
plt.plot(np.arange(len(y_full)), y_full, label="Historical Sales")
plt.plot(future_index, pred_future, linestyle="--", marker="o", label="Forecast (6 months)")
plt.xlabel("Time Index")
plt.ylabel("Sales")
plt.legend()
plt.tight_layout()
plt.savefig("sales_forecast.png")
plt.close()
dump(best_rf, "best_sales_model.joblib")
print("Forecast for next 6 months:")
for i,p in enumerate(pred_future,1):
    print(f"Month +{i}: {int(round(p))}")
if len(sys.argv) > 1 and sys.argv[1] == "--show":
    import matplotlib.image as mpimg
    img = mpimg.imread("sales_forecast.png")
    import matplotlib.pyplot as plt
    plt.imshow(img); plt.axis("off"); plt.show()
