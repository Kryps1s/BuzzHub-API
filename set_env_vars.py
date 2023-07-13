"""for github actions to set environment variables"""
import os

try:
    env_file = os.getenv('GITHUB_ENV')
    with open(env_file, "a", encoding="utf-8") as env_file:
        env_file.write("env=test\n \
                       region=ca-central-1\n \
                       TRELLO_BOARD_BEEKEEPING=tVNzQnNQ\n \
                       TRELLO_BOARD_COLLECTIVE=RRqKnGAA\n \
                       TRELLO_BOARD_MEETING=KH88ovyS\n \
                       TRELLO_BOARD_TEMPLATES=KH88ovyS\n \
                       BEEKEEPING_BOARD_ID=61f889ff737a1d7b1031bb9d\n \
                       MEETING_BOARD_ID=61f889ff737a1d7b1031bb9d\n \
                       COLLECTIVE_BOARD_ID=61f889ff737a1d7b1031bb9d\n \
                       TRELLO_KEY=mocked\n \
                       TRELLO_TOKEN=mocked")
    print("+++ Environment variables is set +++")

except FileNotFoundError as e:
    print(f"+++ Error while setting the environment variable :: {e} +++")
