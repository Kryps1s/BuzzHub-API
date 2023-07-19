"""for github actions to set environment variables"""
import os

try:
    env_file = os.getenv('GITHUB_ENV')
    with open(env_file, "a", encoding="utf-8") as env_file:
        env_file.write("env=test\n")
        env_file.write("region=ca-central-1\n")
        env_file.write("TRELLO_BOARD_BEEKEEPING=tVNzQnNQ\n")
        env_file.write("TRELLO_BOARD_COLLECTIVE=RRqKnGAA\n")
        env_file.write("TRELLO_BOARD_MEETING=KH88ovyS\n")
        env_file.write("TRELLO_BOARD_TEMPLATES=KH88ovyS\n")
        env_file.write("BEEKEEPING_BOARD_ID=61f889ff737a1d7b1031bb9d\n")
        env_file.write("MEETING_BOARD_ID=61f889ff737a1d7b1031bb9d\n")
        env_file.write("COLLECTIVE_BOARD_ID=61f889ff737a1d7b1031bb9d\n")
        env_file.write("TRELLO_KEY=mocked\n")
        env_file.write("TRELLO_TOKEN=mocked\n")
        env_file.write("BUZZHUB_ACCESS_CODE=test\n")
    print("+++ Environment variables are set +++")
except FileNotFoundError as e:
    print(f"+++ Error while setting the environment variable: {e} +++")
