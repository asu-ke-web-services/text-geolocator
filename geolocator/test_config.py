# test_config.py
import config


def compareConfig(expected, actual):
    assert expected == actual


def test_config():
    import os
    assert (
        os.environ['JAVAHOME'] ==
        '/usr/lib/jvm/java-1.7.0-openjdk-amd64/bin')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    compareConfig(config.BASE_DIR, BASE_DIR)
    compareConfig(config.CSRF_ENABLED, True)
    compareConfig(config.DATABASE_CONNECT_OPTIONS, {})
    compareConfig(config.DEBUG, os.getenv('DEBUG', False))
    compareConfig(config.PORT, os.getenv('PORT', 5000))
    compareConfig(
        config.SQLALCHEMY_DATABASE_URI,
        os.getenv('DATABASE_URL',
                  'postgres://postgres@{0}/app'.format(
                      os.getenv('DB_1_PORT_5432_TCP_ADDR'))))
    compareConfig(config.SECRET_KEY, os.getenv('SECRET_KEY', None))
    compareConfig(config.UPLOAD_FOLDER, 'tmp/uploads')
    compareConfig(config.ALLOWED_EXTENSIONS, set(['txt']))
    compareConfig(
        config.SNER_CLASSIFIERS,
        (BASE_DIR +
            '/app/static/stanford-ner-2014-08-27/classifiers/english.all.'
            '3class.distsim.crf.ser.gz'))
    compareConfig(
        config.SNER_JARFILE,
        BASE_DIR + '/app/static/stanford-ner-2014-08-27/stanford-ner.jar')
