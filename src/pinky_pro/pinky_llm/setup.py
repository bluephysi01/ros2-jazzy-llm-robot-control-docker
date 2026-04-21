from setuptools import find_packages, setup

package_name = 'pinky_llm'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['pinky_llm/.env']),
        ('share/' + package_name, ['pinky_llm/robot_tools.py',]),
        ('share/' + package_name + '/params',[
            'params/prompt.yaml',
        ]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='subin',
    maintainer_email='subin@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'agent_service = pinky_llm.agent_service:main',
            'agent_client = pinky_llm.agent_client:main',
        ],
    },
)
