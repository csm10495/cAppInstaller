from setuptools import setup

setup(
    name='cappinstaller',
    author='csm10495',
    author_email='csm10495@gmail.com',
    url='http://github.com/csm10495/cappinstaller',
    packages=['cappinstaller'],
    license='MIT License',
    python_requires='>=3.8',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    include_package_data = True,
    install_requires=['git+https://github.com/csm10495/PySimpleGUI-4-foss', 'numpy'],
)
