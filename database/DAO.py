from database.DB_connect import DBConnect
from model.genere import Genere
from model.cantanti import Cantante

class DAO():
    @staticmethod
    def get_generi():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct g.*
                    from genre g"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Genere(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_nodi(c):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct ar.*
                    from Album a, Track  t , Artist ar
                    where a.AlbumId =t.AlbumId and t.GenreId =%s and a.ArtistId =ar.ArtistId """

        cursor.execute(query,(c,))
        res = []
        for row in cursor:
            res.append(Cantante(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_archi(c):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
                with clienteCheHafattoPiuDiUnAcquisto	as		(select distinct i.CustomerId as idcliente, il.TrackId as idprimoacquisto, il1.TrackId as idsecondoacquisto
from Invoice i, InvoiceLine il, invoice i1, InvoiceLine il1
where i.InvoiceId=il.InvoiceId and i.CustomerId =i1.CustomerId and il1.InvoiceId=i1.InvoiceId and il.TrackId !=il1.TrackId) 

select distinct least(a.ArtistId , a1.ArtistId ) as id1, greatest(a.ArtistId , a1.ArtistId ) as id2
from clienteCheHafattoPiuDiUnAcquisto ca, Track t, Track t1, Album a, Album a1
where ca.idprimoacquisto=t.TrackId and ca.idsecondoacquisto=t1.TrackId and t.AlbumId =a.AlbumId and t1.AlbumId =a1.AlbumId
and t.GenreId =%s and t1.GenreId =%s and a.ArtistId != a1.ArtistId 
group by least(a.ArtistId , a1.ArtistId ), greatest(a.ArtistId , a1.ArtistId )"""

        cursor.execute(query, (c,c))
        res = []
        for row in cursor:
            res.append((row["id1"],row["id2"]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_pesi(c):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select a.ArtistId as a, SUM(quantity) as peso
                From InvoiceLine il, Track t, Album a
                where il.TrackId=t.TrackId and t.AlbumId=a.AlbumId and t.GenreId=%s
                group by a.ArtistId
                    """

        cursor.execute(query,(c,))
        res = {}
        for row in cursor:
            res[row["a"]] = row["peso"]

        cursor.close()
        cnx.close()
        return res
