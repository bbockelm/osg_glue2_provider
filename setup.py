
from distutils.core import setup

setup(name="osg_glue2_provider",
      version="0.1",
      description="GLUE2 provider for the OSG",
      author="Brian Bockelman",
      author_email="bbockelm@cse.unl.edu",
      url="https://github.com/bbockelm/osg_glue2_provider",
      packages=['osg_glue2_provider', 'osg_glue2_provider', 'osg_glue2_provider'],
      package_dir={"": "src"},
      scripts=['src/fts2_provider'],
      data_files = [('/etc/osg/config.d', ['config/glue2.cfg']),
                    ('/usr/share/gip/templates', ['templates/Glue2Service',
                                                  'templates/Glue2Site',
                                                  'templates/Glue2Storage'])],
     )

