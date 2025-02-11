from setuptools import setup

setup(
   name='evm_wallet',
   version='0.1.1',
   description='Module to work with EVM web3 wallets',
   author='GuessWho',
   author_email='eu1qjqaw8dda@mail.ru',
   packages=['evm_wallet'],
   include_package_data=True,  # Include non-Python files specified in MANIFEST.in
   package_data={
      'evm_swapper': ['contracts/*'],  # Explicitly include the contracts directory
   },
   install_requires=[]
)
