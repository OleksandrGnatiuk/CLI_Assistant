from setuptools import setup, find_packages

setup(name='CLI_Assistant',
      version='0.1.2',
      description='CLI Assistant helps to manage the address book, organizes file in folder',
      url='https://github.com/OleksandrGnatiuk/CLI_Assistant',
      author='Oleksandr Gnatiuk',
      author_email='oleksandr.gnatiuk@gmail.com',
      include_package_data=True,
      license='MIT',
      packages=find_packages(),
      entry_points={'console_scripts': ['assistant = CLI_Assistant.bot:main']}
      )