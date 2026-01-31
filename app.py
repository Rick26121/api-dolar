from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import uvicorn

app = FastAPI()

def limpiar_tasa(texto):
    # Reemplaza coma por punto y limpia espacios
    valor = texto.strip().replace(',', '.')
    return "{:.4f}".format(float(valor)) # Fuerza 4 decimales

@app.get("/tasas")
def obtener_tasas():
    url = "https://www.bcv.org.ve/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # Petición al BCV ignorando errores de certificado SSL
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscamos los contenedores específicos del BCV
        dolar = soup.select_one('#dolar strong').text
        euro = soup.select_one('#euro strong').text

        return {
            "status": "success",
            "dolar": limpiar_tasa(dolar),
            "euro": limpiar_tasa(euro),
            "fuente": "BCV"
        }
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)