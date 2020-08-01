import cherrypy
from server.processor import BuildkiteBuildMamba


class BuildsightResource:

    @cherrypy.expose
    def buildsight(self, app: str):
        BuildMamba = BuildkiteBuildMamba()
        BuildMamba.run(app)


if __name__ == '__main__':
    cherrypy.quickstart(BuildsightResource())
