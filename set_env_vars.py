"""for github actions tests to set environment variables"""
import os

try:
    env_file = os.getenv('GITHUB_ENV')
    with open(env_file, "a", encoding="utf-8") as env_file:
        env_file.write("env=test\n")
        env_file.write("region=ca-central-1\n")
        env_file.write("TRELLO_BOARD_BEEKEEPING=xhYDBHgy\n")
        env_file.write("TRELLO_BOARD_COLLECTIVE=GiK8hX8f\n")
        env_file.write("TRELLO_BOARD_MEETING=Ktv2HlsI\n")
        env_file.write("TRELLO_BOARD_TEMPLATES=KH88ovyS\n")
        env_file.write("BEEKEEPING_BOARD_ID=626194d91594996f726b6838\n")
        env_file.write("MEETING_BOARD_ID=64b21cca436d90217bd118ab\n")
        env_file.write("COLLECTIVE_BOARD_ID=64b21cde88cacf22ced015f1\n")
        env_file.write("BEEKEEPING_LIST_COMPLETED=64beb3f0205aede5e00af059\n")
        env_file.write("BEEKEEPING_LIST_UNASSIGNED=64da66bfdfc9d4cfe0c97b0e\n")
        env_file.write("TRELLO_KEY=mocked\n")
        env_file.write("TRELLO_TOKEN=mocked\n")
        env_file.write("BUZZHUB_ACCESS_CODE=test\n")
    print("+++ Environment variables are set +++")
except FileNotFoundError as e:
    print(f"+++ Error while setting the environment variable: {e} +++")
