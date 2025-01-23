import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

df =  pd.read_csv('caminho_para_o_csv/arquivo.csv', sep = ';') # Aqui, realizei a leitura do .csv, que tem o separador " ; "
output_path = "./caminho_para_onde_vai_o_output/arquivo_com_enderecos.csv"

# Inicialização do geocodificador Nominatim
geolocator = Nominatim(user_agent="contato@exemplo.com") # O OpenStreetMap, que opera o Nominatim, incentiva
# que se inclua um e-mail de contato no user_agent para que eles possam entrar em contato caso haja problemas, como uso excessivo ou requisições mal formuladas.
geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1)

# Crio a função para obter cidade, estado e país a partir das colunas "latitude" e "longitude" no df
def obter_localizacao(lat, lon):
    try:
        location = geocode((lat, lon), exactly_one=True, language='pt')
        if location:
            address = location.raw.get('address', {})
            cidade = address.get('city') or address.get('town') or address.get('village')
            estado = address.get('state')
            pais = address.get('country')
            return pd.Series([cidade, estado, pais])
        else:
            return pd.Series([None, None, None])
    except Exception as e:
        print(f"Erro na geocodificação reversa: {e}")
        return pd.Series([None, None, None])

# Verificação da existência das colunas necessárias no df
required_columns = ["latitude", "longitude"]
if not all(column in df.columns for column in required_columns):
    raise ValueError(f"O arquivo CSV deve conter as colunas: {required_columns}")

# Aplicação do reverse geocoding para cada linha do DataFrame
df[["cidade", "estado", "pais"]] = df.apply(
    lambda row: obter_localizacao(row["latitude"], row["longitude"]), axis=1
)

df.to_csv(output_path, index=False) # salvo o arquivo final no caminho desejado
print(f"Processamento concluído. Resultados salvos em {output_path}")
