"""for github actions to set environment variables"""
import os

try:
    env_file = os.getenv('GITHUB_ENV')
    with open(env_file, "a", encoding="utf-8") as env_file:
        env_file.write("env=test")
    with open(env_file, "a", encoding="utf-8") as env_file:
        env_file.write("region=ca-central-1")
    print("+++ Environment variables is set +++")

except FileNotFoundError as e:
    print(f"+++ Error while setting the environment variable :: {e} +++")
