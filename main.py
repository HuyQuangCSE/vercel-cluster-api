import json
import uvicorn
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

df = pd.read_csv("clustered_products.csv")

app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)


@app.get("/")
async def root():
    return {"detail": "API's root"}


@app.get("/products/{product_id}")
async def get_product_list(product_id: int):
    try:
        cluster = df.loc[df["ProductID"] == product_id, "Cluster"].unique()
    except KeyError as exc:
        raise HTTPException(  # pylint: disable=W0707
            status_code=404, detail=f"Product not found, {exc}"
        )
    return_df = df[df["Cluster"].isin(cluster)].sample(n=20).to_json(orient="records")
    response = json.loads(return_df)
    return response


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
