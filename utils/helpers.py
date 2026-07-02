import pandas as pd
import json
from typing import List, Dict, Any

def converter_para_csv(dados: List[Dict[str, Any]]) -> bytes:
    if not dados:
        return b""
    # Remove colunas complexas para o CSV plano
    df = pd.DataFrame(dados)
    if "json_resultado" in df.columns:
        df = df.drop(columns=["json_resultado"])
    return df.to_csv(index=False).encode('utf-8')

def converter_para_json(dados: List[Dict[str, Any]]) -> str:
    # Conversão customizada de data para serialização nativa
    return json.dumps(dados, default=str, indent=4, ensure_ascii=False)