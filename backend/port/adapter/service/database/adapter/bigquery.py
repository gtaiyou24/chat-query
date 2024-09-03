import json
from typing import override

from google.cloud import bigquery
from google.oauth2 import service_account

from modules.analytics.domain.model.database import DataSet, Field
from port.adapter.service.database.adapter import DataBaseAdapter


class BigQueryAdapter(DataBaseAdapter):
    def __init__(self):
        self.__translator = BigQueryTranslator()

    @staticmethod
    def client(service_account_json: dict) -> bigquery.Client:
        credentials = service_account.Credentials.from_service_account_info(
            service_account_json,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        return bigquery.Client(credentials=credentials, project=credentials.project_id, location='asia-northeast1')

    @property
    def account_service(self) -> dict:
        json_data = """{
          "type": "service_account",
          "project_id": "customer-database-421207",
          "private_key_id": "a03a6dfa058fb3ff3f9073e80238a69a90b37ff6",
          "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDpNX1hy8xPeGHD\n8kiWApG0d2PFFCUka/RtloTu/jWIj4nrmnuSOPmh/pV4pI/n0zV/0PQEyphEGUd6\nk0/BOp0KPTw9Z7DOY9HgenkuzH2u8MhCdsSWVeiCta0E8Sa4OF7UHc0dMFULUXkU\n9s9NjDrF2550+q5mrpanNuuyA/J1cizdt7Nj9wkiOSpcFPszG9JI/BLow4SJpOMT\nhhhmEY6ZfeJNnhiMTnq2qXN2j3P0d+9w4W3cr059+tCmAb7uEnD0HKWcaWH8X/pQ\nG6PyHFWCtOPU3If01hs4j1Zv8WCqvxsIzwXef4x+ngGg16CdCktR8gDPnMMm5wkz\nJDhKcrPDAgMBAAECggEAEEL9SyBhm7MHW8xqJYe1VRiA82eigjLC693AlESGqbVn\n04ir3QThdCg8w2ZaOiFr5bQSdL95znNvnNgz1tBsmrlG/5MnUyT6KBIlbBvkGBqz\nJCtRYJhJ98wnIST9sBl1YPFZC0ccNW28QmsTBoaX1iv1YmI7XtUF+hzMYtcZBSzL\nm6JV0YpSxCg+hT3+SsF4J7UkACRb83yAgG2rNmvjeaHGzSyQklxx1Y8Z/d1mVqlg\nPClCj0YITqXIJoVO8b2m11o0alu3cEwVJbYoAHSxEzRAB8iXrnm3R1VgQiiyVU5j\nyuvI0KNDeOaehj8PlDKXpRRW3XCHPiDs5KJivmFNzQKBgQD3sgKsL5/RaXCtD2LH\nI0LlTf0CiS/MNs4iz4KxYTxtKWnkjo3iCNQjmpFiui4TtDlgwlUqHqyyAzjSoKqn\n0MLC5gpSQ7G42IrOs7MBSHyh5f77zk340nJ++gXLI/RHrULBJMGevN8A6qmXPFwr\nwr7oOFMpLGgJ/S2xAitz2qI8DQKBgQDxByQsBXY9j1+fpqrBrhupA6Po6itsureP\ne50QqqL/6NFmXTTDOcAvR7x3YBFNeFRau8vvMPd4XveuRFArF/egBDWvt8j3Dj9b\nYlKdGtf57sVgdVl0j5NKWnQ2cAzpgi/uMbfPUFHn03PUK0P6zSpRHqEi+QKdk4AX\nlk+R0IcrDwKBgDBbva/WQHKHDmuLNHLCjJ3uIvZqyD0regVL1C1DWaPKURVBS6wU\noy4sUDQhOzu3lPgyGKR3hqnefSqKGadX155rgRpcgwcep8MBTHJ0r3iASc7pkUmB\n9L6bm6P0ag3QYtcIkRCnuTYZmnCfZTNZ+yGlVX8VX16L4m7LiKY+yivFAoGBAJXP\nGH58DpgIqyiyEOQ88VhFuPUlx0PXcgwuits3FAT3kl+LgyXsmTVJ4yxXe6mpJtUW\ncJUE3Gvmqw+XyjReuzysISpMkw5rvplwLWUUsDTaYbeoeKdoLeZC/oRvdLcWgfAM\n2vByPdZXqWCwW5phNvIglYsFNsj2SuFePaql772lAoGBAL1ZVRtO5D/Zk56h9FCo\nstvGQY+kcnKP+zdplhaWs/ObCoN9E3oi4NOTFN82adrpPtHkV+p/SxjN3tqRXmnE\nKOEZidV4+3KKd4ESQo/8+24ukhcek34dcL9lkiwxuG8uOo20jhoNkkqMU8ZFJzHL\nRFhxE8i9Ks3RmBHZoy+Im6/x\n-----END PRIVATE KEY-----\n",
          "client_email": "analytics-gpt@customer-database-421207.iam.gserviceaccount.com",
          "client_id": "103630875542369936550",
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://oauth2.googleapis.com/token",
          "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
          "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/analytics-gpt%40customer-database-421207.iam.gserviceaccount.com",
          "universe_domain": "googleapis.com"
        }"""
        return json.loads(json_data, strict=False)

    @override
    def schemas(self) -> list[str]:
        with self.client(self.account_service) as client:
            r: bigquery.QueryJob = client.query(
                "SELECT table_name, ddl FROM `region-asia-northeast1`.INFORMATION_SCHEMA.TABLES",
                bigquery.QueryJobConfig(use_query_cache=True)
            )
            return [row["ddl"] for i, row in r.to_dataframe().iterrows()]

    @override
    def query(self, query: str) -> DataSet | None:
        with self.client(self.account_service) as client:
            r: bigquery.table.RowIterator = client.query_and_wait(query)
            return self.__translator.dataset_from(r)


class BigQueryTranslator:
    def dataset_from(self, response: bigquery.table.RowIterator) -> DataSet:
        dataframe = response.to_dataframe()
        return DataSet(
            fields=[Field(name=name, semantic_type=str) for name, dtype in dataframe.dtypes.to_dict().items()],
            data_source=dataframe.to_dict('records')
        )
