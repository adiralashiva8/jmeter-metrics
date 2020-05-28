from setuptools import setup, find_packages

filename = 'jmeter_metrics/version.py'
exec(compile(open(filename, 'rb').read(), filename, 'exec'))

setup(name='jmeter-metrics',
      version=__version__,
      description='Custom dashboard report for Jmeter',
      long_description='Dashboard view of jmeter results created by parsing .jtl or .csv file',
      classifiers=[
          'Programming Language :: Python',
          'Topic :: Software Development :: Testing',
      ],
      keywords='Jmeter report',
      author='Shiva Prasad Adirala',
      author_email='adiralashiva8@gmail.com',
      url='https://github.com/adiralashiva8/jmeter-metrics',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'pandas',
          'beautifulsoup4',
      ],
      entry_points={
          'console_scripts': [
              'jmetermetrics=jmeter_metrics.runner:main',
          ]
      },
      )
