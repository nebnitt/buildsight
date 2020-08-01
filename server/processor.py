from pybuildkite.buildkite import Buildkite, BuildState
from datetime import date
from yaml import load, BaseLoader
from typing import List, Dict
import os


class HandleSecrets:

    @staticmethod
    def get_api_token() -> str:
        """
        Loads the api token from the secrets path as defined by the env var JWAPP_CONFD
        :return: the buildkite api token
        """
        path_to_secrets: str = str(os.getenv('JWAPP_CONFD'))
        with open(os.path.join(path_to_secrets, 'api_token.yaml')) as f:
            yml: Dict = load(f, Loader=BaseLoader)
            return yml['BuildkiteApiToken']


class BuildkiteBuildMamba:

    organization: str = 'jwplayer'
    pipeline: str = 'billygoat'
    api_token: str = HandleSecrets.get_api_token()

    def __init__(self):
        self.buildkite = Buildkite()
        self.buildkite.set_access_token(self.api_token)
        self.start_date: date = date(2020, 7, 15)
        self.recent_blocked_builds: List[Dict] = self.get_all_recent_blocked_builds()

    def get_all_recent_blocked_builds(self) -> List[Dict]:
        """
        Gets a list of all recent buildkite builds that are in the BLOCKED status.
        :return: List of buildkite build objects
        """
        return self.buildkite.builds().list_all_for_pipeline(
            organization=self.organization,
            pipeline=self.pipeline,
            states=[BuildState.BLOCKED],
            created_from=self.start_date
        )

    def filter_builds_for_apps_of_interest(self, app: str) -> List[str]:
        """
        Filters the list of all builds for those that relate to a particular app
        :param app: the app of interest
        :return: A list of builds that relate to the app
        """
        relevant_build_ids: List[str] = []
        for build in self.recent_blocked_builds:
            jobs = build.get('jobs', {})
            for job in jobs:
                if app in job.get('name', ''):
                    build_id: str = job['build_url'].split('/')[-1]
                    print(build_id)
                    relevant_build_ids.append(build_id)
                    break
        return relevant_build_ids

    def run(self, app: str):
        self.filter_builds_for_apps_of_interest(app)


if __name__ == '__main__':
    BuildMamba = BuildkiteBuildMamba()
    BuildMamba.run('flink')
