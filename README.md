# 🗺️ Reverse-Geocoding 
A geocodificação reversa é o processo de conversão de coordenadas de latitude e longitude em endereços legíveis, como cidade, estado e país. Esse script automatiza esse processo para um arquivo CSV contendo coordenadas geográficas.  

## 📋 Requisitos
Versão utilizada do Python: 3.8.3  
As bibliotecas Python estão listadas no arquivo requirements.txt (ou instale-as manualmente).  
Um arquivo CSV contendo as colunas latitude e longitude.  

## 🛠️ Instalação
Clone este repositório ou faça o download do script.  
Instale as dependências necessárias executando: 
pip install -r requirements.txt  

## 📂 Estrutura do Arquivo CSV
O arquivo CSV de entrada deve conter pelo menos as seguintes colunas:  
latitude: Valores de latitude (em graus decimais).  
longitude: Valores de longitude (em graus decimais).  

### Exemplo: 
latitude;longitude  
-23.5505;-46.6333  
-22.9068;-43.1729

## Aplicação do script 💻
- Coloque o arquivo CSV na pasta do projeto ou forneça o caminho completo para o arquivo.  
- Execute o script: run reverse_geocoding.py  
- O script gerará um novo arquivo CSV (output.csv) com as colunas adicionais:  
cidade: Nome da cidade.  
estado: Nome do estado.  
pais: Nome do país.  

## 📄 Exemplo de Saída
latitude;longitude;cidade;estado;pais  
-23.5505;-46.6333;São Paulo;São Paulo;Brasil  
-22.9068;-43.1729;Rio de Janeiro;Rio de Janeiro;Brasil  

## 🙌 Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

