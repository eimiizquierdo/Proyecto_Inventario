from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Config(BaseSettings):
    #prueba1: str = Field(default = "Hola", alias = "PRUEBA1")
    #prueba2: int = Field(default = 123, alias = "PRUEBA2")
    supabase_url: str = Field(default = "", alias="SUPABASE_URL")
    supabase_key: str = Field(default = "", alias="SUPABASE_KEY")
    supabase_schema: str = Field(default = "public", alias="SUPABASE_SCHEMA")
    supabase_table: str = Field(default = "product", alias="SUPABASE_TABLE")
    allowed_origins: list[str] = Field(default = [], alias = "ALLOWED_ORIGINS")

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" #El valor por default es: forbid
        )

    #supabase_url: str = Field(..., alias="SUPABASE_URL")
    #supabase_key: str = Field(..., alias="SUPABASE_KEY")
    
config = Config()
#print (config.prueba1)
#print (config.prueba2)
print (config.allowed_origins)