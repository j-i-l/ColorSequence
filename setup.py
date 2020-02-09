from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
        name='ColorSequence',
        # version='0.1',
        # ####################################################################
        # ####################################################################
        use_scm_version={'write_to': 'docs/version.txt'},
        setup_requires=['setuptools_scm'],
        # ####################################################################
        # ####################################################################
        description='Generate lists or generators for distinct colors.',
        long_description=readme(),
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: GNU General Public License 3',
            'Programming Language :: Python :: 3.6',
            'Topic :: Visualisation :: Colors :: Plotting',
        ],
        keywords='colors generator',
        url='https://github.com/j-i-l/ColorSequence',
        author='Jonas I. Liechti [aut, cre]',
        author_email='jonas.i.liechti@gmail.com',
        license='GPL-3',
        packages=['colorseq'],
        install_requires=[],
        test_suite='nose.collector',
        tests_require=['nose', 'nose-cover3'],
        # ToDo:
        # entry_points={
        #   'console_scripts': ['draw-alluvial=pyalluv.command_line:main'],
        # },
        include_package_data=True,
        zip_safe=False
        )
