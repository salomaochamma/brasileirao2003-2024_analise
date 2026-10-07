from pathlib import Path

import numpy as np
import pandas as pd

PASTA_DADOS = Path(__file__).resolve().parent.parent / "data"
PASTA_RAW = PASTA_DADOS / "raw"
PASTA_PROCESSADOS = PASTA_DADOS / "processed"

ORDEM_FAIXAS = ["0-15", "16-30", "31-45", "45+", "46-60", "61-75", "76-90", "90+"]

NOMES_PARTIDAS = {
    "ID": "id",
    "rodata": "rodada",
    "mandante_Placar": "gols_mandante",
    "visitante_Placar": "gols_visitante",
    "mandante_Estado": "estado_mandante",
    "visitante_Estado": "estado_visitante",
}


def ler_partidas_brutas():
    return pd.read_csv(PASTA_RAW / "campeonato-brasileiro-full.csv")


def ler_gols_brutos():
    return pd.read_csv(PASTA_RAW / "campeonato-brasileiro-gols.csv")


def definir_temporada(datas):
    temporada = datas.dt.year
    jogos_2020_em_2021 = (datas >= "2021-01-01") & (datas < "2021-05-01")
    return temporada.mask(jogos_2020_em_2021, 2020)


def limpar_partidas(df):
    df = df.rename(columns=NOMES_PARTIDAS)
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df["arena"] = df["arena"].str.replace("\xa0", " ").str.strip()
    df["temporada"] = definir_temporada(df["data"])

    df["resultado"] = np.select(
        [df["gols_mandante"] > df["gols_visitante"], df["gols_mandante"] < df["gols_visitante"]],
        ["mandante", "visitante"],
        default="empate",
    )
    df["pontos_mandante"] = df["resultado"].map({"mandante": 3, "empate": 1, "visitante": 0})
    df["pontos_visitante"] = df["resultado"].map({"mandante": 0, "empate": 1, "visitante": 3})
    return df


def separar_minuto(minutos):
    partes = minutos.astype(str).str.extract(r"^(\d+)(?:\+(\d+))?$")
    minuto_base = partes[0].astype(int)
    acrescimo = partes[1].fillna(0).astype(int)
    return minuto_base, acrescimo


def classificar_faixa(minuto_base, acrescimo):
    condicoes = [
        (acrescimo > 0) & (minuto_base == 45),
        (acrescimo > 0) & (minuto_base == 90),
        minuto_base <= 15,
        minuto_base <= 30,
        minuto_base <= 45,
        minuto_base <= 60,
        minuto_base <= 75,
    ]
    faixas = ["45+", "90+", "0-15", "16-30", "31-45", "46-60", "61-75"]
    faixa = np.select(condicoes, faixas, default="76-90")
    return pd.Categorical(faixa, categories=ORDEM_FAIXAS, ordered=True)


def limpar_gols(df, partidas):
    df = df.rename(columns={"rodata": "rodada"})
    df["tipo_de_gol"] = df["tipo_de_gol"].fillna("Normal")
    df["minuto_base"], df["acrescimo"] = separar_minuto(df["minuto"])
    df["tempo"] = np.where(df["minuto_base"] <= 45, 1, 2)
    df["minuto_ordem"] = df["minuto_base"] + df["acrescimo"] / 100
    df["faixa"] = classificar_faixa(df["minuto_base"], df["acrescimo"])

    contexto = partidas[["id", "temporada", "mandante", "visitante"]]
    df = df.merge(contexto, left_on="partida_id", right_on="id", how="left").drop(columns="id")
    df["gol_mandante"] = df["clube"] == df["mandante"]
    return df


def carregar_partidas():
    return pd.read_csv(PASTA_PROCESSADOS / "partidas.csv", parse_dates=["data"])


def carregar_gols():
    gols = pd.read_csv(PASTA_PROCESSADOS / "gols.csv")
    gols["faixa"] = pd.Categorical(gols["faixa"], categories=ORDEM_FAIXAS, ordered=True)
    return gols
