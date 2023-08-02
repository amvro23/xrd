from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
   long_description = fh.read()


setup(
   name='xrd',
   version='0.1.0.rc3',
   description='XRD package.',
   long_description=long_description,
   author='Amvrosios Georgiadis',
   author_email='amvro23@gmail.com',
   packages=['xrd'],
   install_requires=[
      'numpy==1.19.*',
      'pandas>=1.1.*',
      'scipy>=1.7.*',
      'matplotlib',
      'lmfit',
      ],
)
