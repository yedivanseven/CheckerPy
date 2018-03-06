from setuptools import setup, find_packages

setup(name='checkerpy',
      version='0.9.7',
      description='Type and value checkers both as callables and decorators',
      url='https://github.com/yedivanseven/CheckerPy',
      download_url='https://pypi.python.org/pypi/checkerpy',
      author='Georg Heimel',
      author_email='georg@muckisnspirit.com',
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Software Development'],
      keywords='validation',
      packages=find_packages(exclude=['checkerpy.tests', 'checkerpy.tests.*']),
      python_requires='>=3.6',
      test_suite='checkerpy.tests')
