from fastapi import FastAPI
import requests 
from bs4 import BeautifulSoup
import uvicorn


#aqui instancio la framework
app = FastAPI() 


def limpiar_tasa(texto):
    # Remplazo la coma por punto y limpio los espacios 
    valor =  texto.strip().replace(',','.')
    return "{:.4f}".format(float(valor)) # muestra los 4 decimales


@app.get("/tasas")
def obtener_tasas():
    url = "https://www.bcv.org.ve/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        #realizar la peticion bcv ignrando los erroes si exiteng por ssl 
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

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
