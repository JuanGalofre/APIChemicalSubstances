from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DBHOSTNAME: str
    db_port: str
    DBUSERNAME: str
    db_password: str
    DBNAME: str
    skey: str
    algorithm:str
    token_time:int
    class Config: 
        env_file = "/etc/secrets/enviroment"
        #env_file = "AppAlch/.env" local stuff
settings= Settings()

