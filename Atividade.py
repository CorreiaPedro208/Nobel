import json
import pandas as pd

with open("nobelPrizes.json", encoding="utf-8") as f:
    laureados = json.load(f)["laureates"]

df = pd.json_normalize(
    laureados,
    record_path="nobelPrizes",
    meta=["id",
        "gender",
        ["fullName", "en"],
        ["orgName", "en"],
        ["birth", "date"],
        ["birth", "year"],
        ["birth", "place", "country", "en"],
        ["birth", "place", "countryNow", "en"],
        ["birth", "place", "continent", "en"],],
    errors="ignore",
)

tabela = df[[
    "id", "fullName.en", "orgName.en", "gender",
    "birth.date", "birth.year",
    "birth.place.country.en", "birth.place.countryNow.en", "birth.place.continent.en",
    "awardYear", "category.en", "motivation.en", "portion", "prizeStatus",
]]
tabela = tabela.rename(columns={
    "fullName.en": "nome_pessoa",
    "orgName.en": "nome_organizacao",
    "gender": "genero",
    "birth.date": "data_nascimento",
    "birth.year": "ano_nascimento",
    "birth.place.country.en": "pais_nascimento",
    "birth.place.countryNow.en": "pais_nascimento_atual",
    "birth.place.continent.en": "continente_nascimento",
    "awardYear": "ano_premio",
    "category.en": "categoria",
    "motivation.en": "motivacao",
    "portion": "parcela_premio",
    "prizeStatus": "status_premio",
})
afiliacoes = []
paises = []
tabela["nome"] = tabela["nome_pessoa"].fillna(tabela["nome_organizacao"])
tabela = tabela.drop(columns=["nome_pessoa", "nome_organizacao"])


for lista in df["affiliations"]:
    if isinstance(lista, list) and len(lista) > 0:
        primeira = lista[0]
        afiliacoes.append(primeira["name"]["en"])
        paises.append(primeira.get("country", {}).get("en"))
    else:
        afiliacoes.append(None)
        paises.append(None)

tabela["afiliacao"] = afiliacoes
tabela["pais_afiliacao"] = paises


print(tabela.shape)
print(tabela.isna().sum())
print(tabela.head(5))

tabela.to_csv("nobel_vencedores.csv", index=False, encoding="utf-8")

