import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from sqlalchemy import create_engine

# Configurações do banco de dados  
db_url = 'postgresql+psycopg2://usuario:senha@localhost:5432/nome_do_banco'  
query = """
    SELECT id, latitude, longitude
    FROM nome_da_tabela """ 

# Caminho de saída para salvar o arquivo em formato csv  
output_path = "./caminho_para_onde_vai_o_output/arquivo_com_enderecos.csv"

# Inicialização do geocodificador Nominatim
geolocator = Nominatim(user_agent="contato@exemplo.com")  # O OpenStreetMap, que opera o Nominatim, incentiva
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
        print(f"Erro na geocodificação reversa para ({lat}, {lon}): {e}")
        return pd.Series([None, None, None])

# Conexão com o banco e execução da query  
engine = create_engine(db_url)
df = pd.read_sql(query, engine) 

# Aplicação do reverse geocoding para cada linha do DataFrame  
df[["cidade", "estado", "pais"]] = df.apply(
    lambda row: obter_localizacao(row["latitude"], row["longitude"]), axis=1
)

# Atualização dos registros no banco de dados  
if "id" in df.columns:
    with engine.connect() as connection:
        for i, row in df.iterrows():  # aqui, ele processa linha a linha do dataframe para, em seguida, lançar no banco
            update_query = f"""
                UPDATE nome_da_tabela
                SET cidade = '{row["cidade"]}', estado = '{row["estado"]}', pais = '{row["pais"]}'
                WHERE id = {row["id"]};
            """
            connection.execute(update_query)

df.to_csv(output_path, index=False)
print(f"Processamento concluído. Resultados salvos em {output_path}")
