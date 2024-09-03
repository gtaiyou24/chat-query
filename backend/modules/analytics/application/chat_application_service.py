from typing import Literal

from injector import singleton, inject

from modules.analytics.application.dpo import DataSetDpo
from modules.analytics.domain.model.database import DataBaseService
from modules.analytics.domain.model.llm import LLMService, Message, Messages

type message = tuple[Literal['user', 'assistant', 'system'], str]


@singleton
class ChatApplicationService:
    @inject
    def __init__(self,
                 database_service: DataBaseService,
                 llm_service: LLMService):
        self.database_service = database_service
        self.llm_service = llm_service

    def chat(self, messages: list[message]) -> list[message]:
        messages = Messages([Message(role=Message.Role[m[0]], content=m[1]) for m in messages])
        messages = self.llm_service.chat(messages)
        return []

    def dataset(self, user_query: str) -> DataSetDpo:
        schemas = self.database_service.schemas()
        messages = Messages.thread(
            Message.Role.SYSTEM(f'''Act as if you're a data scientist who uses exclusively GoogleSQL syntax in BigQuery. 
            Note that in 2024, GoogleSQL was called Google Standard SQL.
    
            You have a BigQuery tables with the following schemas.
            ```{"\n".join(schemas)}```
    
            Based on this data, write a SQL query to answer my questions.
            Return the SQL query ONLY so that it will be executable in BigQuery.
            Do not include any additional explanation.
            Remember that table names must be in the form of `project.dataset_id.table_id` in a GoogleSQL query.
            Enclose Japanese column names with backticks (``).
            '''),
            Message.Role.USER(user_query)
        )

        messages = self.llm_service.chat(messages)

        max_attempts = 0
        while max_attempts <= 10:
            try:
                query = messages.list[-1].content
                dataset = self.database_service.query(query.replace('```sql', '').replace('```', ''))
                return DataSetDpo(query, dataset)
            except Exception as e:
                messages = messages.replay(Message.Role.USER(f'''I ran the query in BigQuery and received the following error(s):
                ```{e}```
                Return a corrected SQL query only with no additional explanation.
                '''))
                messages = self.llm_service.chat(messages)
                max_attempts += 1

        raise RuntimeError('fafa')
