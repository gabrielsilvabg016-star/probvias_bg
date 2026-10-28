#rodar antes
#instalar o python (olhar video)
#pip install psycopg2-binary
import psycopg2
from pathlib import Path

CFG = dict(
    dbname="gis",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432
)

# Pasta onde estão as imagens no Windows
PASTA_IMAGENS = Path(r"C:\temp")

with psycopg2.connect(**CFG) as conn, conn.cursor() as cur:
    # busca registros que têm nome de arquivo em qualquer uma das colunas
    cur.execute("""
        SELECT id, photo1, photo2, photo3
          FROM dadosfase2
         WHERE (photo1 IS NOT NULL AND photo1 <> '')
            OR (photo2 IS NOT NULL AND photo2 <> '')
            OR (photo3 IS NOT NULL AND photo3 <> ''); """)
    registros = cur.fetchall()

    for id_, photo1, photo2, photo3 in registros:
        # Processa photo1
        if photo1:
            caminho1 = PASTA_IMAGENS / photo1
            if caminho1.exists():
                img_bytes = caminho1.read_bytes()
                cur.execute("""
                    UPDATE dadosfase2
                       SET foto1_bytea = %s
                     WHERE id = %s; """, (psycopg2.Binary(img_bytes), id_))
        
        # Processa photo2
        if photo2:
            caminho2 = PASTA_IMAGENS / photo2
            if caminho2.exists():
                img_bytes = caminho2.read_bytes()
                cur.execute("""
                    UPDATE dadosfase2
                       SET foto2_bytea = %s
                     WHERE id = %s; """, (psycopg2.Binary(img_bytes), id_))
        
        # Processa photo3
        if photo3:
            caminho3 = PASTA_IMAGENS / photo3
            if caminho3.exists():
                img_bytes = caminho3.read_bytes()
                cur.execute("""
                    UPDATE dadosfase2
                       SET foto3_bytea = %s
                     WHERE id = %s; """, (psycopg2.Binary(img_bytes), id_))

    conn.commit()

print("Imagens importadas para as colunas BYTEA com sucesso.")
