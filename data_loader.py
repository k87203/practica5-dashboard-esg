"""Descarga indicadores ESG del Banco Mundial y los guarda en CSV cacheado."""
from pathlib import Path
import requests
import pandas as pd

INDICATORS = {
    "NY.GDP.MKTP.CD": "gdp_usd",
    "EN.GHG.CO2.MT.CE.AR5": "co2_mt",
    "SP.POP.TOTL": "population",
}

CONTINENT_MAP = {
    "Africa": ["DZA","AGO","BEN","BWA","BFA","BDI","CMR","CPV","CAF","TCD","COM","COD","COG","CIV","DJI","EGY","GNQ","ERI","SWZ","ETH","GAB","GMB","GHA","GIN","GNB","KEN","LSO","LBR","LBY","MDG","MWI","MLI","MRT","MUS","MAR","MOZ","NAM","NER","NGA","RWA","STP","SEN","SYC","SLE","SOM","ZAF","SSD","SDN","TZA","TGO","TUN","UGA","ZMB","ZWE"],
    "Americas": ["ARG","BHS","BRB","BLZ","BOL","BRA","CAN","CHL","COL","CRI","CUB","DOM","ECU","SLV","GTM","GUY","HTI","HND","JAM","MEX","NIC","PAN","PRY","PER","SUR","TTO","USA","URY","VEN"],
    "Asia": ["AFG","ARM","AZE","BHR","BGD","BTN","BRN","KHM","CHN","CYP","GEO","IND","IDN","IRN","IRQ","ISR","JPN","JOR","KAZ","KWT","KGZ","LAO","LBN","MYS","MDV","MNG","MMR","NPL","OMN","PAK","PHL","QAT","SAU","SGP","KOR","LKA","SYR","TJK","THA","TLS","TUR","TKM","ARE","UZB","VNM","YEM"],
    "Europe": ["ALB","AND","AUT","BLR","BEL","BIH","BGR","HRV","CZE","DNK","EST","FIN","FRA","DEU","GRC","HUN","ISL","IRL","ITA","LVA","LIE","LTU","LUX","MLT","MDA","MCO","MNE","NLD","MKD","NOR","POL","PRT","ROU","RUS","SMR","SRB","SVK","SVN","ESP","SWE","CHE","UKR","GBR"],
    "Oceania": ["AUS","FJI","KIR","MHL","FSM","NRU","NZL","PLW","PNG","WSM","SLB","TON","TUV","VUT"],
}

CACHE = Path(__file__).parent / "data" / "esg_data.csv"


def _country_to_continent() -> dict:
    return {code: cont for cont, codes in CONTINENT_MAP.items() for code in codes}


def _fetch_indicator(code: str, start: int, end: int) -> pd.DataFrame:
    url = f"http://api.worldbank.org/v2/country/all/indicator/{code}"
    params = {"format": "json", "per_page": 20000, "date": f"{start}:{end}"}
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    payload = r.json()
    if len(payload) < 2 or payload[1] is None:
        return pd.DataFrame(columns=["iso3", "country", "year", INDICATORS[code]])
    rows = [
        {
            "iso3": item["countryiso3code"],
            "country": item["country"]["value"],
            "year": int(item["date"]),
            INDICATORS[code]: item["value"],
        }
        for item in payload[1]
        if item.get("countryiso3code")
    ]
    return pd.DataFrame(rows)


def download(start: int = 2000, end: int = 2022) -> pd.DataFrame:
    frames = [_fetch_indicator(code, start, end) for code in INDICATORS]
    df = frames[0]
    for f in frames[1:]:
        df = df.merge(f, on=["iso3", "country", "year"], how="outer")
    cont = _country_to_continent()
    df["continent"] = df["iso3"].map(cont)
    df = df.dropna(subset=["continent"])
    df = df.sort_values(["country", "year"]).reset_index(drop=True)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CACHE, index=False)
    return df


def load() -> pd.DataFrame:
    if CACHE.exists():
        return pd.read_csv(CACHE)
    return download()


if __name__ == "__main__":
    df = download()
    print(f"Descargados {len(df)} registros -> {CACHE}")
    print(df.head())
