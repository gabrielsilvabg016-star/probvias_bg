import psycopg2
from psycopg2 import sql
import base64

# Configuração da conexão
CFG = {
    "host": "localhost",
    "dbname": "gis",
    "user": "postgres",
    "password": "postgres",
    "port": 5432
}

# Nome da tabela e colunas
TABELA = "dadosfase2"
COL_ID = "id"
COL_LATITUDE = "latitude"
COL_LONGITUDE = "longitude"
COL_NOTES = "notes"
COL_ADDRESS = "address"
COL_FOTOS = ["foto1_bytea", "foto2_bytea", "foto3_bytea"]

def gerar_html():
    conn = psycopg2.connect(**CFG)
    cur = conn.cursor()

    # Monta a query dinâmica para pegar todas as colunas
    query = sql.SQL("SELECT {id}, {latitude}, {longitude}, {notes}, {address}, {fotos} FROM {tabela} ORDER BY id").format(
        id=sql.Identifier(COL_ID),
        latitude=sql.Identifier(COL_LATITUDE),
        longitude=sql.Identifier(COL_LONGITUDE),
        notes=sql.Identifier(COL_NOTES),
        address=sql.Identifier(COL_ADDRESS),
        fotos=sql.SQL(", ").join(map(sql.Identifier, COL_FOTOS)),
        tabela=sql.Identifier(TABELA)
    )
    cur.execute(query)

    # Cabeçalho HTML
    html = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>Relatório BYTEA</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .registro { border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 5px; }
            .info { margin-bottom: 15px; }
            .info p { margin: 5px 0; }
            .fotos { display: flex; gap: 15px; flex-wrap: wrap; margin-top: 15px; }
            .fotos img { max-width: 250px; height: auto; border: 1px solid #888; border-radius: 3px; }
            h2 { margin-top: 0; color: #333; }
            .label { font-weight: bold; color: #555; }
        </style>
    </head>
    <body>
    <h1>Relatório da fase 2</h1>
    """

    for row in cur.fetchall():
        id_ = row[0]
        latitude = row[1]
        longitude = row[2]
        notes = row[3]
        address = row[4]
        fotos = row[5:]
        
        html += f'<div class="registro">'
        html += f'<h2>ID: {id_}</h2>'
        html += f'<div class="info">'
        html += f'<p><span class="label">Latitude:</span> {latitude if latitude else "N/A"}</p>'
        html += f'<p><span class="label">Longitude:</span> {longitude if longitude else "N/A"}</p>'
        html += f'<p><span class="label">Endereço:</span> {address if address else "N/A"}</p>'
        html += f'<p><span class="label">Notas:</span> {notes if notes else "N/A"}</p>'
        html += '</div>'
        html += '<div class="fotos">'
        
        for i, foto in enumerate(fotos, start=1):
            if foto:
                b64_img = base64.b64encode(foto).decode("utf-8")
                html += f'<div><p>Foto {i}</p><img src="data:image/jpeg;base64,{b64_img}"></div>'
            else:
                html += f'<div><p>Foto {i}</p><p>(sem imagem)</p></div>'
        
        html += "</div></div>\n"

    html += "</body></html>"

    # Salva em arquivo
    with open("relatorio_fase2.html", "w", encoding="utf-8") as f:
        f.write(html)

    cur.close()
    conn.close()
    print("Relatório gerado: relatorio_bytea.html")

if __name__ == "__main__":
    gerar_html()